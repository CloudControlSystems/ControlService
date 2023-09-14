import numpy as np

def TaskProcessFunction(inputData):

    # get the data from recv_list
    Oi_block = np.matrix(inputData[0])

    # the body function
    u, s, v = Task_C(Oi_block)
    u = u.tolist(); s = s.tolist(); v = v.tolist()
    output = [u, s, v]
    outputData = [output]

    return outputData

def Task_C(Oi_block):
    
    u, s, v = np.linalg.svd(Oi_block); r = len(s);# s = np.diag(s)
    u1 = u[:, 0:r]; v1 = v[0:r, 0:r]; # s1 = s[0:r, 0:r]    
    return u1, s, v1
