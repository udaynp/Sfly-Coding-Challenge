#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import os, argparse
import json
import pandas as pd
from datetime import timedelta

def argument_parser():
    # Parse the given arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="input data")
    parser.add_argument("-o", help="output data")
    parser.add_argument("-x", help="top x")
    args = parser.parse_args()
    return args


def fetch_events_from_file(events_file):
    print os.getcwd() + '/' + events_file

    with open(os.getcwd() + '/' + events_file) as input_file:
        events = json.load(input_file)
    return events 
   
        

def TopXSimpleLTVCustomer(x,D):
    
    #Create the required Dataframes
    DF_SITE_VISIT=pd.DataFrame(columns=["customer_id","event_time","key","verb","tags"])
    DF_CUSTOMER=pd.DataFrame(columns=["key","event_time","verb","last_name","adr_city","adr_state"])
    DF_IMAGE=pd.DataFrame(columns=["customer_id","event_time","key","verb","camera_make","camera_model"])
    DF_ORDER=pd.DataFrame(columns=["customer_id","event_time","key","verb","total_amount"])
    
    #The analysis summary Dataframe
    DF_Customer_LTV=pd.DataFrame(columns=["customer_id","start_time","last_time","LTV"])
          
    #Fill the Dataframe according to the record type
    for record in D:
        if record["type"]=="SITE_VISIT":
            DF_SITE_VISIT=DF_SITE_VISIT.append(record,ignore_index=True)
            continue
        
        if record["type"]=="CUSTOMER":
            DF_CUSTOMER=DF_CUSTOMER.append(record,ignore_index=True)
            continue
        
        if record["type"]=="ORDER":
            DF_ORDER=DF_ORDER.append(record,ignore_index=True)
            continue
        
        if record["type"]=="IMAGE":
            DF_IMAGE=DF_IMAGE.append(record,ignore_index=True)
            continue
        
        print "Unsupprted input record: ",record
    
    
    #Calculating LVT for each customer
    for record in DF_CUSTOMER.iterrows():
        
        customer_id=record[1]["key"]
        #get the list of even associated to the customer_id above
        member_time=DF_SITE_VISIT[DF_SITE_VISIT["customer_id"]==customer_id]["event_time"]
        #correct the datetime format
        member_time=pd.to_datetime(member_time)
        
        member_time.sort_values()
    
        member_time=member_time.reset_index()
      
        #Customer with no visit
        if len(member_time)==0:
            rec_tmp={"customer_id":customer_id,"start_time":"","last_time":"","LTV":""}
            DF_Customer_LTV=DF_Customer_LTV.append(rec_tmp,ignore_index=True)
            continue
        
        #customer with only a single visit
        #the calculation could end up with a big LTV number
        #The Problem needs to be redefined for this scenario
        
        if len(member_time)==1: 
            #total spending per visit
            spend_per_visit=DF_ORDER[DF_ORDER["customer_id"]==customer_id]["total_amount"].str[:-3].astype("float").sum()
            
            order_time=member_time.iloc[0][1]
            
          
            LTV=spend_per_visit*52*10
    
            rec_tmp={"customer_id":customer_id,"start_time":order_time,"last_time":"","LTV":LTV}
            DF_Customer_LTV=DF_Customer_LTV.append(rec_tmp,ignore_index=True)
            continue
        
        first_visit=member_time.iloc[0][1]
        last_visit=member_time.iloc[-1][1]
   
        cnt_weeks=-1
        VisitsOrders=0
        
        while (True):
            
            #calculte next week
            next_week= first_visit+timedelta(days=7)
            cnt_weeks+=1
            
            #get the spending in the given week
            #spend_per_week=DF_ORDER[(DF_ORDER["customer_id"]==customer_id) and (pd.to_datetime(DF_ORDER["event_time"])>=first_visit) and (pd.to_datetime(DF_ORDER["event_time"])<=next_week)]["total_amount"].str[:-3].astype("float").sum()
            DF_Get_ID=DF_ORDER[(DF_ORDER["customer_id"]==customer_id)]
            DF_Get_Time0=DF_Get_ID[(pd.to_datetime(DF_Get_ID["event_time"])>=first_visit)]
            DF_Get_Time1=DF_Get_Time0[(pd.to_datetime(DF_Get_Time0["event_time"])<=next_week)]
            spend_per_week=DF_Get_Time1["total_amount"].str[:-3].astype("float").sum()
    
            #calculate the number of the visit in the given week
            #Number_Visits=DF_SITE_VISIT[(DF_SITE_VISIT["customer_id"]==customer_id) and (pd.to_datetime(DF_SITE_VISIT["event_time"])>=first_visit) and (pd.to_datetime(DF_SITE_VISIT["event_time"])<=next_week)]["event_time"].count()
            DF_Visits_ID=DF_SITE_VISIT[(DF_SITE_VISIT["customer_id"]==customer_id)]
            DF_Visits_Time0=DF_Visits_ID[(pd.to_datetime(DF_SITE_VISIT["event_time"])>=first_visit)]
            DF_Visits_Time1=DF_Visits_Time0[(pd.to_datetime(DF_SITE_VISIT["event_time"])<=next_week)]
            Number_Visits=DF_Visits_Time1["event_time"].count()
    
    
            #accumulate the orders per weeks
            VisitsOrders+=spend_per_week*Number_Visits #
            
            #last week
            if (next_week>last_visit):
                
                LTV=(VisitsOrders/cnt_weeks)*52*10.0
                rec_tmp={"customer_id":customer_id,"start_time":first_visit,"last_time":last_visit,"LTV":LTV}
                DF_Customer_LTV=DF_Customer_LTV.append(rec_tmp,ignore_index=True)
                break
            
          
            first_visit=next_week
        
    #print DF_Customer_LTV
    DF_Customer_LTV=DF_Customer_LTV.reset_index()
    #DF_Customer_LTV.sort_values(by=["LTV"])
    DF_Customer_LTV.nlargest(x, "LTV")
    DF_Customer_LTV= DF_Customer_LTV.sort_values(by=["LTV"],ascending=False)
    DF_Customer_LTV=DF_Customer_LTV.reset_index()
    #print DF_Customer_LTV
    return DF_Customer_LTV.iloc[0:x,2:]
    #DF_Customer_LTV.to_csv("Customer_LTV_Summary.csv")          
 
    
def main():
    args = argument_parser()
    events_file = args.i
    x = int(args.x)
    events_data = fetch_events_from_file(events_file)
    #print events_data
    df = TopXSimpleLTVCustomer(x,events_data)
    print df
    output_file = open(os.getcwd() + '/' + args.o, 'w')
    output_file.write(df.to_string())
    output_file.close()    
      
            
if __name__ == '__main__':
    main()
#    
    
   