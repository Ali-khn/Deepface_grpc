import os
import grpc
import cv2
from concurrent import futures
import aggregator_pb2
import aggregator_pb2_grpc
import json
import numpy as np
from io import BytesIO
################
import redis
from redis.commands.json.path import Path
import redis.commands.search.aggregation as aggregations
import redis.commands.search.reducers as reducers
from redis.commands.search.field import TextField, NumericField, TagField
from redis.commands.search.index_definition import IndexDefinition, IndexType
from redis.commands.search.query import NumericFilter, Query
r = redis.Redis(host="0.0.0.0", port=6379, db=0, decode_responses=True)
################

class AggregatorServicer(aggregator_pb2_grpc.AggregatorServicer):
    def datalogger(self, time_, frame_, redis_key_):

        ####From bytes to array
        nd_array_idata_loaded_bytes =BytesIO(frame_)
        frame_ = np.load(nd_array_idata_loaded_bytes,allow_pickle=True)
        ####End
        ResultedData = { f"Redis_key: {redis_key_}":
                          {
                          "time":time_,
                          "attributes":r.json().get(f"{redis_key_}"),
                           },
                        }
        try:
            os.mkdir(f"./{redis_key_}")
        except:
            print(f"""Could not create folder \"./{redis_key_}\"! It may already exists!""")

        with open(f'./{redis_key_}/{redis_key_}_data.json', 'w') as fp:
            json.dump(ResultedData, fp)
        
        cv2.imwrite(f"./{redis_key_}/{redis_key_}.jpeg",frame_)
        
        return time_,frame_,redis_key_

    def SaveFaceAttributes(self, request, context):
        final1,final2,final3 = AggregatorServicer().datalogger(time_ = request.time,
                                                               frame_ = request.frame,
                                                               redis_key_ = request.redis_key)
        return aggregator_pb2.FaceResultResponse(response=True) # Will be printed on the AI model server stdout

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    aggregator_pb2_grpc.add_AggregatorServicer_to_server(AggregatorServicer(), server)
    server.add_insecure_port('[::]:60051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
