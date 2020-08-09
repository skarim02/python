import re
import pprint
import csv
from collections import defaultdict
import operator

user=[]
per_user = dict()
error_dict = dict()

with open(r'loganalyzer.log','r') as f:
    for line in f:
        if 'ERROR' in line:
            line=line.strip()
            error_generated = re.search(r'ERROR: ([\w+ ]*) (\[#\d+\]) \((\w+)\)',line)
            if error_generated:
                get_user=error_generated.group(3)
                error = error_generated.group(1)
                if error not in error_dict:
                    #create keys of errors
                    error_dict[error] = dict()
                    error_dict[error]['Count'] = 0
                error_dict[error]['Count'] += 1

                if get_user not in per_user:
                    per_user[get_user] = dict()
                    per_user[get_user]['Error'] = 0
                    per_user[get_user]['INFO'] = 0
                per_user[get_user]['Error'] += 1

        if 'INFO' in line:
             line=line.strip()
             get_info = re.search(r'(INFO):.*\((\w+)\)', line)
             get_user = get_info.group(2)
             if get_info:
                 if get_user not in per_user:
                     per_user[get_user] = dict()
                     per_user[get_user]['INFO'] = 0
                     per_user[get_user]['Error'] = 0
                 per_user[get_user]['INFO'] += 1
f.close()

sorted(per_user, key=operator.itemgetter(0))
new_list=[]
new_list=[{'Username':k,'INFO':v.get('INFO'),'Error':v.get('Error')} for k,v in per_user.items()]
new_list=sorted(new_list,key= lambda i: i['Username'])

with open('user_statistics.csv','w') as f:
    writer=csv.DictWriter(f,fieldnames=['Username','INFO','Error'])
    writer.writeheader()
    for row in new_list:
        writer.writerow(row)
f.close()

error_list=[{'Error':k,'Count':v.get('Count')} for k,v in error_dict.items()]
error_list=sorted(error_list,key=lambda i:i['Count'],reverse=True)

with open('error_message.csv','w') as file:
    writer = csv.DictWriter(file,fieldnames=['Error','Count'])
    writer.writeheader()
    for row in error_list:
        writer.writerow(row)
file.close()

