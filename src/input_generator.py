import random, datetime
import json, argparse
import os

def argument_parser():
    # Parse the given arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="input data")
    # parser.add_argument("-o", help="output data")
    # parser.add_argument("-x", help="top x")
    args = parser.parse_args()
    return args

def inputGenerator(eventCounts=500, totalCustomer=10):
    events = list()

    for i in xrange(eventCounts):
        # random.seed() 
        year = random.randint(2006, 2017)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        hour = random.randint(0,23)
        m = random.randint(0,59)
        sec = random.randint(0,59)
        eventTime = datetime.datetime(year, month, day, hour, m, sec)

        eventType = random.choice(['CUSTOMER', 'SITE_VISIT', 'IMAGE','ORDER'])
        # eventType = random.choice(['CUSTOMER'])
        if eventType == 'CUSTOMER':
            event = {'type': eventType,
                    'verb': random.choice(['NEW','UPDATE']),
                    'key': random.randint(0, totalCustomer),
                    'event_time': eventTime.isoformat(),
                    'last_name': None,
                    'adr_city': None,
                    'adr_state':None
            }
            events.append(event)
        elif eventType == 'SITE_VISIT':
            event = {'type': eventType,
                    'verb': 'NEW',
                    'key': random.randint(0, 100),
                    'event_time': eventTime.isoformat(),
                    'customer_id': random.randint(0, totalCustomer),
                    'tags': list()
            }
            events.append(event)
        elif eventType == 'IMAGE':
            customerID = random.randint(0, totalCustomer)
            visitEvent = {'type': 'SITE_VISIT',
                        'verb': random.choice(['NEW','UPDATE']),
                        'key': random.randint(0, 100),
                        'event_time': eventTime.isoformat(),
                        'customer_id': customerID,
                        'tags': list()
            }
            events.append(visitEvent)

            imageEventTime = eventTime + datetime.timedelta(minutes = 10)
            imageEvent = {'type': 'IMAGE',
                        'verb': 'UPLOAD',
                        'key': random.randint(0, 100),
                        'event_time': imageEventTime.isoformat(),
                        'customer_id': customerID,
                        'camera_make': None,
                        'camera_model': None
            }
            events.append(imageEvent)

        elif eventType == 'ORDER':
            customerID = random.randint(0, totalCustomer)
            visitEvent = {'type': 'SITE_VISIT',
                        'verb': random.choice(['NEW','UPDATE']),
                        'key': random.randint(0, 100),
                        'event_time': eventTime.isoformat(),
                        'customer_id': customerID,
                        'tags': list()
            }
            events.append(visitEvent)

            orderEventTime = eventTime + datetime.timedelta(minutes = 10)
            dollar = random.randint(1,100)
            cent = random.randint(0,99)
            cost_str = str(dollar) + "." + str(cent) + " USD"
            
            orderEvent = {'type': 'ORDER',
                        'verb': random.choice(['NEW','UPDATE']),
                        'key': random.randint(0, 100),
                        'event_time': orderEventTime.isoformat(),
                        'customer_id': customerID,
                        'total_amount': cost_str
            }
            events.append(orderEvent)
        else:
            print "Unrecognized event type: ", eventType
    events = json.dumps(events, indent=4)
    return events

def main():
    args = argument_parser()
    events_file = args.i
    events_data = inputGenerator()
    file_path = os.getcwd() + '/' + events_file
    print file_path
    with open(file_path, 'w') as f:
        f.write(events_data)

main()

