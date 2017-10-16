import mysql.connector
import time, datetime
hostid = '10200'

date_raw_1 = "2017-07-03"
date_raw_2 = "2017-07-09"


date_1 = datetime.datetime.strptime(date_raw_1,'%Y-%m-%d')
date_2 = datetime.datetime.strptime(date_raw_2,'%Y-%m-%d')
sep = '=' * 32
date_count = (date_2 - date_1).days
time_template = "( SELECT UNIX_TIMESTAMP('%s 00:00:00') ) AND ( SELECT UNIX_TIMESTAMP('%s 23:59:59') )"

cnx = mysql.connector.connect(user='joshua', password='bagakira',
                              host='192.168.1.144', database='zabbix')
cursor = cnx.cursor()

date_tmp = date_1
for i in range(0, date_count+1):
    time_period = time_template % (date_tmp.strftime('%Y-%m-%d'), date_tmp.strftime('%Y-%m-%d'))
    print('\n', date_tmp)

    query_sum = ( "SELECT SUM(value) FROM history_uint WHERE itemid='28532' AND clock BETWEEN %s"
                  % time_period)
    cursor.execute(query_sum)
    online_sum = cursor.fetchone()[0]

    query_total = ( "SELECT COUNT(value) FROM history_uint WHERE itemid='28532' AND clock BETWEEN %s"
                  % time_period)
    cursor.execute(query_total)
    online_total = cursor.fetchone()[0]

    online_rate = 1 - ( online_sum / online_total )

    query_resp = ( "SELECT AVG(value)*1000 FROM history WHERE itemid='28535' AND clock BETWEEN %s"
                  % time_period)
    cursor.execute(query_resp)
    online_resp = cursor.fetchone()[0]

    date_tmp = date_tmp + datetime.timedelta(days=1)

    print(online_rate, online_resp, sep='\n', end='\n===============')


time_period = time_template % (date_raw_1, date_raw_2)
print('\n', "ALL\n")

query_sum = ("SELECT SUM(value) FROM history_uint WHERE itemid='28532' AND clock BETWEEN %s"
             % time_period)
cursor.execute(query_sum)
online_sum = cursor.fetchone()[0]

query_total = ("SELECT COUNT(value) FROM history_uint WHERE itemid='28532' AND clock BETWEEN %s"
               % time_period)
cursor.execute(query_total)
online_total = cursor.fetchone()[0]

online_rate = 1 - (online_sum / online_total)

query_resp = ("SELECT AVG(value)*1000 FROM history WHERE itemid='28535' AND clock BETWEEN %s"
              % time_period)
cursor.execute(query_resp)
online_resp = cursor.fetchone()[0]

print(online_rate, online_resp, sep='\n', end='\n===============')

