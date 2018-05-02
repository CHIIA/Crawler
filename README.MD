# Submodule for CHIIA-NLP

## Introduction

Scrapy is an application framework written for crawling web site data and extracting structured data. It is a fast, high-level screen capture and web crawler framework developed in Python for grabbing web sites and extracting structured data from pages. Scrapy is widely used for data mining, monitoring and automated testing.
This system use headless chrome for login, Scrapy framework for crawling Fectiva database data and store them into MongoDB.

## Architecture Design

![Architecture](https://github.com/CHIIA/Crawler/blob/master/DOCS/images/function_design.png)

## Sequence Diagram

![Sequence](https://github.com/CHIIA/Crawler/blob/master/DOCS/images/sequence_diagram.png)

## Progress

![Progress](https://github.com/CHIIA/Crawler/blob/master/DOCS/images/progress.png)

## Environment Setup
> source venv/bin/activate

## Package installation
> pip install -r requirement.txt

## Run web crawler
> scrapy runspider spiders/fectiva.py

## Database
* set mongo database directory to Crawler/CHIIA/database
* use visual tools such as Robo3T(Mac) or other tools to visualize test data

> mongod --dbpath ./database


## Directory Structure

<pre>
project                                   scrapy module dirs
├── CHIIA
│   ├── __init__.py
│   ├── chromedriver                      headless chrome driver for whole platforms
│   │   ├── linux_chromedriver
│   │   ├── mac_chromedriver
│   │   └── win_chromedriver.exe
│   ├── cookies.py                        get cookie's api
│   ├── database                          sample mongodb data storage for server test
│   ├── items.py
│   ├── middlewares.py                    download midware
│   ├── pipelines.py                      data pipeline using for yield structure data
│   ├── settings.py
│   ├── spiders
│   │   └── fectiva.py                    core spider for crawl data from fectiva
│   └── user_agents.py
├── README.MD
├── requirements.txt                      package list
├── scrapy.cfg                            module description
└── venv                                  environment configuration

