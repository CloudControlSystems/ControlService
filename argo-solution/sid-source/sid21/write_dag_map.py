#from rediscluster import RedisCluster
import json, redis

sid = redis.StrictRedis(host="172.16.96.100", port = 6379, db=0)
#nodes = [{"host": "192.168.1.23", "port": "7133"}]
#sid = RedisCluster(startup_nodes=nodes, decode_responses=True)

dag_map = {}


dag_map['task0'] = [['null'], ['task1', 'task2']]
dag_map['task1'] = [['task0'], ['task3', 'task4', 'task5', 'task6', 'task7', 'task8', 'task9', 'task10', 'task11', 'task12', 'task20']]
dag_map['task2'] = [['task0'], ['task20']]

dag_map['task3'] = [['task1'], ['task13']]
dag_map['task4'] = [['task1'], ['task13']]
dag_map['task5'] = [['task1'], ['task14']]
dag_map['task6'] = [['task1'], ['task14']]
dag_map['task7'] = [['task1'], ['task15']]
dag_map['task8'] = [['task1'], ['task15']]
dag_map['task9'] = [['task1'], ['task16']]
dag_map['task10'] = [['task1'], ['task16']]
dag_map['task11'] = [['task1'], ['task17']]
dag_map['task12'] = [['task1'], ['task17']]

dag_map['task13'] = [['task3', 'task4'], ['task18']]
dag_map['task14'] = [['task5', 'task6'], ['task18']]
dag_map['task15'] = [['task7', 'task8'], ['task19']]
dag_map['task16'] = [['task9', 'task10'], ['task19']]
dag_map['task17'] = [['task11', 'task12'], ['task20']]
dag_map['task18'] = [['task13', 'task14'], ['task20']]
dag_map['task19'] = [['task15', 'task16'], ['task20']]

dag_map['task20'] = [['task1', 'task2', 'task17', 'task18', 'task19'], ['null']]

dag_map = json.dumps(dag_map)

sid.set('dag_map', dag_map)

