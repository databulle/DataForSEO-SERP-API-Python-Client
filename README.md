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

### SERPs

Get results from Google on a list of keywords.  

#### 1. Post tasks

Put the list of keywords in a text file (one request per line), then run:  

    $ python serps_post.py --input yourfile.txt  

The script will send the keywords to the API by batches of 100 requests, and write a report containing the `task_id` for each keyword.  

The `input` argument is required. Other options are available:  
- `config`: configuration file to use (default: `config.ini`)  
- `input`: input file with the list of requests (required)  
- `output`: output basename for the report (default: `serps-tasks`)  
- `language_code`: language code for the requests (default: `fr`)  
- `location_code`: location code for requests (default: "2250" for France, get other codes on <https://api.dataforseo.com/v3/serp/google/locations>)  
- `nb_results`: number of results to ask for (default: `10`)  
- `device`: choice between `desktop` (default) and `mobile`  
- `pixels`: activate to get the number of pixels from the top of the page to the result (this will double requests costs). You'll need to use the `--advanced` option when getting the results.  
- `priority`: choose the priority queue between `low` (default) and `high` (note: `high` priority requests will be charged more by DataForSEO)  
- `batch`: number of requests to send for each batch, between 1 and 100 (default: `100`)  
- `delay`: delay in seconds between batches of requests (default: `10`)  
- `sep`: CSV separator for `output`(default: `;`)  


#### 2. See if tasks are ready

This step is not required, but will show you how many of your requests have been processed and are available for download.  
Simply run:  

    $ python serps_ready.py  

Note that the API will only show you 1000 available results at most, but there might be more not shown.  

#### 3. Get results

Once you've posted your requests, it usually takes only a few instants for the API to process.  
To get the results, run:  

    $ python serps_get.py  

The script will request the API to check for available results, then download the data for each done task and repeat while there are available results.  

Available options:  
- `config`: configuration file to use (default: `config.ini`)  
- `output`: output basename for the results (default: `serps-results`)  
- `advanced`: get advanced details, such as presence of image, video, ratings, sitelinks, ... or position of the result in pixels (default: `False`).  
- `knowledge_graph`: extract specific content from KG panel. This needs the `advanced` mode to be activated. It will concentrate on locations and extract subtitle, address and phone number. Note that these infos are available in the `items` json field when `advanced` is activated, but less easy to process.  
- `delay`: delay in seconds between batches of requests (default: `10`)  


### Keywords

Get keywords data from Google AdWords API: search volume, cpc, competition, categories.  

#### 1. Post tasks  

Put the list of keywords in a text file (one request per line), then run:  

    $ python keywords_data_post.py --input yourfile.txt  

The script will send the keywords to the API by batches of 100 requests, and write a report containing the `task_id` for each keyword.  

The `input` argument is required. Other options are available:  
- `config`: configuration file to use (default: `config.ini`)  
- `input`: input file with the list of requests (required)  
- `output`: output basename for the report (default: `keywords-data-tasks`)  
- `language_code`: language code for the requests (default: `fr`)  
- `location_code`: location code for requests (default: "2250" for France, get other codes on <https://api.dataforseo.com/v3/keywords_data/google/locations>)  
- `batch`: number of keywords to include for each batch, between 1 and 700 (default: `700`). You will be charged the same amount per batch, no matter what number of keywords you include (so better stay with 700!).  
- `delay`: delay in seconds between batches of requests (default: `1`)  
- `sep`: CSV separator for `output`(default: `;`)  

#### 2. See if tasks are ready  

This step is not required, but will show you how many of your requests have been processed and are available for download.  
Simply run:  

    $ python keywords_data_ready.py  

#### 3. Get results  

Once you've posted your requests, it usually takes only a few instants for the API to process.  
To get the results, run:  

    $ python keywords_data_get.py  

The script will request the API to check for available results, then download the data for each done task and repeat while there are available results.  

Available options:  
- `config`: configuration file to use (default: `config.ini`)  
- `output`: output basename for the results (default: `keywords-data-results`)  
- `delay`: delay in seconds between batches of requests (default: `10`)  

## Contributing

If you wish to contribute to this repository or to report an issue, please do this [on GitLab](https://gitlab.com/databulle/dataforseo-serp-api-python-client).  