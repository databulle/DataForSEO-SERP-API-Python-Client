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
import json


if __name__ == '__main__': 
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default="config.ini",
            type=str, help='Global config file (default: "config.ini")')
    parser.add_argument('--output', default="serps-results",
            type=str, help='Output basename (default: "serps-results")')
    parser.add_argument('--advanced', action='store_true', default=False,
            help='Get advanced details (default: False)')
    parser.add_argument('--knowledge_graph', action='store_true', default=False,
            help='Specific KG content scrap - needs Advanced (default: False)')
    parser.add_argument('--delay', default=10,
            type=float, help='Delay in seconds between batches of requests (default: 10)')
    args = parser.parse_args()

    # Check if --advanced with --knowledge_graph
    if args.knowledge_graph and not args.advanced:
        parser.error("Advanced mode (`--advanced`) must be activated to use the `--knowledge_graph` argument.")

    conf = configparser.ConfigParser()
    conf.read(args.config)
    user = conf['general']['user']
    password = conf['general']['password']

    # Output headers
    fields=['task_id','status','request','request_type','domain','location_code','language_code','timestamp','results_count','spell','item_types','rank_group','rank_absolute','item_type','title','description','url','breadcrumb']
    if args.advanced:
        fields.extend(['is_image','is_video','is_featured_snippet','is_malicious','is_web_story','amp_version','rating','sitelinks','faq','items','pixels_from_top'])
    if args.knowledge_graph:
        fields.extend(['sub_title','address','phone'])

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
                        if(resultTaskInfo['endpoint_advanced']):
                            results.append(client.get(resultTaskInfo['endpoint_advanced']))                

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
                        spell = json.dumps(kw["spell"])
                        item_types = json.dumps(kw["item_types"])

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
                            row["spell"] = spell
                            row["item_types"] = item_types
                            row["results_count"] = results_count
                            row["item_type"] = item["type"]
                            row["rank_group"] = item["rank_group"]
                            row["rank_absolute"] = item["rank_absolute"]
                            if "title" in item.keys():
                                row["title"] = item["title"]
                            if "description" in item.keys():
                                row["description"] = item["description"]
                            if "url" in item.keys():
                                row["url"] = item["url"]
                            if "breadcrumb" in item.keys():
                                row["breadcrumb"] = item["breadcrumb"]

                            if args.advanced:
                                if "is_image" in item.keys():
                                    row["is_image"] = item["is_image"]
                                if "is_video" in item.keys():
                                    row["is_video"] = item["is_video"]
                                if "is_featured_snippet" in item.keys():
                                    row["is_featured_snippet"] = item["is_featured_snippet"]
                                if "is_malicious" in item.keys():
                                    row["is_malicious"] = item["is_malicious"]
                                if "is_web_story" in item.keys():
                                    row["is_web_story"] = item["is_web_story"]
                                if "amp_version" in item.keys():
                                    row["amp_version"] = item["amp_version"]
                                if "rating" in item.keys():
                                    row["rating"] = json.dumps(item["rating"])
                                if "links" in item.keys():
                                    row["sitelinks"] = json.dumps(item["links"])
                                if "faq" in item.keys():
                                    row["faq"] = json.dumps(item["faq"])
                                if "items" in item.keys():
                                    row["items"] = json.dumps(item["items"])
                                if "rectangle" in item.keys():
                                    row["pixels_from_top"] = item["rectangle"]["y"]

                                if (args.knowledge_graph) and (item["type"] == "knowledge_graph"):
                                    if "sub_title" in item.keys():
                                        row["sub_title"] = item["sub_title"]
                                    for i in item["items"]:
                                        if "data_attrid" in i.keys():
                                            if "address" in str(i["data_attrid"]):
                                                row["address"] = i["text"]
                                            elif "phone" in str(i["data_attrid"]):
                                                row["phone"] = i["text"]


                            with open(filename,'a',newline='') as file:
                                writer = csv.DictWriter(file, fieldnames=fields, delimiter=";")
                                writer.writerow(row)
                                file.close()

            print("Batch done.")
            time.sleep(args.delay)
        else:
            next_batch = False
            print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))
