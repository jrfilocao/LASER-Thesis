#!/usr/bin/python3

import psycopg2


def get_database_connection():
    database_connection = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="postgres")
    database_connection.autocommit = True
    return database_connection
