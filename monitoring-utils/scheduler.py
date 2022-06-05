import schedule
import time
import requests
from pymongo import MongoClient
from datetime import datetime

try:
   mongo_client = MongoClient(host='20.84.71.186', port=27017, username='mongoadmin', password='secret')
   db = mongo_client['orbit']
   collection = db['metrics_10']
   print('conectou')
except:
   print('nao conectou')


def send_to_verify(data):
   availability_request = 'http://localhost:5004/'
   requests.post(availability_request, json=data)

def fetch_metrics():

   ###TEMPO DE RESPOSTA
   time_response_request='http://localhost:9090/api/v1/query?query=irate(http_server_requests_seconds_sum{instance="localhost:8080", uri!~".*actuator.*"}[1m]) / irate(http_server_requests_seconds_count{instance="localhost:8080", uri!~".*actuator.*"}[1m])'
   time_response_register=requests.get(time_response_request).json()
   

   ##USO DE CPU
   cpu_usage_request='http://localhost:9090/api/v1/query?query=system_cpu_usage{instance="localhost:8080"}'
   cpu_usage_register=requests.get(cpu_usage_request).json()

   ###USO TOTAL DE MEMÓRIA
   memory_used_request='http://localhost:9090/api/v1/query?query=sum(jvm_memory_used_bytes{instance="localhost:8080"})*100/sum(jvm_memory_max_bytes{instance="localhost:8080"})'
   memory_used_register=requests.get(memory_used_request).json()

   ###USO DE MEMÓRIA HEAP
   heap_used_request='http://localhost:9090/api/v1/query?query=sum(jvm_memory_used_bytes{instance="localhost:8080", area="heap"})*100/sum(jvm_memory_max_bytes{instance="localhost:8080", area="heap"})'
   heap_used_register=requests.get(heap_used_request).json()

   ###USO DE MEMÓRIA NON-HEAP
   non_heap_used_request='http://localhost:9090/api/v1/query?query=sum(jvm_memory_used_bytes{instance="localhost:8080", area="nonheap"})*100/sum(jvm_memory_max_bytes{instance="localhost:8080", area="nonheap"})'
   non_heap_used_register=requests.get(non_heap_used_request).json()

   trrg_ts = 0
   trrg = 0
   trrp_ts = 0
   trrp = 0
   available = 1

   for r in time_response_register['data']['result']:
      if r['metric']['uri'] == '/users' and r['metric']['method'] == 'GET':
         trrg_ts = r['value'][0]
         trrg = r['value'][1]
         if trrg == 'NaN':
            trrg = 0
      if r['metric']['uri'] == '/users' and r['metric']['method'] == 'POST':
         trrp_ts = r['value'][0]
         trrp = r['value'][1]
         if trrp == 'NaN':
            trrp = 0
      if '50' in r['metric']['status'] or '40' in r['metric']['status']:
         available = 0
   
   if len(cpu_usage_register['data']['result']) > 0:
      cpuu = cpu_usage_register['data']['result'][0]['value'][1]
   else:
      cpuu = 0

   if float(trrp) > 20 or float(trrg) > 40:
      available = 0

   register = {
      "time_response_get": float(trrg),
      "time_response_post": float(trrp),
      "cpu_usage": float(cpuu),
      "memory_used": float(memory_used_register['data']['result'][0]['value'][1] if len(memory_used_register['data']['result']) > 0 else 0),
      "heap_used": float(heap_used_register['data']['result'][0]['value'][1] if len(heap_used_register['data']['result']) > 0 else 0),
      "non_heap_used": float(non_heap_used_register['data']['result'][0]['value'][1] if len(non_heap_used_register['data']['result']) > 0 else 0),
      "time": non_heap_used_register['data']['result'][0]['value'][0] if len(non_heap_used_register['data']['result']) > 0 else datetime.now().timestamp(),
      "available": available
   }
   
   print(register)
   send_to_verify(register)
   a = collection.insert_one(register)
   print(a.inserted_id)

   

schedule.every(30).seconds.do(fetch_metrics)


while True:
   schedule.run_pending()
   time.sleep(1)
