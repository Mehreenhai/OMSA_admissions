# Stats for GeorgiaTech OMS in Analytics Applications

Analysis of Data Provided on Reddit by Applicants of GeorgiaTech's Online Masters of Science in Analytics for terms Fall 2017 to Spring 2019.

## Intro

### Motivations Behind this Analysis

I am extremely interested in pursuing an Online Masters in Data Analytics which concentrates on conducting the analysis through programming languages. For this reason, I decided to analyze posts available online (on Reddit - threads created and maintained by u/xoxoalexa) by applicants of one of the most popular such programs: GeorgiaTech's Online Masters in Analytics (offered through EdX), hoping to learn a bit more about the admissions experience.

I have used some of the Data Analytics skills I learned in UC Berkeley Extension's Data Analytics Bootcamp as well as GeorgiaTech's online course 'Data Analytics in Business'.


## Prerequisites

What things you need to install and use my code:
```
For the purpose of data retrieval and data analysis, I have used a variety of tools including:
* Python
* Praw (API wrapper for Reddit API)
* Requests
* Pandas  
* Numpy
* Matplotlib
* Vader (for sentiment analysis)
* Wordcloud
```
## Methodology

```
I first used Praw (a very user-friendly API wrapper for Reddit), along with the Requests module in Python to scrape 4 Reddit threads for data (1 for every admissions cycle so far). Then using Pandas I cleaned up the data and made it ready for analysis. Following this I used a number of modules such as Numpy, Matplotlib, Wordcloud and Vader for analyzing the data and finding patterns or interesting points in the data.

```

## Running the script

You should be able to fork this respository and get an updated version of my data by simply running the app.py file (after plugging in your own config file).



# Results

Results

### Average Sentiments of Comments by Admissions Cycle

![alt text](https://github.com/Mehreenhai/OMSAnalytics_admissions/blob/master/graphs/Comment_sentiments_by_term.png)

### A Word Cloud Analysis of Comments left by Applicants of this thread

![alt text](https://github.com/Mehreenhai/OMSAnalytics_admissions/blob/master/graphs/comments_wordcloud.png)


### Time Taken (in Days) for Successful and Unsuccessful Candidates to Get Decisions

![alt text](https://github.com/Mehreenhai/OMSAnalytics_admissions/blob/master/graphs/Response_time_by_decision.png)

### Time Taken (in Days) for Candidates in every Admissions Cycle to Get Decisions

![alt text](https://github.com/Mehreenhai/OMSAnalytics_admissions/blob/master/graphs/Response_time_by_term.png)

### Success Rates of Applicants Contributing to this Data

![alt text](https://github.com/Mehreenhai/OMSAnalytics_admissions/blob/master/graphs/Status_metrics_chart.png)




## Acknowledgments

* Extremely grateful to u/xoxoalexa for maintaining this data every admissions cycle and ensuring a format that makes it easy to use.

