#!/bin/env python
import requests
import datetime
from datetime import date, time, datetime
import time
import locale
import json
import boto3
locale.setlocale( locale.LC_ALL, '' )
'English_United States.1252'


def lambda_handler(event, context):
    relevant_batches = []
    genfund_total = 0
    s3 = boto3.resource('s3')
    object = s3.Object(s3_bucket, 'avg.json')
    sc_session = simplechurch_auth(sc_user, sc_pass, sc_baseurl)
    relevant_batches = get_batches(sc_session, sc_baseurl, relevant_batches)
    ytd_offering = get_batch_detail(sc_session, sc_baseurl, relevant_batches, genfund_total)
    avg = {}
    avg["Average_Offering"] = calculate_avg(ytd_offering)
    object.put(Body=(bytes(json.dumps(avg).encode('UTF-8'))))
    return {
        'statusCode': 200,
        'body': json.dumps(avg)
    }


with open("creds.json", encoding='utf-8') as f:
    credentials = json.load(f)
    sc_user = credentials["sc_user"]
    sc_pass = credentials["sc_pass"]
    sc_baseurl = credentials["sc_baseurl"]
    s3_bucket = credentials["s3_bucket"]


def simplechurch_auth(sc_user, sc_pass, sc_baseurl):
    params = {"username": sc_user, "password": sc_pass}
    response = requests.get('{}user/login'.format(sc_baseurl), params=params)
    session_id = response.json()
    return(session_id["data"]["session_id"])

def get_batches(sc_session, sc_baseurl, relevant_batches):
    today = datetime.today()
    current_year = datetime(today.year, 1, 1, 0, 0)
    current_year_int = (time.mktime(current_year.timetuple()))
    params = {"session_id": sc_session}
    response = requests.get('{}giving/batches'.format(sc_baseurl), params=params)
    batches = response.json()
    for i in batches["data"]:
        batch_date = i["dateReceived"]
        batch_date = time.mktime(datetime.strptime(batch_date, "%Y-%m-%d").timetuple())
        if batch_date > current_year_int:
            relevant_batches.append(i["id"])
    return(relevant_batches)

def get_batch_detail(sc_session, sc_baseurl, relevant_batches, genfund_total):
    today = datetime.today()
    current_year = datetime(today.year, 1, 1, 0, 0)
    current_year_int = (time.mktime(current_year.timetuple()))
    for i in relevant_batches:
        url = ''.join([sc_baseurl, "giving/batch/", str(i)])
        params = {"session_id": sc_session}
        response = requests.get(url, params=params)
        batches = response.json()
        for i2 in batches["data"]["entries"]:
            if i2["category"]["id"] == 1:
                transaction_date = i2["date"]
                transaction_date = time.mktime(datetime.strptime(transaction_date, "%Y-%m-%d").timetuple())
                if transaction_date > current_year_int:
                    genfund_total = genfund_total + i2["amount"]
    return(genfund_total)

def calculate_avg(ytd_offering):
    today = datetime.today()
    week_num = today.strftime("%U")
    return(locale.currency((ytd_offering / int(week_num)), grouping=True)) 


#lambda_handler("test", "test2")
