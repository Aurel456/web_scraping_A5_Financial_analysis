# web_scrapping_A5_Financial_Analysis
master 2 web scrapping project 

# ESG Company Analysis Project

## Overview
This project aims to perform an analysis of ESG (Environmental, Social, Governance) companies by collecting data from various sources, performing sentiment analysis on news headlines, and visualizing sentiment trends among these companies.

## Project Structure
### Webscrapping
- `webscrapper_google_finance_CDP.ipynb`:scarping data from Google Finance of climate-leaders.
- `yfinance.ipynb`: scraping data using Yahoo Finance API, Finviz
### data processing + sentiment analysis + ML + Use case demonstration
- `sentiment_analysis.ipynb`: Notebook for sentiment analysis
### html interface with templates and static images
- `app.py`:Flask interface for the website
- `index.html`: Main page, input the article and the entreprise ticker
- `result.html`: Result of sentiment analysis + prediction on stock percent variation 3 days from today's date
- `esg_info.html`:Displaying how we selected the entreprise to scrap, ESG

### data
- `data_close.csv`: CSV file containing closing stock prices of ESG companies.
- `data_open.csv`: CSV file containing opening stock prices of ESG companies.
 - `rolling_diff_3days.csv`: CSV  file containing rolling difference in 3 days of the stock prices 
- `news_esg.csv`: CSV file storing news headlines scraped from Finviz related to ESG companies.
- `news_esg_sentiment.csv`: CSV file with sentiment analysis results of news headlines.

## Requirements
- Python 3.10
- Libraries: `pandas`, `numpy`, `requests`, `beautifulsoup4`, `yfinance`, `transformers`, `tqdm`, `matplotlib`, `seaborn`, `flask`, `joblib`

## Steps to Run the Project
1. Ensure Python 3.10 is installed.
2. Install the required libraries using `pip install -r requirements.txt`.
3. Open and run the Jupyter Notebooks to scrap and analys data, train a ML model. We already have a pretrained model in /data
4. Run `app.py`, the app will be running on **http://127.0.0.1:5000**
5.  Enter the news article, select a Ticker, press **Predict**, you will be redirected on the result webpage.


## Additional Notes
- The sentiment analysis utilizes transformer-based models from the `transformers` library.
- The project aims to provide insights into the sentiment trends among ESG companies using news headlines.
- Visualization scripts are available in the Jupyter Notebook to analyze sentiment distribution across companies.

## References
- [Google Finance climate leaders](https://www.google.com/finance/markets/climate-leaders)
- [Investors.com](https://www.investors.com/news/esg-stocks-list-of-100-best-esg-companies/)
- [Yahoo Finance API](https://finance.yahoo.com/)
- [Finviz](https://finviz.com/)
- [Transformers Library](https://huggingface.co/transformers/)

