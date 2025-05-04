import sys, os
script_directory = os.path.dirname(os.path.abspath(__file__))
wanted_dir='/'
for i in range(1,len(script_directory.split('/'))-1):
    wanted_dir += script_directory.split('/')[i]+'/'
sys.path.append(wanted_dir)

import grpc
from model_1 import model_landmark_cal_pb22
from model_1 import model_landmark_cal_pb22_grpc

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
      with grpc.insecure_channel('localhost:40051') as channel:
          stub = model_landmark_cal_pb22_grpc.Model_Landmark2_CalculatorStub(channel)
          response = stub.Add_second(model_landmark_cal_pb22.Model_Landmark2_Input_img(model_landmark2_idata=idata_bytes))
      ###############

    if __name__=='__main__':
        with grpc.insecure_channel('localhost:40051') as channel:
            stub = model_landmark_cal_pb22_grpc.Model_Landmark2_CalculatorStub(channel)
            response = stub.Add(model_landmark_cal_pb22.Model_Landmark2_Input_img(model_landmark2_idata=img))

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
