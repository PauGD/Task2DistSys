# Task2DistSys
Introduction

In this project we have decided to obtain data about the main 5 vaccines: Pfizer , Moderna , Astrazeneca , Sputnik and CoronaVac. The data will be  processed and uploaded to ibm_cloud so queries can be made on it later.

Architecture  and design

For the execution of functions we will use the serverless functions of ibm_cloud, to make the calls to these functions we will use the lithops framework. Since we want to get tweets we will also use the tweepy library, a python library that facilitates access to the twitter API . For the sentiment analysis of these tweets we will use textblob, an open-source library for processing text .These libraries are not available on ibm_cloud, we will use docker to solve this problem. This platform will allow us to create a custom runtime where we will be able to use the elements mentioned and which can also be used in lithops.

Tweepy allows us to  make queries to  tweets which  contain specific strings. It also allows us to specify the language, mode and number of tweets to be obtained, among other parameters. The queries made  will be the tweets containing the name of the vaccine, written in Spanish and that are not retweets. The search method  only allows us to get 100 tweets per page, we are looking to get 1000 tweets so we will use a cursor that allows us to get the results of 10 pages. After we have collected all the data it will be processed. The process for each tweet  will consist of first getting the text of the tweet and obtaining its sentiment using textblob. After that we will also get the Id, date ,number of retweets and hashtags.  All this data will be written into a csv file named ‘nameofvaccine.csv’.   When we finish processing we will follow the following steps to upload the results to the bucket of the ibm cloud.  We will start by checking if an older file exists in the bucket, if it does we will upload the older file to it with the name ‘old-nameovaccine.csv’. We will continue by uploading three copies of the results so we have backup in case anything fails. The name of the three files will be ‘nameovaccine.csv ‘, ‘01-nameovaccine.csv’ and ‘02-nameovaccine.csv’.

We will utilize the functionexecutor.map() function of lithops which will  enable us to  run concurrent serverless functions for each element of an argument list and wait for their respective results.  The function that will be applied to the arguments will contain the process explained before and the arguments will be the names of each vaccine. So we will have five processes, one for each vaccine name. 

