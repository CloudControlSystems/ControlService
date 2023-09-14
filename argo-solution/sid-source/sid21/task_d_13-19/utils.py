import numpy as np
import scipy as sp
from scipy import linalg
from numpy import diag

def TaskProcessFunction(inputData):

    # get the data from recv_list
    data1 = inputData[0]
    data2 = inputData[1]

    u1 = np.matrix(data1[0])
    s1 = data1[1]
    v1 = np.matrix(data1[2])

    u2 = np.matrix(data2[0])
    s2 = data2[1]
    v2 = np.matrix(data2[2])
    
    s1 = diag(s1)
    s2 = diag(s2)

    u, s, v = Task_D(u1, s1, v1, u2, s2, v2)
    u = u.tolist()
    s = s.tolist()
    v = v.tolist()

    output = [u, s, v]; 
    outputData = [output]

    return outputData


def Task_D(u1, s1, v1, u2, s2, v2):

    #s1 = np.array(s1); s2 = np.array(s2)
    #print("type: ", type(s1), "type: ", type(s2))
    #s1 = diag(s1); s1 = diag(s1); 
    #print("shape: ", np.shape(s1), "shape: ", np.shape(s2))
    H = np.hstack((u1.dot(s1), u2.dot(s2)))
    #print("s1: ", np.shape(s1), "s2: ", np.shape(s2))
    #print("u1: ", np.shape(u1), "s2: ", np.shape(u2))
    print("H: ", np.shape(H))
    u, s, vhat = np.linalg.svd(H); v = vhat*linalg.block_diag(v1, v2)
    r = len(s); v = v[0:r, 0:r]
    return u, s, v