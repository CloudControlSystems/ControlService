#from rediscluster import RedisCluster
import json, redis

sid = redis.StrictRedis(host="172.16.96.100", port = 6379, db=0)
#nodes = [{"host": "192.168.1.23", "port": "7133"}]
#sid = RedisCluster(startup_nodes=nodes, decode_responses=True)

dag_map = {}


dag_map['task0'] = [['null'], ['task1', 'task2']]
dag_map['task1'] = [['task0'], ['task3', 'task4', 'task5']]
dag_map['task2'] = [['task0'], ['task5']]

dag_map['task3'] = [['task1'], ['task5']]
dag_map['task4'] = [['task1'], ['task5']]

dag_map['task5'] = [['task1', 'task2', 'task3', 'task4'], ['null']]

dag_map = json.dumps(dag_map)

sid.set('dag_map', dag_map)

