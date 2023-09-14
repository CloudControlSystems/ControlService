import json, pickle, os, time, redis, sys, socket
from utils import TaskProcessFunction
import numpy as np
"""
Function: send start signals
"""

def get_host_ip():

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

# def send_data_to_child(ip, data):

#     #print("建立连接")
#     tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     #print("enter it deeper")
#     tcp_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
#     server_ip = ip
#     server_port = 7070
#     server_addr = (server_ip, server_port)
    
#     tcp_socket.connect(server_addr)
#     #print("scale of row data: ", sys.getsizeof(pickle.dumps(data)))
#     print("序列化数据")
#     send_data = pickle.dumps(data)
#     print("scale: ", sys.getsizeof(send_data))
#     print("准备发送")
#     tcp_socket.send(send_data)
#     #print("have sent")
#     #back_data = tcp_socket.recv(1024)
#     tcp_socket.close()
#     print("发送完毕")
#     #print("------------------------")


# def client_for_child(ip, data):

#     while True:

#         try:
#             send_data_to_child(ip, data)
#             break
#         except:
            # continue


if __name__ == '__main__':
    
    inputData = {}
    print('任务开始')
  
    # redisIp = os.environ.get("REDIS_IP")
    taskId = sys.argv[1]
    redisIp = sys.argv[2]
    print ('taskId: ', taskId)
    print ('redisIp: ', redisIp)

    # sid = redis.StrictRedis(host="172.23.27.47", port = 6379, db=0)
    sid = redis.StrictRedis(host=redisIp, port = 6379, db=0)
    print('redis连接成功')

    # taskId = os.environ.get("TASK_ID")
    self_index = taskId
    print("task ID is:", self_index)

    self_ip = get_host_ip()
    print("task ID :", taskId , ' ip地址为 :', self_ip)
    self_ip_json = json.dumps(self_ip)
    sid.set(self_index, self_ip_json)

    dag_map = sid.get('dag_map')
    dag_map = json.loads(dag_map)
    self_map = dag_map[self_index]
    print('获得依赖关系：', self_map)
    # get the ips of children tasks
    children_tasks = self_map[1]
    children_ips = [None]*len(children_tasks)

    # build the bind for getting the end signal form task e
    # tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # tcp_server_socket.bind((self_ip, 7070))
    # tcp_server_socket.listen(1)


    # for i in range(len(children_tasks)):

    #     children_ips[i] = json.loads(sid.get(children_tasks[i]))

    # print("type: ", type(children_ips[0]))
    # print("children ips: ", children_ips)

        # get the parent tasks
    inputData['startTask'] = 'start'

    outputData = TaskProcessFunction(inputData)
        
    output = json.dumps(outputData)
    # sid.set(taskId, output)
    # t1 = time.time()
        # record the current time, microseconds
    startTime = int(time.time()*1000000)
    sid.set('startTime', startTime)
    
    for index, child in enumerate(children_tasks):

        print("保存第",str(index),"个数据")
        #client_for_child(child, output[index])
        saveKey = self_index + 'to' + child
        print("saveKey: ", saveKey)
        sid.set(saveKey, output)

        print('保存 output_data to ：', saveKey)
        print("------------------------")

    # i = 0
    # t1 = time.time()
    # for child in children_ips:
        
    #     print("发送第",str(i+1),"个数据")
    #     client_for_child(child, output[i])
    #     print('发送 output_data[',str(i+1) , ']至', child)
    #     print("------------------------")
    #     i = i + 1


    # write into redis
    #print('startTime: ', sid.get('startTime'))

    # print('等待终止信息')
    # new_client_socket, client_addr = tcp_server_socket.accept()
    # end_signal = new_client_socket.recv(1024)
    # new_client_socket.send(end_signal)
    # end_time = time.time()
    # new_client_socket.close()


    print('Task0 is finished')
