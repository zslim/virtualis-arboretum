# Virtuális Arborétum


Ubuntu 20.04-en a `psycopg2` Python csomag installálásához szükség volt a következő Ubuntu libraryre:

```shell
$ sudo apt-get install ibpq-dev
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
