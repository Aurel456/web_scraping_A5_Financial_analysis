from flask import Flask, render_template, request
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pandas as pd
from joblib import load

app = Flask(__name__)

# Loading the sentiment analysis model
tokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/roberta-large-financial-news-sentiment-en")
specific_model = AutoModelForSequenceClassification.from_pretrained("Jean-Baptiste/roberta-large-financial-news-sentiment-en")
pipe = pipeline("text-classification", model=specific_model, tokenizer=tokenizer)
X_encoded_ticker_columns = ['Ticker_A', 'Ticker_AAPL', 'Ticker_ADI', 'Ticker_ADM', 'Ticker_AEE',
    'Ticker_AEP', 'Ticker_AES', 'Ticker_AJG', 'Ticker_ALB', 'Ticker_AM',
    'Ticker_AMT', 'Ticker_ANET', 'Ticker_APD', 'Ticker_ARCH', 'Ticker_ASH',
    'Ticker_AVY', 'Ticker_BG', 'Ticker_BR', 'Ticker_BTU', 'Ticker_CAG',
    'Ticker_CALM', 'Ticker_CBT', 'Ticker_CDNS', 'Ticker_CMG', 'Ticker_CMI',
    'Ticker_CMS', 'Ticker_COMM', 'Ticker_COP', 'Ticker_CVX', 'Ticker_D',
    'Ticker_DAR', 'Ticker_DE', 'Ticker_DECK', 'Ticker_DHR', 'Ticker_DOX',
    'Ticker_DTE', 'Ticker_ED', 'Ticker_EPAM', 'Ticker_ES', 'Ticker_EXC',
    'Ticker_EXPO', 'Ticker_FMC', 'Ticker_FSLR', 'Ticker_FSS', 'Ticker_GEF',
    'Ticker_HAL', 'Ticker_HES', 'Ticker_HRL', 'Ticker_HST', 'Ticker_IBM',
    'Ticker_IT', 'Ticker_JBHT', 'Ticker_JBL', 'Ticker_KBR', 'Ticker_KDP',
    'Ticker_KEYS', 'Ticker_KMI', 'Ticker_KO', 'Ticker_KR', 'Ticker_LECO',
    'Ticker_LLY', 'Ticker_LNG', 'Ticker_LNT', 'Ticker_LTHM', 'Ticker_MA',
    'Ticker_MAR', 'Ticker_MAT', 'Ticker_MDLZ', 'Ticker_MPC', 'Ticker_MRK',
    'Ticker_MRO', 'Ticker_MSM', 'Ticker_NEE', 'Ticker_NRG', 'Ticker_NSP',
    'Ticker_OKE', 'Ticker_ON', 'Ticker_ORA', 'Ticker_OXY', 'Ticker_PEP',
    'Ticker_PKG', 'Ticker_PSA', 'Ticker_PSX', 'Ticker_RRC', 'Ticker_SCL',
    'Ticker_SHO', 'Ticker_SRE', 'Ticker_TMO', 'Ticker_TXN', 'Ticker_VC',
    'Ticker_VLO', 'Ticker_VRSK', 'Ticker_VVV', 'Ticker_WCC', 'Ticker_WEC',
    'Ticker_WMB', 'Ticker_WOR', 'Ticker_XEL', 'Ticker_XOM']
all_tickers = [k[7:] for k in X_encoded_ticker_columns]

# Loading the prediction model
model = load('data/saved_model.joblib')

def get_sentiment_score(article):
    sentiment_result = pipe(article)
    sentiment_label = sentiment_result[0]['label']
    sentiment_score = sentiment_result[0]['score']
    return sentiment_label, sentiment_score

def convert_sentiment_to_score(sentiment_label):
    sentiment_mapping = {'negative': -1, 'neutral': 0, 'positive': 1}
    return sentiment_mapping.get(sentiment_label, 0)

def predict_stock_value(article_text, ticker_name):
    sentiment_label, sentiment_score = get_sentiment_score(article_text)
    sentiment_score_numeric = convert_sentiment_to_score(sentiment_label)

    input_data = {
        'Date': '2023-12-30',  # Replace with the article's date if available
        'sentiment_endoded_JB': sentiment_score_numeric
    }
    input_df = pd.DataFrame([input_data])
    input_df['Date'] = pd.to_datetime(input_df['Date'])
    input_df['Year'] = input_df['Date'].dt.year
    input_df['Month'] = input_df['Date'].dt.month
    input_df['Day'] = input_df['Date'].dt.day
    input_df = input_df.drop('Date', axis=1)


    
    input_df[X_encoded_ticker_columns] = False
    input_df.loc[0, f'Ticker_{ticker_name}'] = True
    
    prediction = model.predict(input_df)
    return prediction[0]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        article_text = request.form['article']
        ticker_name = request.form['ticker']
        
        predicted_value = predict_stock_value(article_text, ticker_name)
        
        sentiment_label, sentiment_score = get_sentiment_score(article_text)
        
        return render_template('result.html', 
                               article=article_text, 
                               ticker=ticker_name,
                               sentiment_label=sentiment_label,
                               sentiment_score=sentiment_score,
                               predicted_value=predicted_value)
    return render_template('index.html',  all_tickers=all_tickers)

@app.route('/esg_info')
def esg_info():
    return render_template('esg_info.html')

if __name__ == '__main__':
    app.run(debug=True)
