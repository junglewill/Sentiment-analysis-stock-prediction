# Sentiment Analysis for Stock Prediction

This project contains 3 parts: 

1. Keywords list:  
Create keywords lists for rise and decline scenarios separately, using tf-idf and chi-square value.
2. Big Issue Prediction:  
Train and test the news and forum data released before significant issues happened, like the golden cross and death cross. Use the keywords with higher tf-idf to train 2016-2017 data to predict 2018 data to see if the stock price is reversing.
3. Placing Order Simulation:  
Simulate and backtest to optimize our performance (gain or loss) of long position in the market for the target stocks. 

The dataset we used is the data of news and bbs (the largest public forum in Taiwan) from 2016 to 2018. The stocks we discussed include TSMC (2330.TW), Foxconn (2317.TW), and Uni-President (1216.TW). The programming language is Python.

It was a group project created in the Big Data and Business Analytics course at National Taiwan University. I created labelled word lists and extracted the related data for the three target stocks, while my teammates covered most of the modeling parts at that time.


