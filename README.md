# QRodizio Backend

**Número do Grupo**: 10<br>
**Código da Disciplina**: FGA0208-T01<br>

## Alunos

| Matrícula  | Aluno                                                           |
| ---------- | --------------------------------------------------------------- |
| 15/0078692 | [Caio César de Almeida Beleza](https://github.com/Caiocbeleza)  |
| 14/0056068 | [Cauê Mateus Oliveira](https://github.com/caue96)               |
| 12/0116928 | [Fábio Teixeira](https://github.com/fabio1079)                  |
| 14/0145842 | [João Pedro Gomes Cabral Ferreira](https://github.com/jppgomes) |
| 13/0122254 | [Lucas Midley](https://github.com/lucasmidlhey)                 |

## Sobre

Backend do projeto [QRodizio](https://github.com/UnBArqDsw/2020.1_G10_QRodizio)

Aplicação feita em python com o uso do microframework [flask](https://flask.palletsprojects.com)

## Screenshots

Adicione 3 ou mais screenshots do projeto em termos de interface e funcionamento.

## Instalação

**Linguagens**: Python<br>
**Tecnologias**: Flask, Docker<br>

A aplicação pode ser executada tanto pelo uso do [docker](https://www.docker.com/) quanto por um [virtualenv](https://virtualenv.pypa.io/en/latest/).

No caso do [docker](https://www.docker.com/), é necessário o uso do [docker-compose](https://docs.docker.com/compose/).

No caso do [virtualenv](https://virtualenv.pypa.io/en/latest/), é necessário uso de um banco de dados postgreesql com um banco
de nome "qrodizio_development" previamente criado.

### Docker

Preparando ambiente pela primeira vez:

- sudo docker-compose build
- sudo docker-compose up
- sudo docker-compose run api flask create-db

Rodando aplicação:

- sudo docker-compose up

**PS**: É recomendável fazer um "sudo docker-compose down" de pois de alguns "ups".

### Virtualenv

Preparando ambiente pela primeira vez:

- virtualenv -p python3 .venv
- source .venv/bin/activate
- make install
- flask create-db

**PS**: Talvez seja necessário instalar a libpq-dev por causa da psycopg2.

Rodando aplicação:

- flask run

**PS**: Caso queira usar Virtualenv mas nao tem um banco de dados posgreesql, basta remover a linha SQLALCHEMY_DATABASE_URI do arquivo "settings.toml" em "[development]". Dessa forma a aplicação vai usar a configuração padrão que é o sqlite. E lembre-se de nao comitar essa alteração 😅.

## Uso

- Com docker: sudo docker-compose up
- Com Virtualenv: flask run

## Vídeo

Adicione 1 ou mais vídeos com a execução do projeto final.

## Outros

Quaisquer outras informações sobre seu projeto podem ser descritas abaixo.
