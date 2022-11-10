
#!/bin/env python3
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import configparser
import os, sys
import csv
import traceback
import time
import random
import setup 

re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"
pu="\033[0;35m"
ye="\033[0;33m"

def banner():
    print(f""" {cy}
             `-hh+                                
             s.`omm+:o/.                          
            `h-```:/.+yyysss+-`                   
          ./+y/-..```.....-:sdms-                 
          /h--```  ``.-.`````-oNNo                
         .o++:.```.--.``--.``.-yMM/               
        -so+:`.::-.`     `..::./MMh               
        y+:` -////-        .::-`mMN`              
       .y`  `-ooyhs.    ` `-oyy:hMM:              
       /:   `:o`.mN+ .-----/.-MoyMM+              
       s`    .yhmyh--:-::----/y:/MMy              
      ::      `-:-`.:---------. `oMN/+yo.         
     -o.           `///:------` `yMN  +MMo-`      
     .my-           `-:+++//:- -yMMy  ``.-sMd-    
     `sdyh+:.               .:oyhho  `.````hMN.   
    .ys.-syyyso+/:--....-:/oyyyyyy/  .```` +MMy   
   -hs/osyyyyyyyyyyyyyyyyyyyyyyyyys` .`````sMMy   
  `hy`/yyyyyyyo/s++++yyyyyyyyyyydmmh/:-..-sMMM:   
  :Nh/oyyyyyyyyyyyyyyyyyyyyyyyysNMMMMNNmmNMMm+    
  `ymNmyo:--/oossyyyyyyyyyyyoooyMMN--:+syso:.     
    `-ms     -oo+yyyyyyyyyysossNMMs               
      :d-````oyyyyyyyyyyyyyyyymMMm`               
       hNso/oyyyyyyyyyyyyyyyyhMMM:                
       `smyooyyyyhmNNNdhhyssdMMMy                 
        `m/::/dmmMMMNdNNd+//ohMM:                 
         hMMMMMMMmh/` .omMMMMMMMo  {cy}               
        """)
    

cpass = configparser.RawConfigParser()
cpass.read('config.data')

try:
    api_id = cpass['cred']['id']
    api_hash = cpass['cred']['hash']
    phone = cpass['cred']['phone']
    client = TelegramClient(phone, api_id, api_hash)
except KeyError:
    os.system('clear')
    banner()
    print(re+"[!] run python3 setup.py first !!\n")
    sys.exit(1)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    os.system('clear')
    banner()
    client.sign_in(phone, input(gr+'[+] Enter the code: '+re))
 
os.system('clear')
banner()
input_file = sys.argv[1]
users = []
with open(input_file, encoding='UTF-8') as f:
    rows = csv.reader(f,delimiter=",",lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        user['access_hash'] = int(row[2])
        user['name'] = row[3]
        users.append(user)
 
chats = []
last_date = None
chunk_size = 200
groups=[]
 
result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))

chats.extend(result.chats)
 
for chat in chats:
    try:
        if chat.megagroup== True:
            groups.append(chat)
    except:
        continue

i=0
for group in groups:
    print(gr+'['+cy+str(i)+gr+']'+cy+' - '+group.title)
    i+=1

print(gr+'[+] Choose a group to add members')
g_index = input(gr+"[+] Enter a Number : "+pu)
target_group=groups[int(g_index)]
 
target_group_entity = InputPeerChannel(target_group.id,target_group.access_hash)
 
print(gr+"[1] add member by username\n[2] add member by user ID ")
mode = int(input(gr+"Input : "+pu)) 

n = 0

for user in users:
    n += 1
    if n % 50 == 0:
     print(ye+"Reach the limit, waiting for 900 Seconds...")
     sleep(900)
    try:
        print (cy+"Adding {}".format(user['id']))
        if mode == 1:
            if user['username'] == "":
                continue
            user_to_add = client.get_input_entity(user['username'])
        elif mode == 2:
            user_to_add = InputPeerUser(user['id'], user['access_hash'])
        else:
            sys.exit("Invalid Mode Selected. Please Try Again.")
        client(InviteToChannelRequest(target_group_entity,[user_to_add]))
        print(ye+"Waiting for 20-60 Seconds...")
        time.sleep(random.randrange(20, 60))
    except PeerFloodError:
        print(re+"Oops! Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
    except UserPrivacyRestrictedError:
        print(re+"The user's privacy settings do not allow you to add. Skipping.")
    except:
        traceback.print_exc()
        print(re+"Unexpected Error!")
        continue
