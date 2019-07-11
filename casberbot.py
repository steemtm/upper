from steem import Steem
from steem.account import Account
from steem.blockchain import Blockchain
from steem.post import Post
import time
import csv
import threading
import traceback
from datetime import date
from datetime import datetime
from regex import regex
dt = datetime.now()
data_atual = date.today()
datahora = dt.strftime('%H:%M:%S')
s = Steem(keys='')
c = Account('ptgram-power')
filtro = '!up'
delay = 0
autores = []
with open('autores', mode='r') as infile:
    leitor = csv.reader(infile)
    for rows in leitor:
        v = rows[0]
        autores.append(v)
log_time = []
log = []
with open('log', mode='r') as inlog:
    leitor2 = csv.reader(inlog)
    for rows in leitor2:
        r = rows[0]
        log.append(r)

def leitor():
    REGEX = "(?<=^|(?<=[^a-zA-Z0-9-_\.]))!([A-Za-z]+[A-Za-z0-9]+)"
    print('\033[37mIniciando leitura...')
    blockchain = Blockchain()
    stream = map(Post, blockchain.stream(filter_by=['comment']))
    for post in stream:
        author = post['author']
        flag = regex.findall(REGEX, post['body'])
        # body = post['body']
        p_parente = post['parent_permlink']
        a_parente = post['parent_author']
        if post.is_comment():
            if author in autores:
                if filtro in flag:
                    if p_parente in log:
                        print('\033[37machei 1 mas ja comentei-')
                    else:
                        # print(author, body, a_parente, p_parente)
                        log.append(p_parente)
                        acaoThread = threading.Thread(target=acao, args=(a_parente, p_parente, author))
                        acaoThread.start()


def acao(a_acao, p_acao, a_author):
    print(f'\33[31m{data_atual} {datahora}: @{a_acao}/{p_acao} Fila: {threading.active_count() - 1}')
    time.sleep(delay)
    alvo = '@' + a_acao+ '/' + p_acao
    comentario = str(f'Parabéns, @{a_acao}!\nO leitor @{a_author} gostou de seu post e o @ptgram está contribuindo para divulgá-lo. Obrigado por postar seguindo bons critérios de qualidade!')
    try:
        s.commit.vote(alvo, weight=100.0, account='ptgram-power')
        s.commit.post(title='', body=comentario, author='ptgram-power', reply_identifier=alvo)
        s.commit.resteem(alvo, account='ptgram-power')
        print(f'\33[32m{data_atual} {datahora}: {alvo} OK!')
        log_time.append(f'{data_atual} {datahora}: {alvo}')
    except Exception as erro:
        print(repr(erro))


if __name__ == "__main__":

    while True:
        try:
            leitor()
        except (KeyboardInterrupt, SystemExit):
            print('\033[37mGerando logs...')
            with open('log', mode='a') as l:
                for item in log:
                    l.write(f'{item}\n')
            with open('logtime', mode='a') as lt:
                for itemt in log_time:
                    lt.write(f'{itemt}\n')
            print('\033[37mAté mais!')
            break
        except Exception as e:
            traceback.print_exc()
            print('\033[37mIniciando leitura...')
