from time import ctime, time
from getpass import getpass
import random, string, hashlib, datetime

lock_time = 60

def register(user):
    with open('account', 'a+') as acc_file:
        user_list = acc_file.readlines()
        for i in user_list:
            if user in i:
                return 'User %s already registered!' % user
        salt = ''.join(random.sample(string.ascii_letters + string.digits, 16))
        passwd = getpass('Password: ')
        passwd = salt + passwd
        passwd_hashed = hashlib.md5(passwd.encode('utf-8')).hexdigest()
        acc_file.write('%s;%s;%s\n' % (user, salt, passwd_hashed))
        return 'User %s created at %s' % (user, ctime())

def login(user):
    with open('account', 'r') as acc_file, open('locked', 'r+') as acc_lock:
        user_list = acc_file.readlines()
        user_locked = acc_lock.readlines()
        for i in user_locked:
            i = i.rstrip('\n')
            u, t = i.split(';')
            t = int(t)
            end = t + lock_time
            end_date = datetime.datetime.fromtimestamp(end).strftime('%Y/%m/%d-%H:%M:%S')
            if user in u:
                if time() < end:
                    return "User %s is LOCKED till %s" % (user, end_date)
                else:
                    user_locked.pop(user_locked.index(i+'\n'))
                    acc_lock.close()
                    acc_lock = open('locked', 'w')
                    for i in user_locked:
                        acc_lock.write(i + '\n')
                    acc_lock.flush()

        login_cnt = 0
        for i in user_list:
            i = i.rstrip('\n')
            u, s, p = i.split(';')
            if user == u:
                while login_cnt < 5:
                    passwd = getpass('Password: ')
                    passwd = s + passwd
                    passwd_hash = hashlib.md5(passwd.encode('utf-8')).hexdigest()
                    if passwd_hash == p:
                        return 'OK'
                    else:
                        login_cnt += 1
                        print('Password not correct, you still have %d times to try\n' % (5 - login_cnt) )
                print('Failed to login too many times! Account will be locked for %s seconds!' % lock_time)
                acc_lock.write('%s;%s\n' % (user, round(time())))

if __name__ == '__main__':
    login('test')