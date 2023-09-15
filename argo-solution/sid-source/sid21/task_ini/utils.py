import numpy as np
import os, json, redis
#from rediscluster import RedisCluster

"""
input: none
output1: (Up, Yp, Uf, Yf) to Task_1
output2: (Upp, Ypp, Ufm, Yfm) to Task_2
output3: (Ui, Yi, l) to Task_20 (*)
"""

def Run_Task_initial():

    #nodes = [{"host": "192.168.1.23", "port": "7133"}]
    #sid = RedisCluster(startup_nodes=nodes, decode_responses=True)
    # redisIp = os.environ.get("REDIS_IP")
    # sid = redis.StrictRedis(host=redisIp, port = 6379, db=0)
    sid = redis.StrictRedis(host="172.16.96.100", port = 6379, db=0)
    
    print('redis连接成功')

    #Up, Yp, Uf, Yf, Upp, Ypp, Ufm, Yfm, Ui, Yi, l  = Task_initial()
    Yp, Yf, Ypp, Yfm, Up, Uf, Upp, Ufm, Ui, Yi, l = Task_initial()

    print("Up, Yp, Uf, Yf: ", np.shape(Up), np.shape(Yp), np.shape(Uf), np.shape(Yf))
    print("Upp, Ypp, Ufm, Yfm: ", np.shape(Upp), np.shape(Ypp), np.shape(Ufm), np.shape(Yfm))

    output1 = json.dumps([Up.tolist(), Yp.tolist(), Uf.tolist(), Yf.tolist()])
    output2 = json.dumps([Upp.tolist(), Ypp.tolist(), Ufm.tolist(), Yfm.tolist()])
    output3 = json.dumps([Ui.tolist(), Yi.tolist(), l.tolist()])

    sid.set('Task0toTask1', output1); sid.set('Task0toTask2', output2); sid.set('Task0toTask20', output3)


def Task_initial():
    
    A=np.matrix([[2,-1],[1,0]]); B=np.matrix([[1],[0]]); C=np.matrix([[0.00014,0.00014]]); D = np.matrix([[0]])
    N = 20; j = 1000; steps = 2*N+j-1
    
    mv, pos = ball_bean_system_simluate(A,B,C,D,steps)
    Yp, Yf, Ypp, Yfm, Up, Uf, Upp, Ufm, Ui, Yi, l = output_Hankel(mv,pos,N,j)
    
    return Yp, Yf, Ypp, Yfm, Up, Uf, Upp, Ufm, Ui, Yi, l
    
    
def output_Hankel(u,y,N,j):
    
    y = list2mat(y); l = np.matrix(y.shape[0]); Ui = u[:,N:N+j]; Yi = y[:,N:N+j]
    Yp, Yf, Ypp, Yfm = create_Hankel(y,N,j); Up, Uf, Upp, Ufm = create_Hankel(u,N,j)
    
    return Yp, Yf, Ypp, Yfm, Up, Uf, Upp, Ufm, Ui, Yi, l
    
def list2mat(A):
    m = A[0].shape[0]; n = A[0].shape[1]; p = len(A); B = np.matrix(np.zeros([m,n*p]))
    for i in range(p):
        B[:,i*n:(i+1)*n] = A[i]
    return B

def create_Hankel(data,N,j): 
    p = data.shape[0]; H = np.matrix(np.zeros([2*N*p,j]))
    for i in range(2*N):
        for t in range(j):
            H[i*p:(i+1)*p,t] = data[:,i+t]
    Hp = H[:N,:]; Hf = H[N:2*N,:]; Hpp = H[:N+1,:]; Hfm = H[N+1:2*N,:];
    return Hp, Hf, Hpp, Hfm

def ball_bean_system_simluate(A,B,C,D,steps):
    
    #ball-beam system's state-space model
    A=np.matrix([[2,-1],[1,0]]); B=np.matrix([[1],[0]]); C=np.matrix([[0.00014,0.00014]]); D = np.matrix([[0]])
    #parameters
    x = np.zeros([2,1]); y = np.zeros([1,1])
    #pid parameters
    Kp = 9; Ki = 3; Kd = 9; a = Kp+Ki*0.02+Kd/0.02; b = Kp+2*Kd/0.02; c = Kd/0.02;
    ex = 0; es = 0; exx = 0; ux = 0; mv = []; pos = []; ref = []; runtime = []; u = 0; r=0.2;
    
    for i in range(steps):
        runtime.append(0.02*i)
        if u >= 0.2:
            u = 0.2
        if u <= -0.2:
            u = -0.2
        x = A*x+B*u; y = C*x+D*u
        if y >= 0.4:
            y = 0.4
        if y < -0.4:
            y = -0.4
        mv.append(u); pos.append(y); ref.append(r); es = r- float(y); u=ux+a*es-b*ex+c*exx; ux=u; exx=ex; ex=es
    mv = np.matrix(mv); pos = np.transpose(list2mat(pos))

    return mv, pos
