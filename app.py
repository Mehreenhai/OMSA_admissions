import os
from os import path
import praw
import config
import requests #import Session
import pandas as pd
import numpy
import csv
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from datetime import datetime
from dateutil import parser
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()

reddit = praw.Reddit(client_id=config.client_id,
                     client_secret=config.client_secret,
                     password=config.password,
                     user_agent='masters_proj',
                     username='mehreenhai')


# print("Testing - my username is: " + str(reddit.user.me()))

submission_2019_spring = reddit.submission(id="8m2anv")
submission_2018_fall = reddit.submission(id="7sgy2v")
submission_2018_spring = reddit.submission(id="6tmfea")
submission_2017_fall = reddit.submission(id="6h9avr")
#example url='https://www.reddit.com/r/OMSA/comments/8m2anv/spring_2019_admissions_thread/')

def get_raw_answers():
    ans_num = 0
    global answers_df 
    answers_df = pd.DataFrame()
    raw_answers = []
    term = []

    for item in [submission_2019_spring, submission_2018_fall, submission_2018_spring, submission_2017_fall]:
        
        for top_level_comments in item.comments:   
            if item == submission_2019_spring:
                term.append("2019_Spring")
            elif item == submission_2018_spring:
                term.append("2018_Spring")
            elif item == submission_2018_fall:
                term.append("2018_fall")
            elif item == submission_2017_fall:
                term.append("2017_fall")
            else: 
                term.append("rogue data - check script")

            raw_answers.append(top_level_comments.body)

    answers_df['term'] = term
    answers_df['raw_answers'] = raw_answers
    print("Found " + str(len(raw_answers))+ " raw answers.\n")
    print(answers_df.head())
    answers_df.to_csv("data_collected/raw_answers.csv")



def clean_answers():
    answers_df = pd.read_csv("data_collected/raw_answers.csv")
    print("raw answers length: " + str(len(answers_df)))
    status = []
    application_date = []
    decision_date = []
    education = []
    test_scores = []
    experience = []
    comments = []

    for answers in answers_df["raw_answers"]:
        answer_components = answers.split("\n")
        if "Status:" in answers:
            for component in answer_components:
                if "Status:" in component:
                    if ("Accepted" in component or "accepted" in component or "Accept" in component):
                        status.append("Accepted")
                    elif ("Rejected" in component or "rejected" in component or "Denied" in component):
                        status.append("Rejected")
                    elif ("Deferred" in component or "deferred" in component):
                        status.append("Deferred")
                    elif ("Pending" in component or "pending" in component or "Under Review" in component or "In Process" in component or "To Dept" in component or "In-progress" in component):
                        status.append("Pending")
                    elif ("Applied" in component or "applied" in component):
                        status.append("Applied")                   
                    else:
                        cleaned_status = component.replace("Status:", "", 1)
                        status.append(cleaned_status)
        else: 
            status.append("not found")

        if "Application Date:" in answers:
            for component in answer_components:
                if "Application Date:" in component:
                    cleaned_application_date = component.replace("Application Date:", "", 1)
                    try:
                        cleaned_application_date = parser.parse(cleaned_application_date)
                    except (TypeError,ValueError):
                        cleaned_application_date = cleaned_application_date
                    application_date.append(cleaned_application_date)
        else: 
            application_date.append("not found")

        if "Decision Date:" in answers:
            for component in answer_components:
                if "Decision Date:" in component:
                    cleaned_decision_date = component.replace("Decision Date:", "", 1)
                    try:
                        cleaned_decision_date = parser.parse(cleaned_decision_date)
                    except (TypeError,ValueError):
                        cleaned_decision_date = cleaned_decision_date
                    decision_date.append(cleaned_decision_date)
        else: 
            decision_date.append("not found")

        if "Education:" in answers:
            for component in answer_components:
                if "Education:" in component:
                    cleaned_education = component.replace("Education:", "", 1)
                    education.append(cleaned_education)
        else: 
            education.append("not found")

        if "Test Scores:" in answers:
            for component in answer_components:
                if "Test Scores:" in component:
                    cleaned_test_scores = component.replace("Test Scores:", "", 1)
                    test_scores.append(cleaned_test_scores)
        else: 
            test_scores.append("not found")

        if "Experience:" in answers:
            for component in answer_components:
                if "Experience:" in component:
                    cleaned_experience = component.replace("Experience:", "", 1)
                    experience.append(cleaned_experience)
        else: 
            experience.append("not found")

        if "Comments:" in answers:
            for component in answer_components:
                if "Comments:" in component:
                    cleaned_comments = component.replace("Comments:", "", 1)
                    comments.append(cleaned_comments)
        else: 
            comments.append("not found")


    answers_df["Status"] = status
    answers_df["Application Date"] = application_date
    answers_df["Decision Date"] = decision_date
    answers_df["Education"] = education[:(len(answers_df))]
    answers_df["Test Scores"] = test_scores[:(len(answers_df))]
    answers_df["Experience"] = experience[:(len(answers_df))]
    answers_df["Comments"] = comments[:(len(answers_df))]

    # print(answers_df.head())
    answers_df.to_csv("data_collected/cleaned_answers.csv")



