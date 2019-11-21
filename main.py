# -*- coding: utf-8 -*-
# Imports principais do sistema
from flask import Flask, render_template, url_for, redirect, session, request
from conexao import Conexao
from usuario import Usuario
# Imports para construção dos graficos
import requests
import threading
import matplotlib.pyplot as plt
from datetime import datetime
import time
# Inicializando
app = Flask(__name__)
# Rotas da aplicação
c = Conexao()
app.secret_key = "GlKdjIWSZk"
ABEV3 = VAL3 = None
ABEV3T = VAL3T = False
INVESNTIRABEV = INVESTIRVALE = False
# Sistema de envio de mensagens
# Metodo da thread
def threadGraficos(e):
    global ABEV3, VAL3, ABEV3T, VAL3T
    # Looping da thread
    while True:
        try:
            if e == 'ABEV3':
                ABEV3 = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=ABEV3.SA&interval=5min&apikey=5C7SG5L9B22QBUEG')
            elif e == 'VAL3':
                VAL3 = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MGLU3.SA&interval=5min&apikey=5C7SG5L9B22QBUEG')
            if INVESNTIRABEV:
                ABEV3T = True
                print(">> A ambev é uma otima opção para investimento no momento.")
            if INVESTIRVALE:
                VAL3T = True
                print(">> A vale é uma otima opção para investimento no momennto.")
            time.sleep(65)
        except:
            print("Não foi possivel carregar os graficos.")
# Carregando graficos
def atualizarGraficos():
    global ABEV3, VAL3, INVESTIRVALE, INVESNTIRABEV, ABEV3T, VAL3T
    while True:
        if ABEV3 is not None and VAL3 is not None:
            lista = [ABEV3,VAL3]
            for i in lista:
                # Iniciando variaveis
                valor = []
                data = i.json()
                now = datetime.now()
                # Time series
                timeSeries = data['Time Series (5min)']
                open = [float(dado["1. open"]) for dado in timeSeries.values()]
                high = [float(dado["2. high"]) for dado in timeSeries.values()]
                close = [float(dado["4. close"]) for dado in timeSeries.values()]
                volume = [float(dado["5. volume"]) for dado in timeSeries.values()]

                for u in range(len(open)):
                    valor.append(u)

                # verificando
                plt.figure(num=None, figsize=(6, 2.6), dpi=100, facecolor='w', edgecolor='black')

                n = lista.index(i)
                if n == 0:
                    value = 'ambev'
                elif n == 1:
                    value = 'vale'
                # Media movel
                if (n == 0 and not ABEV3T) or (n ==  1 and not VAL3T):
                    if n == 0:
                        ABEV3T = True
                    elif n == 1:
                        VAL3T = True
                    num_sorts = []
                    for x in range(0, 5):
                        num_sorts.append(close[(len(close) - 1) - x])
                    ultimo = num_sorts[0]
                    media = sum(num_sorts) / 5
                    if ultimo > media:
                        if n == 0:
                            INVESNTIRABEV = True
                        elif n == 1:
                            INVESTIRVALE = True
                # Fim media movel
                plt.plot(valor, open[::-1])
                plt.savefig('static/graficos/'+value+"open" + '.png')
                plt.clf()
                plt.plot(valor, high[::-1])
                plt.savefig('static/graficos/'+value+"high" + '.png')
                plt.clf()
                plt.plot(valor, close[::-1])
                plt.savefig('static/graficos/'+value+"close" + '.png')
                plt.clf()
                plt.plot(valor, volume[::-1])
                plt.savefig('static/graficos/'+value+"volume" + '.png')
                plt.clf()
                plt.close()
            ABEV3 = None
            VAL3 = None

# Fim Carregando graficos
@app.route("/")
def main_page():
    global mail_to
    if 'login' not in session:
        return render_template('login.html')
    else:
        user = c.getUsuario(session['login'])
    mail_to = user.getEmail()
    return render_template('trades.html', u = user , tempo = datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
@app.route("/logar", methods= ['POST'])
def logar():
    if request.method == 'POST':
        lista_u = c.usuarios()
        user_encontrado = None
        email = request.form['email']
        senha = request.form['senha']
        for u in lista_u:
            if u.getEmail() == email and u.getSenha() == senha:
                user_encontrado = u
                break
        if user_encontrado != None:
            session['login'] = user_encontrado.getId()
            session['email'] = user_encontrado.getEmail()
    return redirect(url_for('main_page'))

@app.route("/registro")
def registro():
    if 'login' not in session:
	    return render_template("registro.html")
    else:
        return redirect(url_for(main_page))
@app.route("/registrar", methods=['POST'])
def registrar():
	nome  = request.form['nome']
	email = request.form['email']
	senha = request.form['senha']
	usuario = Usuario(0,nome,email,senha)
	c.cadastrar(usuario)
	return redirect(url_for('main_page'))
@app.route("/deslogar")
def deslogar():
	if 'login' in session:
		session.clear()
	return redirect(url_for('main_page'))
@app.route("/investimento/<string:empresa>")
def investimento(empresa):
	return render_template('investimento.html', empresa = empresa)
def run():
	app.run(debug=True)
# Incializando sistema
thread1 = threading.Thread(target=threadGraficos,args=('ABEV3',))
thread2 = threading.Thread(target=threadGraficos,args=('VAL3',))
thread = threading.Thread(target=atualizarGraficos)
thread1.start()
thread2.start()
thread.start()
run()