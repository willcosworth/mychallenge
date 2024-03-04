from flask import Flask, jsonify
import pymysql
import os

MYSQL_HOST = os.environ.get('MYSQL_HOST','appdb')
MYSQL_PORT = int(os.environ.get('MYSQL_PORT',3306))
MYSQL_DB = os.environ.get('MYSQL_DB','appdb')
MYSQL_USER = os.environ.get('MYSQL_USER','app')
MYSQL_PASS = os.environ.get('MYSQL_PASS','challenge')

app = Flask(__name__)
appdb = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT,db=MYSQL_DB, user=MYSQL_USER, passwd=MYSQL_PASS)
# Rota para listar todos os itens do banco de dados
@app.route('/api/votos', methods=['GET'])
def votos():
    while True:
        try:
            # Conectar ao banco de dados MySQL
            cursor = appdb.cursor()
            # Consulta SQL Candidatos
            query_candidato1 = 'SELECT COUNT(*) FROM candidato1'
            cursor.execute(query_candidato1)
            voto_candidato1 = cursor.fetchone()[0]
            # 
            query_candidato2 = 'SELECT COUNT(*) FROM candidato2'
            cursor.execute(query_candidato2)
            voto_candidato2 = cursor.fetchone()[0]
            # Retornar os itens como JSON
            dados_formatados = {
            'Candidato 1': voto_candidato1,
            'Candidato 2': voto_candidato2,
            'Total de Votos': voto_candidato1 + voto_candidato2
        }
            return jsonify(dados_formatados)
        except Exception as e:
            return jsonify({'mensagem': 'Erro ao obter os itens do banco de dados', 'erro': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
