import time,os
list = open(r'list.txt')

for i in list.readlines():
    name = i.split('=')
    name = name[-1].rstrip()
    day = time.localtime()
    day = '%s-%s-%s' % (day[0], day[1], day[2])
    i = i.replace(r'&', r'\&').rstrip()
    cmd = 'wget --http-user=pubinxin --http-password=pubinxin %s -O %s-%s.xls' % (i, name, day)
    os.system(cmd)