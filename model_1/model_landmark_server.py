import sys, os, hashlib
script_directory = os.path.dirname(os.path.abspath(__file__))
wanted_dir='/'
for i in range(1,len(script_directory.split('/'))-1):
    wanted_dir += script_directory.split('/')[i]+'/'
sys.path.append(wanted_dir)

import datetime
import grpc
from concurrent import futures
from model_1 import model_landmark_cal_pb22
from model_1 import model_landmark_cal_pb22_grpc

################PARTA: LIBs 
import numpy as np
from io import BytesIO
from deepface import DeepFace
################
from aggregator import client as aggregator_client
from aggregator import aggregator_pb2
from aggregator import aggregator_pb2_grpc
#################
import redis
from redis.commands.json.path import Path
import redis.commands.search.aggregation as aggregations
import redis.commands.search.reducers as reducers
from redis.commands.search.field import TextField, NumericField, TagField
from redis.commands.search.index_definition import IndexDefinition, IndexType
from redis.commands.search.query import NumericFilter, Query
#################
r = redis.Redis(host="0.0.0.0", port=6379, db=0, decode_responses=True)

class Model_Landmark2_CalculatorServicer(model_landmark_cal_pb22_grpc.Model_Landmark2_CalculatorServicer):
    def DeepFACE(self, ImgBytes):
        # From bytes to array
        nd_array_idata_loaded_bytes =BytesIO(ImgBytes)
        frame = np.load(nd_array_idata_loaded_bytes,allow_pickle=True)
        # End
        backends = [
    'opencv', 'ssd', 'dlib', 'mtcnn', 'fastmtcnn',
    'retinaface', 'mediapipe', 'yolov8', 'yolov11s',
    'yolov11n', 'yolov11m', 'yunet', 'centerface',
]
        detector = backends[5]
        align = True
        obj = DeepFace.analyze(img_path=frame, detector_backend = detector, align = align,actions=['age','gender'])
        return ImgBytes, str(obj) #obj

    def Add_second(self, request, context):
        
        imgBytes, final = Model_Landmark2_CalculatorServicer().DeepFACE(request.model_landmark2_idata)
        ################### CLIENT % Redis
        """
        redis_data = {
                      'landmark-model_result': final,
                      }
        """
       
        if r.json().get(str(hashlib.sha256(imgBytes).hexdigest()))!=None: #If the other model has finished its job
            redis_data = r.json().get(str(hashlib.sha256(imgBytes).hexdigest()))
            redis_data["landmark-model_result"]=final          
            r.json().set(str(hashlib.sha256(imgBytes).hexdigest()), Path.root_path(), redis_data)
           
            aggregator_client.run(time_=str(datetime.datetime.now()),
                                  frame_= imgBytes,
                                  redis_key_=str(hashlib.sha256(imgBytes).hexdigest()),
                                 )
        else: #else
            redis_data = {
                      "landmark2-model_result":final,
                      }
            r.json().set(str(hashlib.sha256(imgBytes).hexdigest()), Path.root_path(), redis_data)
        
        ################## END
        return model_landmark_cal_pb22.Model_Landmark2_Output_img(model_landmark2_odata=final) #The odata would be printed on the stdout of the first client

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    model_landmark_cal_pb22_grpc.add_Model_Landmark2_CalculatorServicer_to_server(Model_Landmark2_CalculatorServicer(), server)
    server.add_insecure_port('[::]:40051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
