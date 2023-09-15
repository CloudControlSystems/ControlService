import numpy as np
from utils import TaskProcessFunction
import os, json, pickle, time, sys, redis, socket

"""
input: (Up, Yp, Uf, Yf) from task_0
output1: (O_i_1) to task_3
output1: (O_i_2) to task_4
......
output10: (O_i_10) to task_12
output11: (O_i) to task_20
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
#             continue


# class MyThread(threading.Thread):
#     def __init__(self, func, args):
#         super(MyThread, self).__init__()
#         self.func = func
#         self.args = args

#     def run(self):
#         self.result = self.func(*self.args)

#     def get_result(self):
#         try:
#             return self.result
#         except Exception:
#             return None

# def server_for_parent(self_ip, new_client_socket, client_addr):

#     #new_client_socket, client_addr = tcp_server_socket.accept()
#     #print("client_addr: ", client_addr)
#     recv_ip = client_addr[0]
#     #time2 = time.time()
#     #print("client_addr: ", client_addr, "after time: ", time2)
#     recv_data = b""
#     for j in range(400):  #(50,10000): 210

#         packet = new_client_socket.recv(2048)
#         recv_data += packet
#         #print("type: ", type(packet))
#         #print("scale: ", sys.getsizeof(packet), j)
#         #print("------------------------------")

#     #recv_data = new_client_socket.recv(20480)
#     #print("receive it")
#     print("total scale: ", sys.getsizeof(recv_data))
#     recv_data = pickle.loads(recv_data)
#     #print("type of recv", type(recv_data))
#     #back_data = pickle.dumps(1)
#     #new_client_socket.send(back_data)
#     new_client_socket.close()

#     return recv_ip, recv_data

# def keep_alive(t):

#     time.sleep(t)



if __name__ == '__main__':
    
    inputData = {}
    print('任务开始')
     # connect to the redis    
    #redisIp = os.environ.get("REDIS_IP")
    taskId = sys.argv[1]
    redisIp = sys.argv[2]
    print ('taskId: ', taskId)
    print ('redisIp: ', redisIp)

    # sid = redis.StrictRedis(host="172.23.27.47", port = 6379, db=0)
    sid = redis.StrictRedis(host=redisIp, port = 6379, db=0)
    print('redis连接成功')

    #taskId = os.environ.get("TASK_ID")
    self_index = taskId
    print("task ID is:", self_index)

    self_ip = get_host_ip()
    print("task ID :", taskId , ' ip地址为 :', self_ip)
    self_ip_json = json.dumps(self_ip)
    sid.set(taskId, self_ip_json)

    dag_map = sid.get('dag_map')
    dag_map = json.loads(dag_map)
    self_map = dag_map[self_index]
    print('获得自身关系：', self_map)

    children_tasks = self_map[1]
    children_ips = [None]*len(children_tasks)

    # build the bind for getting the end signal form task e
    # tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # tcp_server_socket.bind((self_ip, 7070))
    # tcp_server_socket.listen(1)

    #time.sleep(6)
    # for i in range(len(children_tasks)):

    #     children_ips[i] = json.loads(sid.get(children_tasks[i]))

    # print("type: ", type(children_ips[0]))
    # print("children ips: ", children_ips)
    parent_tasks = self_map[0]
    parent_ips = {}

    # i = 0
    for parent in parent_tasks:

        parent_ips[parent] = json.loads(sid.get(parent))

    recv_list = [None]*len(parent_tasks)
    recv_dic = {}

    print("parent ips: ", parent_ips)
    print("children tasks: ", children_tasks)
    print("children ips: ", children_ips)
    print("----------------------")
    print("----------------------")

    # receive the data
    print('开始从redis取数据')
    #pack_num = int(os.environ.get(PACK_NUM)) - 1
    i = 0

    # while True:

    #     print("准备接收第", str(i+1),"个数据")
    #     new_client_socket, client_addr = tcp_server_socket.accept()
    #     print("client_addr: ", client_addr)
    #     t = MyThread(server_for_parent, args = (self_ip, new_client_socket, client_addr))
    #     t.start()
    #     t.join()
    #     recv_res = t.get_result()
    #     #print("type: ", type(recv_res))
    #     #if not recv_res:
    #     #    pass
    #     #if len(recv_res) == 0:
    #     #    pass
    #     #print("recv_res")
    #     recv_ip = recv_res[0]
    #     recv_data = recv_res[1]
    #     recv_dic[recv_ip] = recv_data
    #     print('从',recv_ip,'接收到',np.shape(recv_data))
    #     print("接收完毕")
    #     print("----------------------")
    #     i = i + 1
    #     if i == len(parent_tasks):
    #         break

    # tcp_server_socket.close()

    # i = 0
    # for parent in parent_tasks:

    #     recv_list[i] = recv_dic[parent_ips[parent]]
    #     i = i + 1

    # output = TaskProcessFunction(recv_list)
    for index, parent in enumerate(parent_tasks):
        
        getKey = parent+ 'to' + self_index
        print("getKey: ", getKey)
        getData = sid.get(getKey)
        recv_list[index] = pickle.loads(getData)
        
    output = TaskProcessFunction(recv_list)
    # i = 0
    # for child in children_ips:
        
    #     print("发送第",str(i+1),"个数据")
    #     client_for_child(child, output[i])
    #     print('发送 output_data[',str(i+1) , ']至', child)
    #     print("------------------------")
    #     i = i + 1
    for index, child in enumerate(children_tasks):

        print("保存第",str(index),"个数据")
        #client_for_child(child, output[index])
        saveKey = self_index + 'to' + child
        print("saveKey: ", saveKey)
        output_data = pickle.dumps(output[index])

        sid.set(saveKey, output_data)

        print('保存 output_data to ：', saveKey)
        print("------------------------")

    # print('等待终止信息')
    # new_client_socket, client_addr = tcp_server_socket.accept()
    # end_signal = new_client_socket.recv(1024)
    # new_client_socket.send(end_signal)
    # end_time = time.time()
    # new_client_socket.close()

    print('Task4 is finished')
