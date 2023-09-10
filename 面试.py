
import re
from unicodedata import decimal
import time
import glob
import linecache

def domainName():
    num = 0
    dn_dict = "https://domain1.com"
    patten = '(http|https)://[a-z]+.[a-z0-9]+.[a-zA-Z]+'
    f = open('files/access.log','r')
    for line in f:
        Domain_Name = re.search(patten,line.split()[10])
        if Domain_Name:
            dn = Domain_Name.group(0)
            if dn == dn_dict:
                num += 1
    print(num)
    return num

#domainName()



ip_regex = r"?P<ip>[\d.]*"
date_regex = r"?P<date>\d+"
month_regex = r"?P<month>\w+"
year_regex = r"?P<year>\d+"
day_time_regex = r"?P<day_time>\S+"
method_regex = r"?P<method>\S+"
request_regex = r"?P<request>\S+"
status_regex = r"?P<status>\d+"
body_bytes_regex = r"?P<body_bytes>\d+"


def parse_log(log_line):
    """
    解析日志，日志格式： 199.120.110.21 - - [01/Jul/1995:00:00:09 -0400] "GET /shuttle/missions/sts-73/mission-sts-73.html HTTP/1.0" 200 4085
    """
    log_fmt = r"(%s)\ - \ -\ \[(%s)/(%s)/(%s)\:(%s)\ [\S]+\]\ \"(%s)?[\s]?(%s)?.*?\"\ (%s)\ (%s)\s"
    p = re.compile(log_fmt % (
    ip_regex, date_regex, month_regex, year_regex, day_time_regex, method_regex, request_regex, status_regex,
    body_bytes_regex),re.VERBOSE)
    return re.search(p, log_line)


def parse_time(date, month, year, log_time):
    """转化为时间戳，整形，单位秒"""
    time_str = '%s%s%s %s' % (year, month, date, log_time)
    return int(time.mktime(time.strptime(time_str, '%Y%b%d %H:%M:%S')))

def statusNum(time):
    num_200 = 0
    num_other = 0
    with open('files/access.log', mode='r', encoding='utf-8') as file_object:
        for line in file_object:
           matches = parse_log(line)
           status = line.split(" ")[8]
           date = matches.group("date")
           month = matches.group("month")
           year = matches.group("year")
           day_time = matches.group("day_time")
           ctime = parse_time(date, month, year, day_time)
           print(ctime)
           if ctime == time:
               if int(status) == 200:
                   num_200 += 1
               else:
                   num_other += 1
    return decimal(num_200 / (num_200 + num_other))

