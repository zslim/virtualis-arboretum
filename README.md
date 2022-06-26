# Virtuális Arborétum


Ubuntu 20.04-en a `psycopg2` Python csomag installálásához szükség volt a `libpq-dev` Ubuntu libraryre.
Ahhoz pedig downgrade-elnem kellett a `libpq5` csomagot.

```shell
$ sudo apt-get install libpq5=12.11-0ubuntu0.20.04.1
$ sudo apt-get install libpq-dev
```


## Setting up the database

* Create database manually
* Set db name and uri in `app_init.py`
* Run setup script for table creation like this:

```shell
$ cd virtualis-arboretum
$ python db_setup/db_setup.py
```

* Confirm that you want to drop all your tables
* Done


## Running webserver

```shell
$ cd virtualis-arboretum
$ python server.py
```


## Swagger UI

This app contains an OpenApi 3 documentation and a Swagger UI based on that.
When the webserver is running, it is accessible on `/swagger`.
