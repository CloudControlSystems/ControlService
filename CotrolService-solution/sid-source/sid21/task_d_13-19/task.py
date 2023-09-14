import numpy as np
from concurrent import futures
import os, pickle, socket, threading, json, time, sys, grpc, redis
from base_package import data_pb2, data_pb2_grpc
from utils import TaskProcessFunction
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial
"""
input: an block matrix of O_i from task_1
output1: Truncated (u, s, v) to it's successor task
"""
_ONE_DAY_IN_SECONDS = 60 * 60 * 24

"""
Change the transfer size limit
"""
# options = [('grpc.max_send_message_length', 64*1024*1024),('grpc.max_receive_message_length', 64*1024*1024)]

global sid, volumeDirectory, receiveDirectory, taskReceiveCompleteStateMap, inputData, taskId, taskInputOutputDataMap

class TaskDataTransmitService(data_pb2_grpc.TaskDataTransmitServiceServicer):

    def TransmitTaskData(self, request, context):

        # current_time = int(time.time()*1000000)
        # startTime = int(sid.get('startTime'))        
        # transmission_from_task0_to_taskd = current_time - startTime
        # print('transmission_from_task0_to_taskd: ', transmission_from_task0_to_taskd/1000)
        # # write into redis
        # sid.set('taskdTime', current_time)

        parentId = request.taskOrder
        parentData = pickle.loads(request.transmitData)
        receiveDirectory[parentId] = parentData
        # print('parentData: ', parentData)
        taskReceiveCompleteStateMap[parentId] = True
        
        accumulatedBoolVar = True

        for parentId in taskInputOutputDataMap['input']:
            parentId = np.uint32(parentId)
            accumulatedBoolVar = accumulatedBoolVar and taskReceiveCompleteStateMap[parentId]

        if accumulatedBoolVar:

            parentTasks = taskInputOutputDataMap['input']
            print("parentTasks: ", parentTasks)  
            #inputData = [None]*len(parentTasks)

            for num, parentId in enumerate(parentTasks):
                parentId = np.uint32(parentId)
                inputData[num] = receiveDirectory[parentId]


            #current_time_before_process_data = int(time.time()*1000000)
            outputData = TaskProcessFunction(inputData)
            # print('outputData: ', outputData)
            # current_time_after_process_data = int(time.time()*1000000)
            # computation_taskd_time = current_time_after_process_data - current_time_before_process_data
            # print('computation_taskd_time: ', computation_taskd_time/1000)
                        
            childrenTasks = taskInputOutputDataMap['output']
            descendantTasks = childrenTasks
            # for num, childTaskId in enumerate(childrenTasks):
            #     res = sendDataToNextTask(outputData[num], childTaskId, taskId)
            #     print('Send success code: ', res.result)
            func = partial(sendDataToNextTask, outputData, taskId, descendantTasks)

            pool_2 = ThreadPool()
            result = pool_2.map(func, childrenTasks)
            print('result: ', result)
            pool_2.close()
            pool_2.join()
               
        return data_pb2.TransmitTaskDataResponse(result=0,volumePath=volumeDirectory)



def grpcServer():
    # get self IP
    selfIp = GetHostIp()
    print('selfIp: ', selfIp)
    # start grpcServer
    grpcServer = grpc.server(futures.ThreadPoolExecutor(max_workers = 100), options = [('grpc.max_send_message_length', 64*1024*1024),('grpc.max_receive_message_length', 64*1024*1024)])
    data_pb2_grpc.add_TaskDataTransmitServiceServicer_to_server(TaskDataTransmitService(), grpcServer)
    grpcServer.add_insecure_port(selfIp + ':' + '6060')
    grpcServer.start()
    print("Start grpc server...")
    #grpcServer.wait_for_termination()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        grpcServer.stop(0)
        

def sendDataToNextTask(outdata, taskId, descendantTasks, childTaskId):

    for num, taskIndex in enumerate(descendantTasks):
        if taskIndex == childTaskId:          
            order = num
            break  
        print('taskReceiveCompleteStateMap: ',taskReceiveCompleteStateMap)                 
    dataJson = pickle.dumps(outdata[order])
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
    response = client.TransmitTaskData(data_pb2.TransmitTaskDataRequest(taskOrder = taskId, transmitData=dataJson))
    conn.close()
    return response


def RunTask():

    #initialize taskReceiveCompleteStateMap
    if taskFlag != 'startTask':
        for parentId in taskInputOutputDataMap['input']:
            parentId = np.uint32(parentId)
            taskReceiveCompleteStateMap[parentId] = False 

    # start grpc thread
    grpcThread = threading.Thread(target=grpcServer)
    grpcThread.start()

    # send the data to children tasks
    if taskFlag == 'startTask':

        # get the parent tasks
        inputData['startTask'] = 'start'
        outputData = TaskProcessFunction(inputData)
        childrenTasks = taskInputOutputDataMap['output']
        # for childTaskId in childrenTasks:
            
        #     outdata = outputData
        #     res = sendDataToNextTask(outdata,childTaskId,taskId)
        #     print('Send success code: ', res.result)
        descendantTasks = childrenTasks
        func = partial(sendDataToNextTask, outputData, taskId, descendantTasks)
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
    
     # connect to the redis   
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
    print("taskInputOutputDataMap: ", taskInputOutputDataMap)

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