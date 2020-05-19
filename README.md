#### An example Asana integration using Django
To get started, you will need Asana token. You can get it from Developer Console https://app.asana.com/0/developer-console
Put it in the .env file as ASANA_TOKEN env var.

```
mv .env.example .env
```


To run locally:

```
git clone https://github.com/deniskolosov/asana_client.git
cd asana_client
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py get_asana_users # prepopulate Asana users table
python3 manage.py runserver
```
Check running app on localhost:8000

To Run in Docker:
```
docker-compose up -d
```
Run migrations
```
docker-compose exec web python manage.py migrate
```
Prepopulate Asana users to be able to assign them to tasks

```
docker-compose exec web python manage.py get_asana_users
```
Create superuser
```
docker-compose exec web python manage.py createsuperuser
```
Go to admin `0.0.0.0:8000/admin` and test the functionality.
Projects and tasks will be created in first workspace available (see asana_client/manager/__init__.py)


To run tests:
```
docker-compose exec web python manage.py test
```

