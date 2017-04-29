import time
import os
import requests
import json


def pseudo_cron_job(get_from_url, push_to_url):
    while True:

        updates = requests.get(get_from_url)  # Update to include time parameters
        updates_df = updates.json()
        print updates_df
        forwarding_data = {"id": 0,
                           "rfid": 'null',
                           "weight": 0}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(push_to_url, data=json.dumps(forwarding_data), headers=headers)
        if (r.status_code<200 or r.status_code>299):
            print "post failed"
            return False
        time.sleep(10)
pseudo_cron_job('https://github.com/timeline.json', ' ')