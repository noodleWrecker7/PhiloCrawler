# Philosophy Crawler

### What does it do?
This is small script which crawls Wikipedia pages to see if they will reach the Philosophy page, as described [here](https://en.wikipedia.org/wiki/Wikipedia:Getting_to_Philosophy)

## Installing
##### Ensure you have Python 3 or above & pip installed and added to PATH
1. Clone the repo to its own folder and `cd` into it
2. Create the virtual environment\
    `py -m venv venv`
3. Activate the virtual environment

    For Windows run:
    `venv\Script\activate.bat`
    
    For Unix/MacOS run:    
    `source venv/bin/activate`
4. Install the requirements:\
    `pip install -r requirements.txt`
    
    You can then run the script using `py crawl.py`\
    Add a wiki page title after crawl.py to choose a specific page  