import numpy as np

def TaskProcessFunction(inputData):

    # get the data
    Upp = np.matrix(inputData[0]); Ypp = np.matrix(inputData[1])
    Ufm = np.matrix(inputData[2]); Yfm = np.matrix(inputData[3])


    # the body function
    Oim1 = Task_B(Upp, Ypp, Ufm, Yfm)
    outputData = [Oim1]

    return outputData

def Task_B(Upp, Ypp, Ufm, Yfm):
    
    Wpp = np.vstack((Upp,Ypp)); Oim1 = compute_Ob(Yfm,Ufm,Wpp)
    return Oim1
      
def compute_Ob(A,B,C):
    temp1 = np.hstack((C.T,B.T)); temp2 = np.hstack((np.matmul(C,C.T),np.matmul(C,B.T)))
    temp3 = np.hstack((np.matmul(B,C.T),np.matmul(B,B.T))); temp4 = np.vstack((temp2,temp3))
    r,b = C.shape; temp4 = np.linalg.pinv(temp4); temp4 = temp4[:,:r]
    Ob = np.matmul(A,temp1); Ob = np.matmul(Ob,temp4); Ob = np.matmul(Ob,C)
    return Ob