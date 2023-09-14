import numpy as np

def TaskProcessFunction(inputData):

    # get the data
    Up = np.matrix(inputData[0]); Yp = np.matrix(inputData[1])
    Uf = np.matrix(inputData[2]); Yf = np.matrix(inputData[3])

    # the body function
    # print('Up: ', Up)
    # print('Yp: ', Yp)
    # print('Uf: ', Uf)
    # print('Yf: ', Yf)
    listBlock = Task_A(Up, Yp, Uf, Yf)

    outputData = listBlock

    return outputData

def Task_A(Up, Yp, Uf, Yf):
    
    col = 10000; Wp = np.vstack((Up,Yp))
    # print('Wp: ', Wp) 

    Oi = compute_Ob(Yf,Uf,Wp)
    # print('Oi: ', Oi) 

    list_block = selice_matrix(Oi,col)
    print("Oi: ", np.shape(Oi))
    list_block.append(Oi)
    
    return list_block
    
def compute_Ob(A,B,C):
    temp1 = np.hstack((C.T,B.T))
    # print('temp1: ', temp1)    
    temp2 = np.hstack((np.matmul(C, C.T), np.matmul(C, B.T)))
    #temp2 = np.hstack((C*C.T, C*B.T))
    # print('C.T: ', C.T) 
    # print('B.T: ', B.T) 

    #print('C*C.T: ', C*C.T)
    print('np.matmul(C,C.T): ', np.matmul(C, C.T))
    #print('np.matmul(C,B.T): ', np.matmul(C, B.T))
    # print('temp2: ', temp2)
    temp3 = np.hstack((np.matmul(B,C.T),np.matmul(B,B.T)))
    # print('temp3: ', temp3) 
    temp4 = np.vstack((temp2,temp3))
    # print('temp4: ', temp4)
    
    r,b = C.shape; temp4 = np.linalg.pinv(temp4); temp4 = temp4[:,:r]
    Ob = np.matmul(A,temp1); Ob = np.matmul(Ob,temp4); Ob = np.matmul(Ob,C)
    return Ob

def selice_matrix(A, col):
    
    Nc = round(np.shape(A)[1]/col + 0.45); list_block =[]
    for i in range(Nc):
        Ab = A[:,i*col:np.min((np.shape(A)[1],(i+1)*col))]
        list_block.append(Ab)
        
    return list_block

