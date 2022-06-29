# Virtuális Arborétum

## OS level dependencies

I'm using Ubuntu 20.04 for development. 
On this system, `psycopg2` depends on the `libpq-dev` and `python[version]-dev` packages.

Here's what I did to be able to install `psycopg2`:

```shell
$ sudo apt-get install python3.9-dev libpq-dev
```

### Notes

If you're using the default Python version (which is `3.8` for 20.04), 
you don't need to specify minor version in the dev package: `python3-dev` is going to work.

On one environment, I ran into errors when trying to install `libpq-dev`, 
`apt` kept complaining about the version of the `libpq5` package.
Eventually I could solve this by downgrading `libpq5`:

```shell
$ sudo apt-get install libpq5=12.11-0ubuntu0.20.04.1
```

After this, `sudo apt-get install libpq-dev` worked.


## Setting up the database

* Create database manually
* Set db name and uri in `app_init.py`
* Run setup script for table creation like this:

```shell
$ cd arboretum/db_setup
$ python db_setup.py
```

* Confirm that you want to drop all your tables
* Done


## Running webserver

### For trial & debugging

```shell
$ python app.py
```

### For production use

```shell
$ gunicorn --access-logfile - arboretum.app:app
```

## Swagger UI

This app contains an OpenApi 3 documentation and a Swagger UI based on that.
When the webserver is running, it is accessible on `/swagger`.


## Unittests

```shell
$ pytest test
```
