# DataForSEO SERP API Python Client

A simple Python client example to send requests and get results from [DataForSEO SERP API](https://dataforseo.com/apis/serp-api).  

## Setup

1. Clone this repo:  

    $ git clone git@gitlab.com:databulle/dataforseo-serp-api-python-client.git  
    $ cd dataforseo-serp-api-python-client  

2. (Optional) Setup a new [pyenv](https://github.com/pyenv/pyenv) virtual environment:  

    $ pyenv virtualenv 3.7.0 dataforseo  
    $ pyenv local dataforseo  

3. Get your credentials from DataForSEO:  

Go to [the API dashboard](https://app.dataforseo.com/api-dashboard) and get your `API Login` and `API Password`.  

4. Create you `config.ini` file:  

Copy the sample config file:  

    $ cp config.sample.ini config.ini  

Edit the new file and fill in your login and password  

5. That's all!  

### Sandbox  

If you want to test the API, you can simply edit the `client.py` file and replace on line 7:  

    domain = "api.dataforseo.com"  

With:  

    domain = "sandbox.dataforseo.com"  

The sandbox API lets you post as many requests as necessary to try your setup, and can send you dummy data.  
Remember to switch it back when things get real ;)  


## Usage

### 1. Post tasks

### 2. See if tasks are ready

This step is not required, but will show you how many of your requests have been processed and are available for download.  
Simply run:  

    $ python tasks_ready.py  



### 3. Get results

