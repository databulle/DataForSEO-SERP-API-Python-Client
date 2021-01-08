####
## DATAFORSEO GOOGLE KEYWORDS API
##
## Posts keywords search volume requests.  
####

import csv
import configparser
import argparse
import time
import datetime
from client import RestClient

def range_limited_int_type(arg):
    """ Type function for argparse - an int within some predefined bounds """
    try:
        f = int(arg)
    except ValueError:    
        raise argparse.ArgumentTypeError("Must be an integer")
    if f < 1 or f > 700:
        raise argparse.ArgumentTypeError("Argument must be < " + str(1) + " and > " + str(700))
    return f

if __name__ == '__main__': 
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default="config.ini",
            type=str, help='Global config file (default: "config.ini").')
    parser.add_argument('--input', required=True,
            type=str, help='List of keywords to request.')
    parser.add_argument('--output', default="keywords-data-tasks",
            type=str, help='Output basename (default: "keywords-data-tasks").')
    parser.add_argument('--language_code', default="fr",
            type=str, help='Language code for requests (default: "fr")')
    parser.add_argument('--location_code', default=2250,
            type=int, help='Location code for requests (default: "2250" for France, get other codes on <https://api.dataforseo.com/v3/serp/google/locations>)')
    parser.add_argument('--batch', default=700,
            type=range_limited_int_type, help='Max number of tasks per batch. Max 700. Each batch costs 0.05$ (default: 700).')
    parser.add_argument('--delay', default=1,
            type=float, help='Delay in seconds between batches of requests (default: 1).')
    parser.add_argument('--sep', default=";",
            type=str, help='CSV file separator (default: ";").')
    args = parser.parse_args()


        # Read list of requests
    with open(args.input,'r') as file:
        kws = list()
        for line in file.readlines():
            kws.append(str.strip(line))
        file.close()
    # Output headers
    fields=['id','status','tag','nb_requests','first_kw','last_kw']
    # Output name
    timestr = time.strftime("%Y%m%d-%H%M%S")
    tag = args.output + "-" + timestr
    filename = tag + ".csv"

    conf = configparser.ConfigParser()
    conf.read(args.config)
    user = conf['general']['user']
    password = conf['general']['password']

    with open(filename,'w',newline='') as file:
        writer = csv.DictWriter(file,fieldnames=fields,delimiter=args.sep)
        writer.writeheader()
        file.close()

        client = RestClient(user, password)
        i = 0
        j = args.batch

        # Cut the kws list in batches
        while j < len(kws)+args.batch:
            post_data = {}
            post_data[len(post_data)] = dict(
                language_code = args.language_code,
                location_code = args.location_code,
                keywords = kws[i:j],
                tag = tag,
            )


            response = client.post("/v3/keywords_data/google/search_volume/task_post", post_data)
            if response["status_code"] == 20000:
                for task in response["tasks"]:
                    data = dict()
                    data["nb_requests"] = len(task["data"]["keywords"])
                    data["first_kw"] = task["data"]["keywords"][0]
                    data["last_kw"] = task["data"]["keywords"][-1]
                    data["status"] = task["status_message"]
                    data["id"] = task["id"]
                    data["tag"] = task["data"]["tag"]
                    with open(filename,'a',newline='') as file:
                        writer = csv.DictWriter(file,fieldnames=fields,delimiter=args.sep)
                        writer.writerow(data)
                        file.close()
                print("Batch {} done.".format(int((i/args.batch) + 1)))
            else:
                print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))

            i = j
            j += args.batch
            time.sleep(args.delay)

        file.close()