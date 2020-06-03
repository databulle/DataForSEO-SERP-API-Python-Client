# DataForSEO SERP API Python Client

A simple Python client example to send requests and get results from [DataForSEO SERP API](https://dataforseo.com/apis/serp-api).  

## Setup

__1. Clone this repo:__  

    $ git clone git@gitlab.com:databulle/dataforseo-serp-api-python-client.git
    $ cd dataforseo-serp-api-python-client  


__2. (Optional) Setup a new [pyenv](https://github.com/pyenv/pyenv) virtual environment:__  

    $ pyenv virtualenv 3.7.0 dataforseo
    $ pyenv local dataforseo  


__3. Get your credentials from DataForSEO:__  

Go to [the API dashboard](https://app.dataforseo.com/api-dashboard) and get your `API Login` and `API Password`.  


__4. Create you `config.ini` file:__  

Copy the sample config file:  

    $ cp config.sample.ini config.ini  

Edit the new file and fill in your login and password  


__5. That's all!__  

### Sandbox  

If you want to test the API, you can simply edit the `client.py` file and replace on line 7:  

    domain = "api.dataforseo.com"  

With:  

    domain = "sandbox.dataforseo.com"  

The sandbox API lets you post as many requests as necessary to try your setup, and can send you dummy data.  
Remember to switch it back when things get real ;)  


## Usage

### 1. Post tasks

Put the list of keywords in a text file (one request per line), then run:  

    $ python tasks_post.py --input yourfile.txt  

The script will send the keywords to the API by batches of 100 requests, and write a report containing the `task_id` for each keyword.  

The `input` argument is required. Other options are available:  
- `config`: configuration file to use (default: `config.ini`)  
- `input`: input file with the list of requests (required)  
- `output`: output basename for the report (default: `keyword-requests`)  
- `language_code`: language code for the requests (default: `fr`)  
- `location_code`: location code for requests (default: "2250" for France, get other codes on <https://api.dataforseo.com/v3/serp/google/locations>)  
- `nb_results`: number of results to ask for (default: `10`)  
- `device`: choice between `desktop` (default) and `mobile`  
- `priority`: choose the priority queue between `low` (default) and `high` (note: `high` priority requests will be charged more by DataForSEO)  
- `batch`: number of requests to send for each batch, between 1 and 100 (default: `100`)  
- `delay`: delay in seconds between batches of requests (default: `10`)  
- `sep`: CSV separator for `output`(default: `;`)  


### 2. See if tasks are ready

This step is not required, but will show you how many of your requests have been processed and are available for download.  
Simply run:  

    $ python tasks_ready.py  



### 3. Get results

