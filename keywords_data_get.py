####
## DATAFORSEO GOOGLE KEYWORDS API
##
## Fetches available results from API.
####

import csv
import configparser
import argparse
import time
import datetime
from client import RestClient
import json

if __name__ == '__main__': 
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default="config.ini",
            type=str, help='Global config file (default: "config.ini")')
    parser.add_argument('--output', default="keywords-data-results",
            type=str, help='Output basename (default: "keywords-data-results")')
    parser.add_argument('--delay', default=1,
            type=float, help='Delay in seconds between batches of requests (default: 1)')
    args = parser.parse_args()

    conf = configparser.ConfigParser()
    conf.read(args.config)
    user = conf['general']['user']
    password = conf['general']['password']

    # Output headers
    fields=['keyword','location_code','language_code','search_partners','search_volume','cpc','competition','categories','monthly_searches']
    # Output name
    timestr = time.strftime("%Y%m%d-%H%M%S")
    tag = args.output + "-" + timestr
    filename = tag + ".csv"

    with open(filename,'w',newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fields, delimiter=";")
        writer.writeheader()
        file.close()

    client = RestClient(user,password)

    # While there are results, request the next batch
    next_batch = True
    while next_batch:
        response = client.get("/v3/keywords_data/google/search_volume/tasks_ready")
        if response['status_code'] == 20000:    
            tasks_available = response["tasks"][0]["result_count"]
            print("{} tasks available".format(tasks_available))
            if tasks_available < 1:
                next_batch = False

            for task in response["tasks"]:
                if (task['result'] and (len(task['result']) > 0)):
                    for result_task_info in task['result']:
                        if(result_task_info['endpoint']):
                            res = client.get(result_task_info['endpoint'])
                            
                            for t in res["tasks"]:
                                if (t['result'] and (len(t['result']) > 0)):
                                    for k in t['result']:
                                        data = dict()
                                        data["keyword"] = k["keyword"]
                                        data["location_code"] = k["location_code"]
                                        data["language_code"] = k["language_code"]
                                        data["search_partners"] = k["search_partners"]
                                        data["search_volume"] = k["search_volume"]
                                        data["cpc"] = k["cpc"]
                                        data["competition"] = k["competition"]
                                        data["categories"] = json.dumps(k["categories"])
                                        monthly_searches = []
                                        for m in sorted(k["monthly_searches"], key=lambda x: (x['year'], x['month'])):
                                            monthly_searches. append(m["search_volume"])
                                        data["monthly_searches"] = json.dumps(monthly_searches)
                                        
                                        with open(filename,'a',newline='') as file:
                                            writer = csv.DictWriter(file, fieldnames=fields, delimiter=";")
                                            writer.writerow(data)
                                            file.close()
                            
            print("Batch done.")
            time.sleep(args.delay)
        else:
            next_batch = False
            print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"])) 
