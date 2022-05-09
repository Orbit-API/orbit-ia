import schedule
import time
import requests
from pymongo import MongoClient
from datetime import datetime

try:
   # con = 'mongodb+srv://mongoadmin:secret@20.84.71.186:27017/orbit'
   mongo_client = MongoClient(host='20.84.71.186', port=27017, username='mongoadmin', password='secret')
   db = mongo_client['orbit']
   collection = db['metrics']
   print('conectou')

except:
   print('nao conectou')


def fetch_metrics():

   ###TEMPO DE RESPOSTA
   time_response_request='http://20.106.206.173:9090/api/v1/query?query=irate(http_server_requests_seconds_sum{instance="20.106.206.173:8080", method="GET", exception="None", uri!~".*actuator.*"}[1m]) / irate(http_server_requests_seconds_count{instance="20.106.206.173:8080", exception="None", method="GET", uri!~".*actuator.*"}[1m])'
   time_response_register=requests.get(time_response_request).json()
   

   ##USO DE CPU
   cpu_usage_request='http://20.106.206.173:9090/api/v1/query?query=system_cpu_usage{instance="20.106.206.173:8080"}'
   cpu_usage_register=requests.get(cpu_usage_request).json()

   ###USO TOTAL DE MEMÓRIA
   memory_used_request='http://20.106.206.173:9090/api/v1/query?query=sum(jvm_memory_used_bytes{instance="20.106.206.173:8080"})*100/sum(jvm_memory_max_bytes{instance="20.106.206.173:8080"})'
   memory_used_register=requests.get(memory_used_request).json()

   ###USO DE MEMÓRIA HEAP
   heap_used_request='http://20.106.206.173:9090/api/v1/query?query=sum(jvm_memory_used_bytes{instance="20.106.206.173:8080", area="heap"})*100/sum(jvm_memory_max_bytes{instance="20.106.206.173:8080", area="heap"})'
   heap_used_register=requests.get(heap_used_request).json()

   ###USO DE MEMÓRIA NON-HEAP
   non_heap_used_request='http://20.106.206.173:9090/api/v1/query?query=sum(jvm_memory_used_bytes{instance="20.106.206.173:8080", area="nonheap"})*100/sum(jvm_memory_max_bytes{instance="20.106.206.173:8080", area="nonheap"})'
   non_heap_used_register=requests.get(non_heap_used_request).json()

   trr_ts = 0
   trr = 0
   for r in time_response_register['data']['result']:
      if r['metric']['uri'] == '/users':
         trr_ts = r['value'][0]
         trr = r['value'][1]


   mean_timestamp = (trr_ts + cpu_usage_register['data']['result'][0]['value'][0] + memory_used_register['data']['result'][0]['value'][0] + heap_used_register['data']['result'][0]['value'][0] + non_heap_used_register['data']['result'][0]['value'][0]) / 5

   register = {
      "time_response": trr,
      "cpu_usage": cpu_usage_register['data']['result'][0]['value'][1],
      "memory_used": memory_used_register['data']['result'][0]['value'][1],
      "heap_used": heap_used_register['data']['result'][0]['value'][1],
      "non_heap_used": non_heap_used_register['data']['result'][0]['value'][1],
      "time": datetime.fromtimestamp(mean_timestamp).isoformat()
   }

   print(register)
   # a = collection.insert_one(register)
   # print(a.inserted_id)

schedule.every(4).seconds.do(fetch_metrics)


while True:
   schedule.run_pending()
   time.sleep(1)
