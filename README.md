# Sfly-Customer-Lifetime-Value
Coding challenge from shutterfly.

## Overview
Calculate simple LTV using equation: `52(a) x t`. `t` is 10 years here. `a` = customer expenditures per visit (USD) x number of site visits per week. A customer's expenditures is the sum of all expenditures of this customer, and the time of visit can be extracted from all his/her visit events. The timeframe is calculated by substracting the earliest time from the latest time, which are recorded from all event times.

## Running
Run the script from the project home directory as given in the sample example:
`python src/shutterfly_ltv.py -i input/events.txt -x 5 -o output/output.txt`

You can change value of x to fetch top x customers with the highest ltv.

You can also generate test data (default 500 events and 10 customers, you can change it in the file) by running
`python src/input_generator.py -i input/events.txt`


##Assumptions:
1. For each event, the headers would always be present even if the value is null
Example: you will always have field tags in site visit even if it is null
2. All amounts are in USD
3. You cannot place an order when you haven't visited the website

## Design Decisions & Performance
Used `Pandas` data frames to store and filter events data
It will be faster solution keeping in mind that events data can be large and then even dictionary will be slow as the data grows.

  

## Requirements
* pandas

It can be installed using:
`pip install pandas`

