# Deepface_grpc
Facial attributes exteraction using NoSQL db and grpc and two deepface models.

## Description

Using grpc and NoSQL, you could use AI models to run them async (using asyncio) to handle the whole process of AI predictions and saving data from the databse using an aggregator.

## Getting Started

### Dependencies and Installing

* OS (Operating system) is ubuntu
* change your working directory to here so that you could see models, and aggregator directories. ex: ```cd .```
* Python version is 3.12.3 and pip version is 24.0
* install tmux in your ubuntu
* ```pip install redis```
* ```pip install "redis[hiredis]"```
* ```sudo apt-get install redis-server```
* ```pip install -r ./requirements.txt```
* download the redis json module docker file from [Here](https://uploadkon.ir/uploads/08e004_25redislabs-rejson.rar). Extract the file. open a tmux session and let's call it tmux_redis. if docker did not run because the redis is not started, initialize redis server. run these commands in tmux_redis: 1- ```docker load -i /path/to/redislabs_rejson.tar```; 2- ```docker run --name=redis-devel --publish=6379:6379 --hostname=redis --restart=on-failure --detach redislabs/rejson```

* In case of using the ./model2/model_landmark_cal.proto file add the below code to the top of the "./model2/model_landmark_cal_pb2_grpc.py":
```
import sys, os
script_directory = os.path.dirname(os.path.abspath(__file__))
wanted_dir='/'
for i in range(1,len(script_directory.split('/'))-1):
    wanted_dir += script_directory.split('/')[i]+'/'
sys.path.append(wanted_dir)
```

* In case of using the ./model_1/model_landmark_cal.proto file add the below code to the top of the "./model_1/model_landmark_cal_pb22_grpc.py":
```
import sys, os
script_directory = os.path.dirname(os.path.abspath(__file__))
wanted_dir='/'
for i in range(1,len(script_directory.split('/'))-1):
    wanted_dir += script_directory.split('/')[i]+'/'
sys.path.append(wanted_dir)
```

* In case of using the ./aggregator/aggregator.proto file add the below code to the top of the "./aggregator/aggregator_pb2_grpc.py":
```
import sys, os
script_directory = os.path.dirname(os.path.abspath(__file__))
wanted_dir='/'
for i in range(1,len(script_directory.split('/'))):
    wanted_dir += script_directory.split('/')[i]+'/'
sys.path.append(wanted_dir)
```



### Executing program

#### How to run the program
###### Step-by-step bullets

* open another tmux session call it tmux_model_1; then run: ```python3 ./model_1/model_landmark_server.py```
* open another tmux session call it tmux_model2; then run: ```python3 ./model2/model_landmark_server.py```
* open another tmux session call it tmux_aggregator; then run: ```python3 ./aggregator/server.py```
* open another tmux session call it tmux_end_user_client; then run: ```python3 ./async.py```
* Give the address of a images directory and be sure to have "/" at the end of the address.


## Author

Contributors names and contact info

Ali khazaeinezhad

## Version History
* 0.1
    * Initial Release
