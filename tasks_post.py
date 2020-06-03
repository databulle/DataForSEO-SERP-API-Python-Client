####
## DATAFORSEO SERPS API
##
## Post tasks
####

import csv
import configparser
import argparse
import time
import datetime
from client import RestClient

def range_limited_float_type(arg):
    """ Type function for argparse - a float within some predefined bounds """
    try:
        f = int(arg)
    except ValueError:    
        raise argparse.ArgumentTypeError("Must be an integer")
    if f < 1 or f > 100:
        raise argparse.ArgumentTypeError("Argument must be < " + str(1) + "and > " + str(100))
    return f


if __name__ == '__main__': 
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default="config.ini",
            type=str, help='Global config file (default: "config.ini")')
    parser.add_argument('--input', required=True,
            type=str, help='List of keywords to request')
    parser.add_argument('--output', default="keyword-requests",
            type=str, help='Output basename (default: "keyword-requests")')
    parser.add_argument('--language_code', default="fr",
            type=str, help='Language code for requests (default: "fr")')
    parser.add_argument('--location_code', default=2250,
            type=int, help='Location code for requests (default: "2250" for France, get other codes on <https://api.dataforseo.com/v3/serp/google/locations>)')
    parser.add_argument('--nb_results', default=10,
            type=int, help='Number of results (default: 10)')
    parser.add_argument('--device', choices=['desktop','mobile'], default="desktop",
            help='Device type (default:"desktop")')
    parser.add_argument('--priority', choices=['high','low'], default='low',
            help='Priority queue (default: "low")')
    parser.add_argument('--batch', default=100,
            type=range_limited_float_type, help='Max number of tasks per batch (default: 100)')
    parser.add_argument('--delay', default=10,
            type=float, help='Delay in seconds between batches of requests (default: 10)')
    parser.add_argument('--sep', default=";",
            type=str, help='CSV file separator (default: ";")')
    args = parser.parse_args()

    # Read list of requests
    with open(args.input,'r') as file:
        kws = list()
        for line in file.readlines():
            kws.append(str.strip(line))
        file.close()

    # Output headers
    fields=['request','status','id','tag']
    # Output name
    timestr = time.strftime("%Y%m%d-%H%M%S")
    tag = args.output + "-" + timestr
    filename = tag + ".csv"

    print('Requests are tagged: {}'.format(tag))

    # Set priority queue
    priority = {0:0,'low':1,'high':2}
    priority = priority[args.priority]

    conf = configparser.ConfigParser()
    conf.read(args.config)
    user = conf['general']['user']
    password = conf['general']['password']

    # Send requests
    with open(filename,'w',newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fields,delimiter=";")
        writer.writeheader()

        client = RestClient(user, password)

        # We need to send batches of max 100 tasks
        i = 0
        j = args.batch

        # Cut the kws list in batches
        while j < len(kws)+args.batch:  
            post_data = dict()          
            for kw in kws[i:j]:
                post_data[len(post_data)] = dict(
                    language_code=args.language_code,
                    location_code=args.location_code,
                    keyword=kw,
                    priority=priority,
                    depth=args.nb_results,
                    device=args.device,
                    tag=tag,
                )

            response = client.post("/v3/serp/google/organic/task_post", post_data)
            if response["status_code"] == 20000:
                for task in response["tasks"]:
                    data = dict()
                    data["request"] = task["data"]["keyword"]
                    data["status"] = task["status_message"]
                    data["id"] = task["id"]
                    data["tag"] = task["data"]["tag"]
                    writer.writerow(data)
                print("Batch {} done.".format(int((i/args.batch) + 1)))
            else:
                print("Error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))

            i = j
            j += args.batch
            time.sleep(args.delay)

