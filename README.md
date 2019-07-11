Upper
---
reads every new comment made by authors in a list and searches for the flag(!command) who will trigger actions on the **main post**(e.g. upvote, comment, and resteem)

Introduction
---
A steemian friend asks me to help him with his project, a curation project with several curators reading and approving posts. He needs to automate tasks (upvote, comment, and resteem). As it may be useful to others I decided to open source and post it.

Upper is a simple python script following basic instructions from the steem-python official library, plus a few things I've added. 


---

**Requirements**
 - Python 3.6+
- Steem-Python
- Regex
- Linux (Ubuntu)
---

**Install**
*Always best to create a venv or use idle like pycharm*

Installing steem-python and regex:
```
pip3 install regex
pip3 install steem
```

Clone repository:
```
git clone https://github.com/lpessin/upper.git
```
---
**Setup & usage**

Open *curators* file, and add accounts you wish to search for comments with the flag(!command):
```
lpessin
acc2
acc3
...
```

Now edit upper.py to set-up the worker account:

```
acc = 'your_account' 
s = Steem(keys='your_posting_key')

w = 100.0 # set the vote weight you want
```

Choose your flag (!up as default):

```
# Set here your flag command without the '!'        
flag = 'up'   
```
Write the comment you want to post (markdown supported):
```
comment = str(f'Congrats, @{a_action}!\nYour post received an Upper from @{c_action}!')
```
<center>'{a_action}' is the main post author, and '{c_action}' is the curator</center>

And finally, run:
```
python3 upper.py
```
Now whenever a listed curator types '!up'(or the flag you chose) inside a comment, your account will upvote, comment and resteem the main post where the comment was made. Cool!

---
Outputs:


---

---

**Highlights:**

- flag(!command) is spotted at any part of the comment and alongside with any other words in the comment body
- A log file with date and time who keeps all past data (you can exit, run again and will never lose track)
- Handles multiples action threads in parallel with the stream (you won't miss a post)
- Will never perform the same actions on the same **main post**

-----------------
