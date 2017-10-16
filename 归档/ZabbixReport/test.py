import mysql.connector
import time, datetime
host_sh = open('host-shanghai.txt', 'r')
host_hz = open('host-hangzhou.txt', 'r')
test = open('test', 'r')
result = open('result_win.txt', 'w')

date_raw_1 = "2017-05-01"
date_raw_2 = "2017-05-07"
host_list = test



date_1 = datetime.datetime.strptime(date_raw_1,'%Y-%m-%d')
date_2 = datetime.datetime.strptime(date_raw_2,'%Y-%m-%d')
sep = '=' * 32
date_count = (date_2 - date_1).days
time_template = "( SELECT UNIX_TIMESTAMP('%s 00:00:00') ) AND ( SELECT UNIX_TIMESTAMP('%s 23:59:59') )"

cnx = mysql.connector.connect(user='joshua', password='bagakira',
                              host='192.168.1.144', database='zabbix')
cursor = cnx.cursor()


def get_gen_stats(hostlist, time_period):
    for host in hostlist.readlines():
        # Hostid
        host = host.rstrip()
        query_hostid = "SELECT hostid FROM hosts WHERE name='%s'" % host
        cursor.execute(query_hostid)
        host_result = cursor.fetchall()[0][0]

        # Online Rate %
        # Sum
        query_online_id = "SELECT itemid FROM items WHERE hostid='%s' AND name='agent ping'" % host_result
        cursor.execute(query_online_id)
        online_id = cursor.fetchone()[0]
        query_online_sum = "SELECT SUM(value) FROM history_uint WHERE itemid=%s AND clock BETWEEN %s" % (
        online_id, time_period)
        cursor.execute(query_online_sum)
        online_sum = cursor.fetchone()[0]
        # Count
        query_online_count = "SELECT COUNT(value) FROM history_uint WHERE itemid=%s AND clock BETWEEN %s" % (
        online_id, time_period)
        cursor.execute(query_online_count)
        online_count = cursor.fetchone()[0]
        # Rate
        online_rate = online_sum / online_count

        # CPU Load
        query_cpu_load_id = "SELECT itemid FROM items WHERE hostid='%s' AND name='Processor load (15 min average)'" % host_result
        cursor.execute(query_cpu_load_id)
        cpu_load_id = cursor.fetchone()[0]
        query_cpu_load = "SELECT AVG(value) FROM history WHERE itemid=%s AND clock BETWEEN %s" % (
        cpu_load_id, time_period)
        cursor.execute(query_cpu_load)
        cpu_load = cursor.fetchone()[0]

        # Free Memory
        query_mem_free_id = ("SELECT itemid FROM items WHERE hostid='%s' AND name='Free memory'" % host_result)
        cursor.execute(query_mem_free_id)
        mem_free_id = cursor.fetchone()[0]
        query_mem_free = ("SELECT AVG(value)/1048576 FROM history_uint WHERE itemid=%s AND clock BETWEEN %s"
                          % (mem_free_id, time_period))
        cursor.execute(query_mem_free)
        mem_free = cursor.fetchone()[0]

        # Memory Rate
        query_mem_total_id = ("SELECT itemid FROM items WHERE hostid='%s' AND name='Total Memory'" % host_result)
        cursor.execute(query_mem_total_id)
        mem_total_id = cursor.fetchone()[0]
        query_mem_total = "SELECT AVG(value)/1048576 FROM history_uint WHERE itemid=%s AND clock BETWEEN %s" % (
        mem_total_id, time_period)
        cursor.execute(query_mem_total)
        mem_total = cursor.fetchone()[0]
        mem_rate = mem_free / mem_total

        # Disk Read
        query_disk_read_id = (
        "SELECT itemid FROM items WHERE hostid='%s' AND name='File read bytes per second'" % host_result)
        cursor.execute(query_disk_read_id)
        disk_read_id = cursor.fetchone()[0]
        query_disk_read = ("SELECT AVG(value)/1024 FROM history WHERE itemid=%s AND clock BETWEEN %s"
                           % (disk_read_id, time_period))
        cursor.execute(query_disk_read)
        disk_read = cursor.fetchone()[0]

        # Disk Write
        query_disk_write_id = (
        "SELECT itemid FROM items WHERE hostid='%s' AND name='File write bytes per second'" % host_result)
        cursor.execute(query_disk_write_id)
        disk_write_id = cursor.fetchone()[0]
        query_disk_write = ("SELECT AVG(value)/1024 FROM history WHERE itemid=%s AND clock BETWEEN %s"
                            % (disk_write_id, time_period))
        cursor.execute(query_disk_write)
        disk_write = cursor.fetchone()[0]

        print(host, online_rate, cpu_load, mem_free, mem_rate, disk_read, disk_write, sep="\n")
        result.write("%s\n%s\n%s\n%s\n%s\n%s\n" % (online_rate, cpu_load, mem_free, mem_rate, disk_read, disk_write))
        result.flush()

        # Disk Search
        query_item_list = ( "SELECT itemid,name,key_ FROM items WHERE hostid=%s" % host_result )
        cursor.execute(query_item_list)
        item_list = cursor.fetchall()
        disk_list = []
        for i in item_list:
            if i[2][:11] == 'vfs.fs.size' and i[2][-8:] == ':,pfree]':
                disk_list.extend(i)
        while disk_list:
            item_id, item_name, item_key = disk_list[:3]
            disk_list = disk_list[3:]
            query_disk_usage = ( "SELECT AVG(value)/100 FROM history WHERE itemid=%s and clock between %s"
                                 % (item_id, time_period) )
            cursor.execute(query_disk_usage)
            disk_usage = cursor.fetchone()[0]
            print(disk_usage)
            result.write("%s\n" % disk_usage)
            result.flush()


#date_tmp = date_1
#for i in range(0, date_count+1):
#    time_period = time_template % (date_tmp.strftime('%Y-%m-%d'), date_tmp.strftime('%Y-%m-%d'))
#    print(sep, date_tmp)
#    result.write(sep)
#    result.write("\n%s\n" % date_tmp)
#    get_gen_stats(host_list, time_period)
#    host_list.seek(0)
#    date_tmp = date_tmp + datetime.timedelta(days=1)


host_list.seek(0)
time_all = time_template % (date_raw_1, date_raw_2)
result.write(sep + 'All\n')
get_gen_stats(host_list, time_all)

result.flush()
result.close()
print('Done')