import cv2
import glob
import sys
import asyncio
from concurrent.futures import ProcessPoolExecutor
sys.path.extend(["./model2","./model_1", "./aggregator"])
from model2 import model_landmark_client as modelsecond_cli
from model_1 import model_landmark_client as modelfirst_cli

print('running async for end user client')

def landmark_model(end_user_idata_path_):
   modelsecond_cli.run(end_user_idata_path_)


def age_gender_model(end_user_idata_path_):
    modelfirst_cli.run(end_user_idata_path_)

if __name__ == "__main__":
    # End user client
    end_user_idata_path = input("Please insert images directory path: ")
    ext = ['png', 'jpg', 'gif']    # Add image formats here
    files = []
    [files.extend(glob.glob(end_user_idata_path + '*.' + e)) for e in ext]

    for file in files:
        executor = ProcessPoolExecutor(2)
        loop = asyncio.new_event_loop()
        model_first_loop = loop.run_in_executor(executor, landmark_model(file))

        model_second_loop = loop.run_in_executor(executor, age_gender_model(file))

        loop.stop()
        loop.close()
    print("\nJob Done.\n")
