import sys, os
script_directory = os.path.dirname(os.path.abspath(__file__))
wanted_dir='/'
for i in range(1,len(script_directory.split('/'))-1):
    wanted_dir += script_directory.split('/')[i]+'/'
sys.path.append(wanted_dir)
import grpc
from model2 import model_landmark_cal_pb2
from model2 import model_landmark_cal_pb2_grpc

############ PARTA: LIBs
import cv2
import numpy as np
from io import BytesIO
##############
def run(img):
    if type(img)==str:
      # Read user Input 
      idata_path = img
      idata = cv2.imread(idata_path)
      ####np.array to bytes 
      np_bytes = BytesIO()
      np.save(np_bytes, idata, allow_pickle=True)
      idata_bytes = np_bytes.getvalue()  
      ###############
      with grpc.insecure_channel('localhost:50051') as channel:
          stub = model_landmark_cal_pb2_grpc.Model_Landmark_CalculatorStub(channel)
          
          response = stub.Add(model_landmark_cal_pb2.Model_Landmark_Input_img(model_landmark_idata=idata_bytes))
          
      ###############

    if __name__=='__main__':
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = model_landmark_cal_pb2_grpc.Model_Landmark_CalculatorStub(channel)
            response = stub.Add(model_landmark_cal_pb2.Model_Landmark_Input_img(model_landmark_idata=img))

          
if __name__ == '__main__':
    # Get user Input 
    idata_path = input("Please input img full path: ")
    idata = cv2.imread(idata_path)
    ####np.array to bytes 
    np_bytes = BytesIO()
    np.save(np_bytes, idata, allow_pickle=True)
    idata_bytes = np_bytes.getvalue()
    #####################
    run(idata_bytes)
