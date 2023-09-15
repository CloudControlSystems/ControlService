import numpy as np
from numpy import diag
from scipy import signal, linalg

def TaskProcessFunction(inputDataRedis, inputData):

    # get the data
    Ui = np.matrix(inputDataRedis[0]); Yi = np.matrix(inputDataRedis[1]); l = np.matrix(inputDataRedis[2])
    Oi = inputData[0]; Oim1 = inputData[1]
    s1 = inputData[2][1]; v1 = np.matrix(inputData[2][2]); u1 = np.matrix(inputData[2][0])
    s2 = inputData[3][1]; v2 = np.matrix(inputData[3][2]); u2 = np.matrix(inputData[3][0])
    s1 = diag(s1); s2 = diag(s2)

    # the body function
    Ahat, Bhat, Chat, Dhat = Task_E(Ui, Yi, l, Oi, Oim1, u1, s1, v1, u2, s2, v2)
    outputData = [Ahat, Bhat, Chat, Dhat]

    return outputData

def Task_E(Ui, Yi, l, Oi, Oim1, u1, s1, v1, u2, s2, v2):
    # print('Ui: ', Ui)
    # print('Yi: ', Yi)
    # print('l: ', l)
    # print('Oi: ', Oi)
    # print('Oim1: ', Oim1)
    # print('s1: ', s1)
    # print('v1: ', v1)
    # print('u2: ', u2)
    # print('s2: ', s2)
    # print('v2: ', v2)
    # deal with l
    l = int(l)
    # obtain Gamma and order
    Gamma_i, Gamma_im1, n = compute_Gamma_and_order(u1, s1, v1, u2, s2, v2, l)
    # compute the emstimated state sequence
    Xihat, Xip1hat = compute_Xs(Gamma_i,Gamma_im1,Oi,Oim1)
    # estimeate the system matrices
    Ahat, Bhat, Chat, Dhat = estimate_parameters(Xihat,Xip1hat,Yi,Ui,n,l)
    Ahat, Bhat, Chat, Dhat = system_matrices_simplify(Ahat, Bhat, Chat, Dhat)
    
    return Ahat, Bhat, Chat, Dhat

def Task_D(u1, s1, v1, u2, s2, v2):
    
    H = np.hstack((u1.dot(s1), u2.dot(s2)))
    u, s, vhat = np.linalg.svd(H); v = vhat*linalg.block_diag(v1, v2)
    r = len(s); v = v[0:r, 0:r]; # s = diag(s)
    #print("s: ", type(s), np.shape(s))
    return u, s, v    

def compute_Gamma_and_order(u1, s1, v1, u2, s2, v2, l):
    
    #U, S, VT = merge_svd_result(u1, s1, v1, u2, s2, v2, u3, s3, v3)
    U, S, VT = Task_D(u1, s1, v1, u2, s2, v2)
    print("U: ", np.shape(U), "S: ", np.shape(S), "VT: ", np.shape(VT))
    n = 2; S1 = S[:n]
    print("S1: ", np.shape(S1))
    Gamma_i = U[:,:n].dot(np.diag(np.sqrt(S1))); Gamma_im1 = Gamma_i[:-l] # cut last l rows
    return Gamma_i, Gamma_im1, n

def compute_Xs(Gamma_i,Gamma_im1,Oi,Oim1):
    print("Gamma_i: ", np.shape(Gamma_i), "Oi: ", np.shape(Oi))
    print("Gamma_im1: ", np.shape(Gamma_im1), "Oim1: ", np.shape(Oim1))
    Xihat = np.linalg.pinv(Gamma_i).dot(Oi); 
    Xip1hat = np.linalg.pinv(Gamma_im1).dot(Oim1)
    return Xihat, Xip1hat

def estimate_parameters(Xihat,Xip1hat,Yi,Ui,n,l):
    
    Left = np.vstack((Xip1hat,Yi)); Right = np.vstack((Xihat,Ui)); paras = Left.dot(np.linalg.pinv(Right))
    Ahat = paras[:n,:n]; Bhat = paras[:n,n:]; Chat = paras[n:n+l,:n]; Dhat = paras[n:n+l,n:]
    return Ahat, Bhat, Chat, Dhat

def system_matrices_simplify(A,B,C,D):
    n1,s1 = signal.ss2tf(A,B,C,D)
    n2 = (np.hstack((np.array([0]), n1[0][0:len(n1[0])-1]))).reshape([1,3])
    A1,B1,C1,D1 = signal.tf2ss(n2,s1)
    return A1,B1,C1,D1