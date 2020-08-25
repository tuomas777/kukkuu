# Kukkuu

:baby: Culture Kids (kulttuurin kummilapset) API :violin:

[![status](https://travis-ci.com/City-of-Helsinki/kukkuu.svg)](https://github.com/City-of-Helsinki/kukkuu)
[![codecov](https://codecov.io/gh/City-of-Helsinki/kukkuu/branch/develop/graph/badge.svg)](https://codecov.io/gh/City-of-Helsinki/kukkuu)

## Environments
Production environment:
- https://kukkuu-api.prod.hel.ninja/kukkuu/graphql

Testing environment:
- https://kukkuu.test.kuva.hel.ninja/graphql

## Development with Docker

1. Copy `docker-compose.env.yaml.example` to `docker-compose.env.yaml` and modify it if needed.

2. Run `docker-compose up`

The project is now running at [localhost:8081](http://localhost:8081)

## Development without Docker

Prerequisites:

* PostgreSQL 10
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

Add default languages (optional)

    python manage.py add_languages --default

### Cron jobs
By default email sending won't be queued. In case you want to queue emails:
 - In `settings.py` configure `ILMOITIN_QUEUE_NOTIFICATIONS` to `True`
 - Install `cron` in your host machine
 - Add a crontab to execute the email delivery, here is an example:
   
    ```
    *       * * * * (/path/to/your/python path/to/your/app/manage.py send_mail > /var/log/cron.log 2>&1)
    0,20,40 * * * * (/path/to/your/python path/to/your/app/manage.py retry_deferred > /var/log/cron.log 2>&1)
    0 0 * * * (/path/to/your/python path/to/your/app/manage.py purge_mail_log 7 > /var/log/cron.log 2>&1)
    # An empty line is required at the end of this file for a valid cron file.

    ```

### Daily running, Debugging

* Create `.env` file: `touch .env`
* Set the `DEBUG` environment variable to `1`.
* Run `python manage.py migrate`
* Run `python manage.py runserver localhost:8081`
* The project is now running at [localhost:8081](http://localhost:8081) 

## API Documentation

To view the API documentation, in DEBUG mode visit: http://localhost:8081/graphql and checkout the `Documentation Explorer` section

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

Or you can use [`pre-commit`](https://pre-commit.com/) to quickly format your code before committing.


1. Install `pre-commit` (there are many ways to do but let's use pip as an example):
    * `pip install pre-commit`
2. Set up git hooks from `.pre-commit-config.yaml`, run this command from project root:
    * `pre-commit install`

After that, formatting hooks will run against all changed files before committing

## Contact infomation

@tuomas777 @quyenlq

## Issues board

https://helsinkisolutionoffice.atlassian.net/projects/KK/issues/?filter=allissues
