# avito data scrapping

script for scrapping some data from avito web pages

## How to run
  1. Make a virtual env by `python -m venv ./venvdir`
  2. Install requirements by `pip install -r requirements.txt`
  3. Run `avito_scrap.py "path_to_json" "out_file_name"`
  
### JSON
  In json folder you will find an examples how to tune your json
  file according to got data you need.
  The main idea is what you need to define params to get 'products card'
  and then you need to define 'fields' list you want to be parsed.

