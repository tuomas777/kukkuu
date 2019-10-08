# Kukkuu

:baby: Godchildren of culture (kulttuurin kummilapset) API :violin:

## Development with Docker

1. Create `.env` environment file

2. Set the `DEBUG` environment variable to `1`

3. Run `docker-compose up`

4. Run migrations if needed: 
    * `docker exec kukkuu python manage.py migrate`

5. Create superuser if needed: 
    * `docker exec -it kukkuu python manage.py createsuperuser`

The project is now running at [localhost:8000](http://localhost:8000)

## Development without Docker

Prerequisites:

* PostgreSQL 11
* Python 3.7

### Installing Python requirements

* Run `pip install -r requirements.txt`
* Run `pip install -r requirements-dev.txt` (development requirements)

### Database

To setup a database compatible with default database settings:

Create user and database

    sudo -u postgres createuser -P -R -S kukkuu  # use password `kukkuu`
    sudo -u postgres createdb -O kukkuu kukkuu

Allow user to create test database

    sudo -u postgres psql -c "ALTER USER kukkuu CREATEDB;"

### Daily running

* Create `.env` file: `touch .env`
* Set the `DEBUG` environment variable to `1`.
* Run `python manage.py migrate`
* Run `python manage.py runserver 0:8000`

The project is now running at [localhost:8000](http://localhost:8000)

## Keeping Python requirements up to date

1. Install `pip-tools`:
    
    * `pip install pip-tools`

2. Add new packages to `requirements.in` or `requirements-dev.in`

3. Update `.txt` file for the changed requirements file:
 
    * `pip-compile requirements.in`
    * `pip-compile requirements-dev.in`

4. If you want to update dependencies to their newest versions, run:

    * `pip-compile --upgrade requirements.in`

5. To install Python requirements run:

    * `pip-sync requirements.txt`

## Code format

This project uses [`black`](https://github.com/ambv/black) for Python code formatting.
We follow the basic config, without any modifications. Basic `black` commands:

* To let `black` do its magic: `black .`
* To see which files `black` would change: `black --check .`
