# mychallenge

Challenge with Docker concepts

ARQUITETURA

FRONTEND -> BACKEND -> RABBITMQ -> WORKER -> DB

Cada item da arquitetura é um container em Docker.
Criado a imagem de cada componente(Dockerfile) e na pasta raiz, utilize o docker compose para subir a aplicação.
Para o frontend (http://localhost:80), foi utilizado Python e framework Flask, criando rotas acessíveis.
No backend (http://localhost:8080), para apresentar os resultados, uma API consulta o banco de dados MySQL (localhost:3306) e retorna um Json, com os votos de cada participante e a votação total.
Implementado conceito de fila (http://localhost:15672), usando o RabbitMQ para receber a votação do frontend e um worker que insere os dados no banco de dados.

Definições do Banco de Dados
# Parametros Banco de dados
MYSQL_PASSWORD = challenge
MYSQL_ROOT_PASSWORD = Challenge
MYSQL_DATABASE = appdb
MYSQL_USER = app

# Criação e disposição das Tabelas

sudo docker exec -it appdb /bin/bash
mysql -u root -p
use appdb;

CREATE TABLE candidato1(
id_voto int(4) AUTO_INCREMENT,
nome varchar(30) NOT NULL,
hora_voto timestamp,
PRIMARY KEY (id_voto)
);

CREATE TABLE candidato2(
id_voto int(4) AUTO_INCREMENT,
nome varchar(30) NOT NULL,
hora_voto timestamp,
PRIMARY KEY (id_voto)
);

# Criação do acesso ao db pelo user do app
CREATE USER ‘app’@’localhost’ IDENTIFIED BY ‘challenge’;
GRANT ALL PRIVILEGES ON *.* TO ‘app’@’localhost’ WITH GRANT OPTION;
FLUSH PRIVILEGES;
SHOW GRANTS FOR ‘app’@’localhost’;
EXIT;

# Check visual do DB
mysql -u app -p
use appdb;
describe candidato1;
describe candidato2;

====================================================================================================================

RABBITMQ
docker run -it -d --name rabbitapp -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management-alpine

Configurar:
User e Senha -> guest
Exchange -> exc_app
Fila -> fila_app
Fazer o bind da Exchange pra fila

====================================================================================================================

API RESULTADOS
URL -> http://localhost:8080/api/votos
 

Instalação Portainer – Monitoramento Visual dos containeres
sudo docker volume create portainer_data
sudo docker run -d -p 8000:8000 -p 9000:9000 --name portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:latest
sudo docker ps
