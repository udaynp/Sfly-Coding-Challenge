# Shutterfly-Customer-Lifetime-Value
Coding challenge from shutterfly.

## Overview
Calculate simple LTV using equation: `52(a) x t`. `t` is 10 years here. `a` = customer expenditures per visit (USD) x number of site visits per week. A customer's expenditures is the sum of all expenditures of this customer, and the time of visit can be extracted from all his/her visit events. The timeframe is calculated by substracting the earliest time from the latest time, which are recorded from all event times.

## Running
Run the script from the project home directory as given in the sample example:
`python src/ltv.py -i input/events.txt -x 4 -o output/output.txt`

You can change value of x to fetch top x customers with the highest ltv.


## Design Decisions & Performance
Used `Pandas` data frames to store and filter events data
It will be faster solution keeping in mind that events data can be large and then even dictionary will be slow as the data grows.
Rather than doing a full sort on an array, we just selected the N largest or smallest items using nlargest method of pandas which further improved performance.
  

## Requirements
* pandas

It can be installed using:
`pip install pandas`

