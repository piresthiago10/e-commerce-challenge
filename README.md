# Ecommerce Backend

Backend básico para manipulação de produtos, serviços, vendedores, clientes e vendas.

# Equipe:

* **Thiago Pires** - *Backend Developer*;

## Requisitos:

* Python 3.9;
* Django 3.0;
* Django Rest Framework 3.11

## Instalção:

1. Clone o projeto:
```
git clone https://github.com/piresthiago10/e-commerce-challenge.git
```
2. Acesse a pasta ecommerce e execute os coamndos:
```
docker-compose run web python manage.py makemigrations

docker-compose run web python manage.py migrate

docker-compose up
```
3. Aguarde a instalação do container Docker, após a instalação a API estará disponível em:
```
http://0.0.0.0:8000/

api/customers
api/products'
api/sales'
api/detail_sales'
api/sellers'
api/accounts'
api/new_user'
api/login/
api/comission/seller/<int:id>/start_date/<str:start_date>/end_date/<str:end_date>/
```

## Run tests:
1. Na pasta ecommerce execute o comando:
```
docker-compose run web python manage.py test
```

## Ferramentas:

* [Docker](https://www.docker.com/)
* [Visual Studio Code](https://code.visualstudio.com/)
* [Google Chrome](https://www.google.pt/intl/pt-PT/chrome/?brand=CHBD&gclid=Cj0KCQjwn_LrBRD4ARIsAFEQFKt3kLTIsdU6a-sk3FKsxrhplkKaYNHo6Pt3aRbaEAJ3TK4fZslZmtUaAvHVEALw_wcB&gclsrc=aw)
* [Postman](https://www.postman.com/)
