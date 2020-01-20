#!/usr/bin/python3

import psycopg2


def get_database_connection():
    return psycopg2.connect(host="localhost", database="postgres", user="postgres", password="postgres")