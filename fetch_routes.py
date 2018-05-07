import urllib2
import sys
import json

def fetch_result(url):
    count = 0
    while True:
        try:
            #fetch result from route json#
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            json_response = json.load(response)
            
            if 'error' in json_response:
                print "error in respons: " + json_response['error']
                print "retry after 5 seconds"
                time.sleep(5)
            else:
                return json_response
        except:
            #state how many loops you want. In this example 10
            if count < 10:
                count += 1
                print "failed to fetch respons -- retry after 5 seconds: " + str(count)
                time.sleep(5)
            else:
                print "failed to fetch respons"
                return {'result': None}


key = 'xxxxx'

params = [key]

#get token

url = 'http://api.routeyou.com/2.0/json/Session?id=1&method=start&params=' + json.dumps(params)

token = fetch_result(url)['result']

#search
sort = 'id ASC'
limit = 100
conditions = {'owner.id': 102763, 'id.min':0}
params = [conditions, sort, limit]

finished = False

while True:
    url = 'http://api.routeyou.com/2.0/json/Route/' + token + '?id=1&method=searchAdvanced&params=' + json.dumps(params)
    response = fetch_result(url)
    for route in response['result']['routes']:
        #do something with the route
        print route['id']
        lastRouteId = route['id']
    
    conditions['id.min'] = lastRouteId
        
    if len(response['result']['routes']) < limit:
        break
    