####
## DATAFORSEO SERPS API
##
## Shows number of tasks ready for download
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
    args = parser.parse_args()

    conf = configparser.ConfigParser()
    conf.read(args.config)
    user = conf['general']['user']
    password = conf['general']['password']

    client = RestClient(user,password)

    response = client.get("/v3/serp/google/organic/tasks_ready")
    if response["status_code"] == 20000:
        tasks_available = response["tasks"][0]["result_count"]
        print("{} tasks available".format(tasks_available))
    else:
        print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))
