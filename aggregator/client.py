import sys, os
script_directory = os.path.dirname(os.path.abspath(__file__))
wanted_dir='/'
for i in range(1,len(script_directory.split('/'))-1):
    wanted_dir += script_directory.split('/')[i]+'/'
sys.path.append(wanted_dir)
import datetime
import grpc
from aggregator import aggregator_pb2
from aggregator import aggregator_pb2_grpc
############ PARTA: LIBs
import numpy as np
from io import BytesIO
##############
def run(time_ ,frame_ ,redis_key_):
    
    with grpc.insecure_channel('localhost:60051') as channel:        
        stub = aggregator_pb2_grpc.AggregatorStub(channel)
        response = stub.SaveFaceAttributes(aggregator_pb2.FaceResult(time=time_,frame=frame_,redis_key=redis_key_))


''' 
#In case of stand alone run
if __name__ == '__main__':
    # Get user Input 
    idata_path = input("Please input img path: ")
    idata = cv2.imread(idata_path)
    ####np.array to bytes 
    np_bytes = BytesIO()
    np.save(np_bytes, idata, allow_pickle=True)
    idata_bytes = np_bytes.getvalue()
    #####################
    run(time_='0',frame_=idata_bytes,redis_key_='00')
'''
