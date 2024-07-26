import sys
import os
import threading
from threading import Semaphore
from multiprocessing.pool import ThreadPool
import requests
import time
import urllib3

with urllib3.warnings.catch_warnings():
   urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Retrieving the value of the "PATH" environment variable
# For use with Nomad (tbd)
# #path = os.environ["PATH"]
#print(path)

class results:
  client_errors = 0
  server_errors = 0
  success = 0

class buildRequest:
    domain = str()
    url = str()
    use_fabio = {"X-Ads-Use-Fabio": "true"}
    headers = dict()

    def __init__(self, input_url, input_domain, input_fabio, input_headers):        
        if domain != "":
            self.headers.update({"Host": input_domain})
        self.url = input_url
        if input_fabio == True:
            self.headers.update(self.use_fabio)
        if input_headers != "":
            self.headers.update(input_headers)
    

def loop_requests(api_url, num_req) -> str:
    requests.packages.urllib3.disable_warnings()
    count = 0
    response = []
    #headers = {"X-Ads-Use-Fabio": "true","Host": "{domain}"}
    for n in range(num_req):
        count = count+1
        #print(new_request.url, new_request.headers)
        #send_request = requests.get(url="https://10.10.34.30/is-you-healthy", verify=False)
        send_request = requests.get(url=new_request.url,headers=new_request.headers,verify=False)
        #print(f"Completed {count} requests")
        #return response.json()
        response.append(send_request.status_code)
    #print(response)
    lock.acquire()
    result.client_errors = result.client_errors + response.count(429)
    result.server_errors = result.server_errors + response.count(503)
    result.success = result.success + response.count(200) 
    lock.release()
    return(count)

def concurrency(threads, api_url, num_req):
    thread_count = 0
    request_thread = []
    
    for n in range(threads):
        thread_count = thread_count+1
        request_thread.append(threading.Thread(target=loop_requests, args=(api_url,num_req)))


    [t.start() for t in request_thread]
    
    [t.join() for t in request_thread]

    print("Completed all threads")


#square_thread = threading.Thread(target=calc_square, args=(numbers,))
#cube_thread = threading.Thread(target=calc_cube, args=(numbers,))

##square_thread.start()
#cube_thread.start()



api_url = str(input("URL to test against? "))
domain = str(input("Domain to try against? "))
total_req = int(input("How many total requests? "))
threads = int(input("How many parallel requests? "))
headers = dict()

new_request = buildRequest(api_url, domain, True, headers)

start_time = time.time()

# Make sure we don't divide by 0, and don't do crazy threading numbers
if threads == 0:
    threads = 1
elif threads > 100:
    threads = 100

# If we accidentally set a low total request number, set the threads to match
# This is to avoid a 0 count
if threads > total_req:
    threads = total_req

# initialize the class
result = results()

# Generate a semaphore lock
global lock
lock = Semaphore()

req_per_thread = total_req//threads
concurrency(threads, api_url, req_per_thread)

print(f"429 responses: {result.client_errors}\n503 responses: {result.server_errors}\n200 responses: {result.success}")

print("--- %s seconds ---" % (time.time() - start_time))



#+-------------+
#| download_id |
#+-------------+
#|    83854930 |
#|    84975844 |
#|    85036615 |
#|    85282873 |
#|    85655167 |
#|    86200309 |
#|    86550799 |
#|    88584562 |
#|    89873794 |
#|    90821941 |
#|    91121749 |
#|    91121752 |
#+-------------+
#(83854930,84975844,85036615,85282873,85655167,86200309,86550799,88584562,89873794,90821941,91121749,91121752)