def analyze():
    cleaned_answers_df = pd.read_csv("data_collected/cleaned_answers.csv")
    print(cleaned_answers_df.head())

    total_clean_answers = len(cleaned_answers_df)
    print("Total Clean Answers: " + str(total_clean_answers))

    # Analyzing Success Rates    
    status_metrics = cleaned_answers_df.groupby(['Status']).count()['term']
    status_metrics_df = pd.DataFrame(status_metrics)
    status_metrics_df = status_metrics_df.rename(columns={'term':'Applicants'})
    status_metrics_df['Percentage'] = 100*status_metrics_df['Applicants']/total_clean_answers
    print("Success Metrics:\n")
    print(status_metrics_df.head())
    plt.figure()
    status_metrics_chart = status_metrics_df['Percentage'].plot.bar().set_title('Percentage Success Rate of Given Applicants')
    plt.savefig("graphs/Status_metrics_chart.png", bbox_inches='tight')

    # Analyzing Comments    
    combined_string = ""
    for comment in cleaned_answers_df['Comments']:
        combined_string += str(comment) + " "

    wordcloud = WordCloud(min_font_size=2,width=600, height=400).generate(combined_string)
    wordcloud.to_file("graphs/comments_wordcloud.png")

    sentiment = []
    for i, r in cleaned_answers_df.iterrows():
        sentence = str(r["Comments"])
        snt = analyser.polarity_scores(sentence)
        sentiment.append(snt['compound'])

    cleaned_answers_df['Comment Sentiments'] = sentiment
    sentiment_df = cleaned_answers_df.loc[cleaned_answers_df['Comment Sentiments'] != 0]
    # sentiment_df = sentiment_df['Comment Sentiments'].mean()
    # print(sentiment_df)


    sentiment_df = pd.DataFrame(sentiment_df.groupby(['term']).mean())
    print(sentiment_df)
    plt.figure()
    comment_sentiment_chart = sentiment_df['Comment Sentiments'].plot.bar().set_title('Comment Sentiments (between -1 and 1) by Application Term')
    plt.savefig("graphs/Comment_sentiments_by_term.png", bbox_inches='tight')


    #Analyzing Response Times to Application
    term = []
    date_diff = []
    row_num = []
    decision = []

    for i, r in cleaned_answers_df.iterrows():
        dec_time = r['Decision Date']
        app_time = r['Application Date']
        try: 
            dec_time_ = datetime.strptime(r['Decision Date'][:10], '%Y-%m-%d')
            app_time_ = datetime.strptime(r['Application Date'][:10], '%Y-%m-%d') 

            difference = dec_time_ - app_time_
            difference = str(difference)
            head, sep, tail = difference.partition('day')
            date_diff.append(abs(int(head)))
            term.append(r['term'])
            decision.append(r['Status'])
            row_num.append(str(dec_time) + " minus "+ str(app_time))

        except:
            None


    Response_time_df = pd.DataFrame(term)
    Response_time_df['Time Taken for Decision'] = date_diff
    Response_time_df['Row num'] = row_num
    Response_time_df['Decision'] = decision


    Response_time_df = Response_time_df.loc[(Response_time_df['Time Taken for Decision'] < 299)]
    Response_time_df['term'] = Response_time_df[0]

    response_metrics_df = pd.DataFrame(Response_time_df.groupby(['term']).mean())
    print(response_metrics_df)
    plt.figure()
    status_metrics_chart = response_metrics_df['Time Taken for Decision'].plot.bar().set_title('Decision Time (in days) by Application Term')
    plt.savefig("graphs/Response_time_by_term.png", bbox_inches='tight')



    response_decision_metrics_df = pd.DataFrame(Response_time_df.groupby(['Decision']).mean())
    print(response_decision_metrics_df)
    plt.figure()
    status_metrics_chart = response_decision_metrics_df['Time Taken for Decision'].plot.bar().set_title('Decision Time (in days) by Application Decision')
    plt.savefig("graphs/Response_time_by_decision.png", bbox_inches='tight')


get_raw_answers()

clean_answers()

analyze()

