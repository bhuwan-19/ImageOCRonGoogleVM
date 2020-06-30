# OCR_Punjabi

## Overview

This project is to extract Punjabi text from various kinds of images using Google Vision API.
Storage for this module is in Google Cloud Storage, which contains up to 170,000 jpg files.
This project is deployed in Google Cloud Virtual Machine using Flask.

## Structure

- credential

    The credential keys to use Google Vision API and Google Cloud Storage.

- src

    The source code for this project.
    
- static

    The javascript code for web site of this project.

- templates

    The source code for web site.
    
- utils

    The source code to manage the folders and files in this project and process images.

- main

    The main execution file.
    
- requirements

    All the dependencies for this project.
    
- settings

    The variable settings for this project.
    
- app, OCR_Punjabi, wsgi

    The source code to deploy this project into Google Cloud Virtual machine.

## Installation

- Environment

    Ubuntu 18.04, Python 3.6
    
- Dependency Installation(Local)

    Please go ahead to the project directory and run the following commands

    ```
        pip3 intall -r requirments.txt
    ```
    
## Execution

- Virtual Machine

    Now this project is deployed in 34.67.236.180, so when you type 34.67.236.180 in browser, you can see the web site to 
    extract the Punjabi text from the images.
    
    When you insert directory url, this project parses all the jpeg files in it to return results to output directory.
    It is your own selection to insert directory url, but you have to insert as following.
    
    For example,  Images/ or Images/12...
    
    That is to say, it assumes that the input directory is in Buckets/books_data/Books, so you don't need to insert this url 
    "Buckets/books_data/Books", but need only the followed url.
    
    If you click "Submit" button, you can see the progress of OCR and the result which contains json, xml and txt file 
    for each imageis saved in Buckets/books_data/Books/output. 

- Local

    Please go ahead to the project directory and run the following command
    
    ```
        python main.py        
    ```
