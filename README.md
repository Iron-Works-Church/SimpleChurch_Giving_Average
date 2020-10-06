# SimpleChurch_Giving_Average
SimpleChurch CRM is a powerful Church Management Software suite to keep track of members, giving, and attednance.  This script will calculate the weekly average giving in the general fund (fund id: 1) for calendar year to date.  It has been written be run on an AWS Lambda Function in Python 3.8 and is configured to write the output to an AWS S3 bucket as "avg.json".  

Our church uses a Google Sheet with the ImportJSON() function to dynamically update our financial stats from this data.

Here are the installation steps:


1.  Edit creds.json to include your SimpleChurch username, password, and URL.  Also include your AWS S3 bucket name.

2.  Create an AWS Lambda function that includes write permissions to your s3 bucket.

3.  Create a file on s3 called "avg.json" and make it public so that it can be accessed from the web.

4.  Schedule CloudWatch or use API Gateway to manually call your lambda function on a scheudle.
