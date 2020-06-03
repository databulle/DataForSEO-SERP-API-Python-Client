####
## DATAFORSEO SERPS API
##
## Get available tasks results
####

import csv
import configparser
import argparse
import time
import datetime
from client import RestClient


if __name__ == '__main__': 
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default="config.ini",
            type=str, help='Global config file (default: "config.ini")')
    parser.add_argument('--output', default="keyword-results",
            type=str, help='Output basename (default: "keyword-results")')
    parser.add_argument('--delay', default=10,
            type=float, help='Delay in seconds between batches of requests (default: 10)')
    args = parser.parse_args()

    conf = configparser.ConfigParser()
    conf.read(args.config)
    user = conf['general']['user']
    password = conf['general']['password']

    # Output headers
    fields=['task_id','status','request','request_type','domain','location_code','language_code','timestamp','results_count','rank_group','rank_absolute','result_type','title','description','url','breadcrumb']
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
        response = client.get("/v3/serp/google/organic/tasks_ready")
        if response['status_code'] == 20000:
            tasks_available = response["tasks"][0]["result_count"]
            print("{} tasks available".format(tasks_available))
            if tasks_available < 1:
                next_batch = False
            results = []
            for task in response['tasks']:
                if (task['result'] and (len(task['result']) > 0)):
                    for resultTaskInfo in task['result']:
                        if(resultTaskInfo['endpoint_regular']):
                            results.append(client.get(resultTaskInfo['endpoint_regular']))                

            for result in results:
                for task in result["tasks"]:
                    task_id = task['id']
                    status = task['status_message']
                    for kw in task["result"]:
                        keyword = kw["keyword"]
                        request_type = kw["type"]
                        domain = kw["se_domain"]
                        location_code = kw["location_code"]
                        language_code = kw["language_code"]
                        timestamp = kw["datetime"]
                        results_count = kw["se_results_count"]

                        for item in kw["items"]:
                            row = dict()
                            row["task_id"] = task_id
                            row["status"] = status
                            row["request"] = keyword
                            row["request_type"] = request_type
                            row["domain"] = domain
                            row["location_code"] = location_code
                            row["language_code"] = language_code
                            row["timestamp"] = timestamp
                            row["results_count"] = results_count
                            row["result_type"] = item["type"]
                            row["rank_group"] = item["rank_group"]
                            row["rank_absolute"] = item["rank_absolute"]
                            row["title"] = item["title"]
                            row["description"] = item["description"]
                            row["url"] = item["url"]
                            row["breadcrumb"] = item["breadcrumb"]

                            with open(filename,'a',newline='') as file:
                                writer = csv.DictWriter(file, fieldnames=fields, delimiter=";")
                                writer.writerow(row)
                                file.close()

            print("Batch done.")
            time.sleep(args.delay)
        else:
            next_batch = False
            print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))