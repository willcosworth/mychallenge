import os
import json
import pika
import pymysql
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import prometheus_client
from prometheus_client import make_wsgi_app, Counter, Gauge, REGISTRY

app = Flask(__name__)

IP_MQ = os.environ.get("IP_MQ","localhost")
PORT_MQ = int(os.environ.get("PORT_MQ",5672))
USER_MQ = os.environ.get("USER_MQ","guest")
PASS_MQ = os.environ.get("PASS_MQ","guest")
EXC_MQ = os.environ.get("EXC_MQ","exchange")

MYSQL_HOST = os.environ.get('MYSQL_HOST','localhost')
MYSQL_PORT = int(os.environ.get('MYSQL_PORT',5672))
MYSQL_DB = os.environ.get('MYSQL_DB','appdb')
MYSQL_USER = os.environ.get('MYSQL_USER','app')
MYSQL_PASS = os.environ.get('MYSQL_PASS','challenge')

# =======================================================================================
# Rota votos:
# @app.route('/votar/<candidato>', methods=["GET"])
# def votacao():
#     votos.labels(candidato).inc(1)
#     votos.labels(voto_total).inc(1)
#     return {candidato}, 200
# =======================================================================================

# # Disable as default
# prometheus_client.REGISTRY.unregister(prometheus_client.PROCESS_COLLECTOR)
# prometheus_client.REGISTRY.unregister(prometheus_client.PLATFORM_COLLECTOR)
# prometheus_client.REGISTRY.unregister(prometheus_client.GC_COLLECTOR)

# votos = Counter('votos_por_candidato', 'Quantidade de votos por candidato', ['candidato'])

# app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
#     '/metrics': make_wsgi_app()
# })

# Conexão Banco
appdb = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT,db=MYSQL_DB, user=MYSQL_USER, passwd=MYSQL_PASS)

# Consulta SQL Candidatos

cursor = appdb.cursor()
# Consulta SQL Candidato1 - Renata
query_candidato1 = "SELECT COUNT(*) FROM candidato1"
cursor.execute(query_candidato1)
voto_candidato1 = cursor.fetchone()[0]

# Consulta SQL Candidato2 - Rafael
query_candidato2 = "SELECT COUNT(*) FROM candidato2"
cursor.execute(query_candidato2)
voto_candidato2 = cursor.fetchone()[0]

# Calcula total
voto_total = voto_candidato1 + voto_candidato2

cursor.close()

# Calcula Porcento
def percentual_votacao(voto_candidato, voto_total):
    percentual = (voto_candidato / voto_total) * 100 if voto_total > 0 else 0
    return round(percentual,2)

#Cria canal pra input no Exchange
def envia_pra_fila(mensagem):
    fmt_mensagem = mensagem
    try:
        connection_parameters = pika.ConnectionParameters(host=IP_MQ,port=PORT_MQ,credentials=pika.PlainCredentials(username=USER_MQ,password=PASS_MQ))
        channel = pika.BlockingConnection(connection_parameters).channel()
        channel.basic_publish(exchange=EXC_MQ,routing_key="",body=fmt_mensagem,properties=pika.BasicProperties(delivery_mode=2))
    except Exception as e:
        return jsonify({'mensagem': 'Erro ao registrar os votos', 'erro': str(e)}), 500

# Index
@app.route('/')
def index():
    return render_template('index.html')

# Registro dos Votos
@app.route('/votar', methods=['GET', 'POST'])
def votar():
    if request.method == 'POST':
        candidato = request.form['candidato']
        # votacao(candidato)
        hora = datetime.now()
        hora_db = hora.isoformat()
        if candidato == 'Renata':
            mensagem = {"nome": candidato, "timestamp": hora_db}
            fmt_mensagem = json.dumps(mensagem)
            envia_pra_fila(fmt_mensagem)
                                  
            # Apresenta percentual votos
            percentual = percentual_votacao(voto_candidato1, voto_total)
            return render_template('confirmacao.html', candidato=candidato, votacao=percentual)
        elif candidato == 'Rafael':
            mensagem = {"nome": candidato, "timestamp": hora_db}
            fmt_mensagem = json.dumps(mensagem)
            envia_pra_fila(fmt_mensagem)
            
            # Apresenta percentual votos
            percentual = percentual_votacao(voto_candidato2, voto_total)
            return render_template('confirmacao.html', candidato=candidato, votacao=percentual)
            
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)

