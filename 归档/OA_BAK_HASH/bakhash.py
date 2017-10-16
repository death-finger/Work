import hashlib, time, os

file_list_all = os.listdir(r'd:\MYOA\bak\TD_OA')
#file_list_all = os.listdir(r'd:\pytest')
file_list_zip = []

def CalcMD5(filepath):
    with open(filepath,'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        hash = md5obj.hexdigest()
        print(hash)
        return hash

for file in file_list_all:
    if file[-3:] == 'zip':
        file_list_zip.append(file)

file_new = sorted(file_list_zip)[-1]
file_day = file_new[:8]

if not ( int(file_day[:4]), int(file_day[4:6]), int(file_day[6:]) ) == time.localtime()[0:3]:
    os.system('echo "Not Backuped Today"')
else:
    md5 = CalcMD5(os.path.join(r'd:\MYOA\bak\TD_OA', file_new))
    os.system('echo %s' % md5)