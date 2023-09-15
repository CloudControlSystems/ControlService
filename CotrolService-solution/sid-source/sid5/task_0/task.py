import numpy as np
from concurrent import futures
import os, socket, threading, json, time, sys, grpc, pickle, redis
from base_package import data_pb2, data_pb2_grpc
from utils import TaskProcessFunction
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial

"""
Function: send start signals
"""
_ONE_DAY_IN_SECONDS = 60 * 60 * 24

"""
Change the transfer size limit
"""
# options = [('grpc.max_send_message_length', 64*1024*1024),('grpc.max_receive_message_length', 64*1024*1024)]


global sid, volumeDirectory, receiveDirectory, taskReceiveCompleteStateMap, inputData, taskId, taskInputOutputDataMap

class TaskDataTransmitService(data_pb2_grpc.TaskDataTransmitServiceServicer):

    def TransmitTaskData(self, request, context):

        parentId = request.taskOrder
        parentData = pickle.loads(request.transmitData)
        receiveDirectory[parentId] = parentData
        taskReceiveCompleteStateMap[parentId] = True
        
        # set the flag of carrying out parent tasks as False   
        # get the parent tasks
        #parentTasks = taskInputOutputDataMap['input']
        print("parentTasks: ", parentTasks)       
        #inputData = [None]*len(parentTasks)
        inputData[parentId] = receiveDirectory[parentId]
        # put the data as parent order

        #print('outputData: ', outputData)

        accumulatedBoolVar = True

        for parentId in taskInputOutputDataMap['input']:
            parentId = np.uint32(parentId)
            accumulatedBoolVar = accumulatedBoolVar and taskReceiveCompleteStateMap[parentId]

        if accumulatedBoolVar:

            outputData = TaskProcessFunction(inputData)
            #for childTaskId in taskInputOutputDataMap['output']:
                # res = sendDataToNextTask(outputData, childTaskId, taskId)
                # print('Send success code: ', res.result)
            childrenTasks = taskInputOutputDataMap['output']

            func = partial(sendDataToNextTask, outputData, taskId)

            pool_2 = ThreadPool()
            result = pool_2.map(func, childrenTasks)
            print('result: ', result)
            pool_2.close()
            pool_2.join()

        return data_pb2.TransmitTaskDataResponse(result=0,volumePath=volumeDirectory)

def grpcServer():
    # get self IP
    selfIp = GetHostIp()
    # start grpcServer
    grpcServer = grpc.server(futures.ThreadPoolExecutor(max_workers = 100), options = [('grpc.max_send_message_length', 64*1024*1024),('grpc.max_receive_message_length', 64*1024*1024)])
    data_pb2_grpc.add_TaskDataTransmitServiceServicer_to_server(TaskDataTransmitService(), grpcServer)
    grpcServer.add_insecure_port(selfIp + ':' + '6060')
    grpcServer.start()
    print("Start grpc server...")
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        grpcServer.stop(0)
    #grpcServer.wait_for_termination()

def sendDataToNextTask(outdata, taskId, childTaskId):

    dataJson = pickle.dumps(outdata)
    # childTaskIp = serviceHostMap[childTaskId]
    # we acquire the service host env through env viriable
    serviceHost = 'TASK_SVC_' + childTaskId + '_SERVICE_HOST'

    while True:
        serviceHostIp = os.environ.get(serviceHost)
        if serviceHostIp != '' and serviceHostIp != None:
            break
    print('serviceHostIp: ', serviceHostIp)

    conn = grpc.insecure_channel(serviceHostIp + ':' + '6060', options = [('grpc.max_send_message_length', 64*1024*1024),('grpc.max_receive_message_length', 64*1024*1024)])
    client = data_pb2_grpc.TaskDataTransmitServiceStub(channel=conn)

    # record the current time, microseconds
    startTime = int(time.time()*1000000)
    # write into redis
    sid.set('startTime', startTime)
    
    response = client.TransmitTaskData(data_pb2.TransmitTaskDataRequest(taskOrder = taskId, transmitData=dataJson))
    conn.close()
    return response


def RunTask():

    #initialize taskReceiveCompleteStateMap
    if taskFlag != 'startTask':
        for parentId in taskInputOutputDataMap['input']:
            parentId = np.uint32(parentId)
            taskReceiveCompleteStateMap[parentId] = False 
        print('taskReceiveCompleteStateMap: ',taskReceiveCompleteStateMap)     
    # start grpc thread
    grpcThread = threading.Thread(target=grpcServer)
    grpcThread.start()

    # send the data to children tasks
    # delay 30 seconds, waiting for the start of taska's grpc server
    time.sleep(20)

    if taskFlag == 'startTask':
        # get the parent tasks
        inputData['startTask'] = 'start'

        outputData = TaskProcessFunction(inputData)
        
        #print('startTime: ', sid.get('startTime'))

        childrenTasks = taskInputOutputDataMap['output']
        # for childTaskId in childrenTasks:

        #     outdata = outputData
        #     res = sendDataToNextTask(outdata,childTaskId,taskId)
        #     print('Send success code: ', res.result)

        func = partial(sendDataToNextTask, outputData, taskId)
        pool_2 = ThreadPool()
        result = pool_2.map(func, childrenTasks)
        print('result: ', result)
        pool_2.close()
        pool_2.join()


    elif taskFlag == 'endTask':

        print('The whole control workflow is finished.')


def GetHostIp():

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip



if __name__ == '__main__':

    # create some map
    taskReceiveCompleteStateMap = {}
    receiveDirectory = {}
    inputData = {}
    taskInputOutputDataMap = {}

    redisIp = os.environ.get("REDIS_IP")
    # sid = redis.StrictRedis(host="172.23.27.47", port = 6379, db=0)
    sid = redis.StrictRedis(host=redisIp, port = 6379, db=0)
    print('redis连接成功')
      # read the PATH of loading volume
    volumeDirectory = os.environ.get("VOLUME_PATH")
    print('volumeDirectory: ', volumeDirectory)

    # read the DAG relationship MAP
    envMAP = os.environ.get("ENV_MAP")
    taskInputOutputDataMap = json.loads(envMAP)
    print('taskInputOutputDataMap: ', taskInputOutputDataMap)
    # read the Service IP map associated with Task Pod
    # serviceMap = os.environ.get("SERVICE_MAP")
    # serviceHostMap = json.loads(serviceMap)
    # print("serviceHostMap: ", serviceHostMap)

    # read the env_variable to get the task index
    taskId = os.environ.get("TASK_ID")
    taskId = int(taskId)

    # read the env_variable to get the task flag: startTask, endTask, nomialTask
    taskFlag = os.environ.get("TASK_FLAG")

    RunTask()

    print('Task is finished')