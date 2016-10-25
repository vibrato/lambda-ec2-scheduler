# Request:
#   Please schedule the EC2 instances to start at 7AM and stop at 7PM Monday to Friday.
#   They are not required on the weekends.
# Tags:
#   Scheduler:Start   H:7 M:00 DOW:01234
#   Scheduler:Stop    H:19 M:00 DOW:01234
#
# Note: Day Of Week (DOW) - Monday is 0 and Sunday is 6.
#       M T W T F S S
#       0 1 2 3 4 5 6
#
# XXX: Does not support minute granularity
# TODO: logging

START_TAG = 'Scheduler:Start'
STOP_TAG = 'Scheduler:Stop'
TIMEZONE = 'Australia/Melbourne'
FILTERS = [ {
    'Name': 'tag:Business:Application',
    'Values': ['something-useless']
} ]

import boto3
import datetime
import logging
import pytz
import re

ec2 = boto3.resource('ec2')

def filter_instances(tag, state):
    filters = FILTERS + [ {
        'Name': 'tag-key',
        'Values': [tag]
    }, {
        'Name': 'instance-state-name',
        'Values': [state]
    } ]
    return ec2.instances.filter(Filters=filters)

def _split(a,b=None): return a,b
def _splitter(v): return _split(*v.split(':'))

def _parser(value):
    for item in re.split(' *', value):
        yield _splitter(item)

def get_tag(tag_key, tags={}):
    for tag in tags:
        if tag['Key'] == tag_key:
            return tag['Value']

def parse_tag_value(value):
    data={'DOW': None, 'H': None, 'M': None} # defaults
    data.update(dict(_parser(value)))
    return data

def find_instances(tag, state, hour, dow):
    tagged = filter_instances(tag, state)
    for i in tagged:
        print i,
        info = parse_tag_value(get_tag(tag, i.tags))
        print info,
        if info['DOW'] is not None and str(dow) in info['DOW']:
            print 'DOW match.',
            if info['H'] is not None and str(hour) == info['H']:
                print 'H match.',
                print 'perform action'
                yield i
        print

def lambda_handler(event, context):
    tz = pytz.timezone(TIMEZONE)
    now = datetime.datetime.now(tz)
    currentHour = now.hour
    currentDOW = now.weekday()

    # Stop first, this may slightly save cost (if going over EC2 usage hour)
    print 'looking for: H', currentHour, 'DOW', currentDOW
    print 'to stop:'
    for inst in find_instances(STOP_TAG, 'running', currentHour, currentDOW):
        print inst.stop()
    print 'to start:'
    for inst in find_instances(START_TAG, 'stopped', currentHour, currentDOW):
        print inst.start()
