# ImageOCR

## Overview

This project is to extract the Punjabi text from various kinds of images using Google Vision API.
The storage for this module is in Google Cloud Storage, which contains up to 170,000 jpg files.
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
   
## Installation

- Environment

    Ubuntu 18.04, Python 3.6
    
- Dependency Installation(Local)

    Please go ahead to the project directory and run the following commands

    ```
        pip3 intall -r requirments.txt
    ```
    
## Execution

- Please go ahead to the project directory and run the following command
    
    ```
        python main.py        
    ```
