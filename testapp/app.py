import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import config

user_dict = {}
user_config = config.BT_USER
for user in user_config.split('/'):
    i = user.split(',')
    user_dict[i[0]]=[i[1],i[2],float(i[3])]
print(user_dict)

MAIL_ACCOUNT = config.MAIL_ACCOUNT
id = MAIL_ACCOUNT.split(',')[0]
password = MAIL_ACCOUNT.split(',')[1]

print(id)
print(password)

LINE_TOKEN = config.LINE_TOKEN
user_dict = {}
for i in LINE_TOKEN.split('/'):
    j = i.split(',')
    user_dict[j[0]]=j[1]
print(user_dict)

bool = os.path.exists('log/log/')
print(bool)
