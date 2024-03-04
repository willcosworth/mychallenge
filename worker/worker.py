import pika, json, pymysql
import os

IP_MQ = os.environ.get("IP_MQ","localhost")
PORT_MQ = int(os.environ.get("PORT_MQ",5672))
USER_MQ = os.environ.get("USER_MQ","guest")
PASS_MQ = os.environ.get("PASS_MQ","guest")
EXC_MQ = os.environ.get("EXC_MQ","exchange")

MYSQL_HOST = os.environ.get('MYSQL_HOST','appdb')
MYSQL_PORT = int(os.environ.get('MYSQL_PORT',3306))
MYSQL_DB = os.environ.get('MYSQL_DB','appdb')
MYSQL_USER = os.environ.get('MYSQL_USER','app')
MYSQL_PASS = os.environ.get('MYSQL_PASS','challenge')



appdb = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT,db=MYSQL_DB, user=MYSQL_USER, passwd=MYSQL_PASS)
connection_parameters = pika.ConnectionParameters(host=IP_MQ,port=PORT_MQ,credentials=pika.PlainCredentials(username=USER_MQ,password=PASS_MQ))

def minha_callback(ch, method, properties, body):
    mensagem = json.loads(body.decode('utf-8'))
#    print(mensagem['nome'],mensagem['hora'])
    if mensagem['nome'] == 'Renata':
        cursor = appdb.cursor()
        # Executa a query
        cursor.execute("INSERT INTO candidato1 (nome, hora_voto) VALUES (%s, %s)", (mensagem['nome'],mensagem['timestamp']))
        appdb.commit()
        # Fecha o cursor
        cursor.close()       
    else:
        cursor = appdb.cursor()
        # Executa a query
        cursor.execute("INSERT INTO candidato2 (nome, hora_voto) VALUES (%s, %s)", ('Rafael',mensagem['timestamp']))
        appdb.commit()
        # Fecha o cursor
        cursor.close()

def input_db():
    channel = pika.BlockingConnection(connection_parameters).channel()
    channel.queue_declare(
        queue="fila_app",
        durable=True
        )
    channel.basic_consume(
        queue="fila_app",
        auto_ack=True,
        on_message_callback=minha_callback
    )

    print(f'Listen RabbitMQ on Port 5672')
    channel.start_consuming()

while True:
    input_db()
