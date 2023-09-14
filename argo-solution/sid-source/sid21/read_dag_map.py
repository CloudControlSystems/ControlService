import redis, json
#import numpy as np

sid = redis.StrictRedis(host="172.16.96.100", port = 6379, db=0)

dag_map = sid.get('dag_map')
dag_map = json.loads(dag_map)
print(dag_map)
# print(dag_map['task1'])
# print(dag_map['task2'])
# print(dag_map['task3'])
# print(dag_map['task4'])
# print(dag_map['task5'])

