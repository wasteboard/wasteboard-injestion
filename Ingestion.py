import time, datetime
import os
import requests
import json
import urllib

def pseudo_cron_job(get_from_url, push_to_url):
    sensor1 = 'b3054f1c-5f22-4ba4-a372-1e42049f8b9a'
    sensor2 = '6c205387-fba7-4e9f-bedd-4fdceb6c5eae'

    while True:

        headers_get = {'Accept': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJYQTBRaUczNl9rUEJMZUlubkpfVkhtMTd3b0ZwZVBGaG1XbDhnQU4ybUlZIn0.eyJqdGkiOiI4NzBlZWQwNi01ZDI4LTRkOGQtYWEyOC04YWI4NWE1NmVmMWYiLCJleHAiOjE0OTM3MjkwNTcsIm5iZiI6MCwiaWF0IjoxNDkzNDY5ODU3LCJpc3MiOiJodHRwczovL3Nzby5zdGVwaGVuLWdpYnNvbi5pb3RwZGV2LmNvbS9hdXRoL3JlYWxtcy9naWJib1N0YWNrQXByMjgiLCJhdWQiOiJhcGkiLCJzdWIiOiJjZmVhMjQyYy0yZjQ3LTQ3ZGUtYmJmNy03ZjlkOTU4NmE1MjEiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJhcGkiLCJhdXRoX3RpbWUiOjE0OTM0Njk4NTYsInNlc3Npb25fc3RhdGUiOiIxOWM0NjM0OC1iNmM4LTRlNzUtYjMyNC1kNjI1ZjM1MWRjOTAiLCJhY3IiOiIxIiwiY2xpZW50X3Nlc3Npb24iOiIyMjczZDU5Zi0wOTc2LTRkOTUtOWE2MS00MjBjYWJlMzhlY2EiLCJhbGxvd2VkLW9yaWdpbnMiOlsiaHR0cHM6Ly9hcGkuc3RlcGhlbi1naWJzb24uaW90cGRldi5jb20iLCJodHRwczovL3ByZWZzLnN0ZXBoZW4tZ2lic29uLmlvdHBkZXYuY29tIiwiaHR0cHM6Ly9zd2FnZ2VyLnN0ZXBoZW4tZ2lic29uLmlvdHBkZXYuY29tIiwiaHR0cHM6Ly9hcGkud3d3LnN0ZXBoZW4tZ2lic29uLmlvdHBkZXYuY29tIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJpb3RwX2FkbWluIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50Iiwidmlldy1wcm9maWxlIl19fSwibmFtZSI6IkFkbWluIFVzZXIiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJpb3RwYWRtaW51c2VyIiwiZ2l2ZW5fbmFtZSI6IkFkbWluIiwiZmFtaWx5X25hbWUiOiJVc2VyIiwiZW1haWwiOiJpb3RwdXNlckBnbWFpbC5jb20ifQ.mVdkSwl5vxN33UojzJaMzBUunGCL61Jn1pRKBztk8BkEwW_9LBKNBlZXMUQC58oQJmlC1g3WqzrCK4rQ6tciY7B6aM_joXt4kQWpkLh74qzXCIj0iqRZp7EMKbC0HlydJKGf1BnTv4oMLO-RY6zSVvl6vyAOFdKXEouggj7HLUwdSl32CctnNwyXt4SfRc3KNsq_RnUEcrfEIAkMo-ZjpiEXGwPjS1oyIHo3f1sgSs5xPlJaX625vEfZ2v7N-g1Q8g8h_FZV2FjxnNqrRChhUvHpW4M5l2BPyHQqoxhmHGgwJhDH7kzKEwJuSbFep_gHkl1cOrDf2Rz4gJhM9T5WMg'}
        #updates_df = json.loads(tempjsonstr)

        updates = requests.get(get_from_url, headers=headers_get)  # Update to include time parameters
        updates_df = updates.json()
        print updates_df

        forward = []
        if(len(updates_df["sensors"])>0):
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            for i in range(len(updates_df["sensors"][0])):
                forward.append({"collection":{"weight": updates_df["sensors"][0]["readings"][i]["sensorValue"]}})
                print updates_df["sensors"][1]["readings"][i]["sensorValue"]
                r = requests.post(push_to_url + updates_df["sensors"][1]["readings"][i]["sensorValue"] + "/collections", data=json.dumps(forward[i]), headers=headers)

            print json.dumps(forward)


            #r = requests.post(push_to_url+updates_df["sensors"][0]["readings"][0]["sensorValue"]+"/collections", data=json.dumps(forward), headers=headers)
            print r.status_code
            if (r.status_code<200 or r.status_code>299):
                print r.status_code
                print "post failed"
                return False
        time.sleep(10)

time_from = datetime.datetime.now() - datetime.timedelta(hours=13, seconds=10)
str_time_from = str(time_from.year)+'-0'+str(time_from.month)+'-'+str(time_from.day)+'T'+str(time_from.hour - 1)+':'+str(time_from.minute)+':'+str(time_from.second)+'Z'
#print str_time_from
url_to_use = urllib.quote_plus(str_time_from)
collect_data_url = "https://swagger.stephen-gibson.iotpdev.com/api/1/reporting/devices/d12a6dbd-3462-435c-8629-5788be1f783a?since="+url_to_use+"&reportingQueryType=NORMAL"

push_to_url_glob = 'http://174.129.63.189:8080/postcodes/'




pseudo_cron_job(collect_data_url, push_to_url_glob)


