import os,sys
result = open('result.txt', 'w')


for i in range(255):
    ip = '192.168.51.%s' % i
    print(ip, 'Scanning')
    result.write(ip)
    os.system('nmap -p 80 %s >> result.txt' % ip)
    result.flush()

result.close()