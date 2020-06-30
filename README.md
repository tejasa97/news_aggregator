
# News Aggregator
##### (As part of M*****d*** challenge)

News Aggregator is an app you can use to obtain and aggregate news from your favorite news providers (ofcourse as long as they have some API interface) 

 ## Tech
 
News Aggregator uses a number of open source projects that comprise it's core components


* [Python]
* [Fastapi]
* [Reddit API]
* [NewsAPI API]

## Installation

News Aggregator requires **Python3.7+** runtime and is built on the *async micro web-framework* **fastapi**

1. Clone this repository  
2. **(Optional)** Sign up for [NewsAPI] and obtain an API KEY, and replace the existing key in the `.env` file (a working demo key is already in repository)
3. Create a virtual environment with *Python3.7+* runtime
4. Activate the virtual environment.
5. Install the required dependencies.
	```sh
	pip install -r requirements.txt
	```
6. Use **uvicorn** to run the app on port 8000.
    ```sh
    uvicorn app:app
    ```
    You should see the following console output once the app's started:
    ```sh
    INFO:     Started server process [2734]   
    INFO:     Waiting for application startup.
    INFO:     Application startup complete.
    INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
    ```

## Usage

News Aggregator provides for a single API, whose usage is explained below

### REST APIs <br>
1. Get general news <br>
  **Request:**
     ```sh
     $ curl localhost:8000/news | json_pp
     ```
    **Response:**
    ```sh
	[
     {
        "source" : "reddit",
        "link" : "https://apnews.com/425e43fa0ffdd6e126c5171653ec47d1",
        "headline" : "AP sources: White House aware of Russian bounties in 2019"
     },
     {
        "headline" : "NYC mayor de Blasio announces plan to slash police budget by $1 billion",
        "link" : "https://globalnews.ca/news/7122512/nyc-plan-defund-police-budget-billion/",
        "source" : "reddit"
     },
     {
        "source" : "newsapi",
        "link" : "https://www.cnn.com/videos/health/2020/06/27/coronavirus-task-force-briefings-dr-peter-hotez-nr-vpx.cnn",
        "headline" : "Doctor on Covid-19 task force briefings: 'Stop screwing around'"
     },
     {
        "link" : "https://www.cnn.com/videos/politics/2020/06/09/bill-barr-donald-trump-white-house-bunker-george-floyd-protests-ebof-sot-vpx.cnn",
        "headline" : "Bill Barr contradicts Trump on his move to the WH bunker",
        "source" : "newsapi"
     }
    ]
    ```
   
2. Get news with a search query term <br> <br>
 	Example : Search for news related to *corona* <br>
    **Request:**
     ```sh
     $ curl localhost:8000/news?query=corona | json_pp
     ```
     **Response:**
     ```sh
     [
       {
          "headline" : "Twitter will fix its overly aggressive '5G corona' fact-checking",
          "source" : "newsapi",
          "link" : "https://www.engadget.com/twitter-to-fix-5g-coronavirus-fact-checking-164611364.html"
       },
       {
          "source" : "newsapi",
          "link" : "https://www.reuters.com/article/us-health-coronavirus-finance-breakingvi-idUSKBN2401CZ",
          "headline" : "Breakingviews - Corona Capital: Vietnam, Vaccine investment - Reuters"
       },
       {
          "headline" : "China Corona virus spreads before symptoms show",
          "source" : "reddit",
          "link" : "https://www.bbc.co.uk/news/world-asia-china-51254523"
       },
       {
          "source" : "reddit",
          "link" : "https://www.dw.com/en/coronavirus-reaches-europe-as-france-confirms-3-cases/a-52145333",
          "headline" : "Corona virus spreads to Europe, France confirms 3 cases."
       },
      ]
     ```
[NewsAPI API]: <https://newsapi.org/account>
[Python]: <https://www.python.org/>
[Fastapi]: <https://fastapi.tiangolo.com/>
[Reddit API]: <https://www.reddit.com/dev/api>
