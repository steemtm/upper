from steem import Steem
from steem.account import Account
from steem.blockchain import Blockchain
from steem.post import Post
from datetime import date
from datetime import datetime
import regex
import time
import csv
import threading
import traceback

# Datetime config
dt = datetime.now()
dh = dt.strftime('%H:%M:%S')
da = date.today()


# Steem instances with account, private posting key and voting weight
acc = 'your_account'
s = Steem(keys='your_posting_key')
c = Account(acc)
w = 100.0


# Lists:
# Read the curators file and make a list 
curators = []
with open('curators', mode='r') as file:
    leitor = csv.reader(file)
    for rows in leitor:
        v = rows[0]
        autores.append(v)
        
# Empty list to receive logs
log_time = []

# Reads the log file and make a list 
log = []
with open('log', mode='r') as inlog:
    leitor2 = csv.reader(inlog)
    for rows in leitor2:
        r = rows[0]
        log.append(r)
        
        
# Set here your flag command without the '!'        
flag = 'flag_command'     


# Blockchain Stream function with filters
def stream():
    REGEX = "(?<=^|(?<=[^a-zA-Z0-9-_\.]))!([A-Za-z]+[A-Za-z0-9]+)" # REGEX code for '!' marker
    blockchain = Blockchain() # blockchain instance
    stream = map(Post, blockchain.stream(filter_by=['comment'])) # stream comments only
    print('\033[37mSearching...')    
    for post in stream:
        curator = post['author']
        p_parent = post['parent_permlink']
        a_parent = post['parent_author']
        f = regex.findall(REGEX, post['body']) # REGEX searches for !'flag'        
        # filters
        if post.is_comment(): 
            if curator in curators:
                if flag in f: 
                    if p_parent in log:
                        continue
                    else:                         
                        # start action thread
                        acaoThread = threading.Thread(target=action, args=(a_parent, p_parent, curator, ))
                        acaoThread.start()

# Function to perfom the actions
def action(a_action, p_action, c_action):
    print(f'\33[31m{da} {dh}: @{a_action}/{p_action} C: {c_action} Queue: {threading.active_count() - 1}')
    time.sleep(3)
    target = '@' + a_action + '/' + p_action
    comment = str(f'Congrats, @{a_action}!\nYour post received an Upper from @{c_action}!')
    try:
        s.commit.vote(target, weight=w, account=acc)
        s.commit.post(title='', body=comentario, author=acc, reply_identifier=target)
        s.commit.resteem(alvo, account=acc)
        print(f'\33[32m{da} {dh}: {target} OK!')
        log.append(p_action)
        log_time.append(f'{da} {dh}: {target}')
    except Exception as error:
        print(repr(error))


if __name__ == "__main__":

    while True:
        try:
            stream()
        except (KeyboardInterrupt, SystemExit):
            print('\033[37mMaking logs...')
            with open('log', mode='a') as l:
                for item in log:
                    l.write(f'{item}\n')
            with open('logtime', mode='a') as lt:
                for itemt in log_time:
                    lt.write(f'{itemt}\n')
            print('\033[37mBye!')
            break
        except Exception as e:
            traceback.print_exc(e)
            print('\033[37mSearching...')
