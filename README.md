# Projeto de PCS3643

Projeto em Django da disciplina PCS3643

## Integrantes do Grupo 9

- Gabriel Cosme Barbosa: 11844051
- Isabelle Ritter Vargas: 11806600
- Matheus Rezende Pereira: 11261805

## Como executar o projeto:

Primeiramente, clone o repositório:

```bash
git clone https://github.com/GabrielCosme/projeto-pcs3643.git
```

Em seguida, crie um ambiente virtual e instale as dependências:

```bash 
python3 -m venv env
./env/bin/activate
pip install -r requirements.txt
```

Para executar o projeto, execute o comando:

```bash
python manage.py runserver
```

Em seguida acesse o endereço http://localhost:8000/ no seu navegador.

Caso queira explorar o ambiente de administração, crie um super usuário:

```bash
python manage.py createsuperuser
```

E acesse o endereço http://localhost:8000/admin/ no seu navegador.

## Como executar os testes:

Para executar os testes, execute o comando:

```bash
python manage.py test
```

## Como fazer migrações do banco de dados:

Para fazer migrações do banco de dados, execute o comando:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Aula de desenvolvimento 1:

Nesta aula foi realizada a construção inicial do repositório e foi feito o esqueleto dos diretórios, tão como definida a direção futura do projeto.'

## Aula de desenvolvimento 2:

Nesta aula foi feita a criação do modelo de dados do projeto, bem como um CRUD rudimentar e os testes relativos a seu funcionamento. Além disso, os diagramas foram refatorados visando corrigi-los.

## Aula de desenvolvimento 3:
Nesta aula foi adicionada uma interface front end para login e navegação no site, criando o template para o CRUD dos Voos, para o monitoramento de voos e geração de relatório, mas sem as funcionalidades de fato. Além disso, foi desenvolvido um Modelo de Inteface - Navegação para o projeto.