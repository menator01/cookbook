#! /usr/bin/env python3.8
'''Database connection, queries and timeconverter'''
from modules import settings

if settings.DB_TYPE == 'sqlite3':
    import sqlite3
    from sqlite3 import Error


    class Database:
        '''Docstring'''
        def __init__(self):
            pass

        def check_for_database(self):
            '''Docstring'''
            try:
                with open('Recipes.db'):
                    print('Files exists')

            except FileNotFoundError:
                try:
                    print('Creating database and tables')
                    conn = sqlite3.connect('Recipes.db')
                    cur = conn.cursor()
                    cur.execute('create table recipes( \
                    id integer primary key autoincrement, \
                    title varchar(100) not null, \
                    ingredients text not null, \
                    instructions text not null, \
                    prep integer not null default 0, \
                    cook integer not null default 0)')
                    conn.commit()

                    cur.execute('insert into recipes (title, ingredients, instructions) values \
                    ("a test recipe","The database requires at least one entry.", \
                    "This will be removed when you add your first recipe")')

                    conn.commit()
                    conn.close()
                except Error:
                    print(Error)
            except Error:
                print(Error)

        def title_query(self, letter):
            '''Docstring'''
            try:
                conn = sqlite3.connect('Recipes.db')
                cursor = conn.cursor()
                cursor.execute(f'select id, title from recipes where title like "{letter}%"')
                results = cursor.fetchall()
                conn.commit()
                conn.close()
                return results
            except Error:
                print(f'Error: {Error}')

        def id_query(self, recipe_id):
            '''Dcostring'''
            try:
                conn = sqlite3.connect('Recipes.db')
                cursor = conn.cursor()
                cursor.execute(f'select * from recipes where id = {recipe_id}')
                result = cursor.fetchone()
                conn.commit()
                conn.close()
                return result
            except Error:
                print(f'Error: {Error}')

        def enter_recipe(self, title, ingredients, instructions, prep, cook):
            '''Docstring'''
            try:
                conn = sqlite3.connect('Recipes.db')
                cursor = conn.cursor()
                cursor.execute('select * from recipes')
                result = cursor.fetchone()
                conn.commit()
                if result[1] == 'a test recipe':
                    cursor.execute(f'delete from recipes where id = {result[0]}')

                cursor.execute(f'insert into recipes (title, ingredients, \
                instructions, prep, cook) values ("{title}", \
                "{ingredients}", "{instructions}", "{prep}", "{cook}")')
                conn.commit()
                conn.close()
                return cursor.lastrowid

            except (Error, FileNotFoundError) as error:
                print(error)

        def first_recipe(self):
            conn = sqlite3.connect('Recipes.db')
            cursor = conn.cursor()
            cursor.execute('select id, title from recipes limit 1')
            result = cursor.fetchone()
            letter = result[1][0]
            recipe_id = result[0]
            return letter, recipe_id

elif settings.DB_TYPE == 'mysql':

    from tkinter import messagebox
    import sys
    import pymysql
    import threading
    from playsound import playsound

    class Database:
        '''doc'''
        def __init__(self):
            pass

        def check_for_database(self):
            '''soc'''
            try:
                self.conn = pymysql.connect(host=settings.HOST, user=settings.USER, \
                passwd=settings.PASSWD, database=settings.DB, port=settings.PORT)
                print(f'Connected to {settings.DB}')

                try:
                    cursor = self.conn.cursor()
                    cursor.execute('select * from recipes')
                except (pymysql.OperationalError, pymysql.ProgrammingError) as error:
                    if error.args[0] == 1146:
                        print('Creating table')
                        cursor.execute('create table recipes (id int(5) auto_increment, \
                        title varchar(200) not null, ingredients text not null, \
                        instructions text not null, prep_time int(5), \
                        cook_time int(5), primary key(id))')
                        cursor.connection.commit()

                        cursor.execute("INSERT INTO collections.recipes (title, \
                        ingredients, instructions, prep_time, cook_time) VALUES \
                        ('a test recipe', 'This is a test recipe', 'It will be removed when you add your first recipe', '10', '90')")
                        cursor.connection.commit()

            except pymysql.OperationalError as error:
                if error:
                    print(f'Error: {error}')
                    threading.Thread(target=playsound, args=(settings.ALERT,)).start()
                    messagebox.showerror(title='Database Connection', \
                    message='Error! Please check database connection settings.')
                    sys.exit()
            self.conn.close()

        ### Query the database for our titles
        def title_query(self, letter):
            '''Docstring'''
            try:
                self.conn = pymysql.connect(host=settings.HOST, user=settings.USER, \
                passwd=settings.PASSWD, database=settings.DB, port=settings.PORT)

                query = f'select id, title from recipes where title like "{letter}%"'
                with self.conn.cursor() as cursor:
                    cursor.execute(query)
                    results = cursor.fetchall()
                return results

            except pymysql.InternalError:
                print('Database Error! Please check your database query for errors.')
                threading.Thread(target=playsound, args=(settings.ALERT,)).start()
                messagebox.showerror(title='Database Error', \
                message='Error! Please check query format settings.')
                sys.exit()

        ### Query the database for recipes
        def id_query(self, recipe_id):
            '''Socstring'''
            try:
                self.conn = pymysql.connect(host=settings.HOST, user=settings.USER, \
                passwd=settings.PASSWD, database=settings.DB, port=settings.PORT)

                query = f'select * from recipes where id = "{recipe_id}"'
                with self.conn.cursor() as cursor:
                    cursor.execute(query)
                    results = cursor.fetchone()
                return results

            except pymysql.InternalError:
                messagebox.showerror(title='Database Error', \
                message='Error! Please check query format settings.')
                sys.exit()

        def enter_recipe(self, title, ingredients, instructions, prep, cook):
            '''Docstring'''
            try:
                self.conn = pymysql.connect(host=settings.HOST, user=settings.USER, \
                passwd=settings.PASSWD, database=settings.DB, port=settings.PORT)

                cursor = self.conn.cursor()

                cursor.execute('select * from recipes')
                result = cursor.fetchone()
                cursor.connection.commit()
                if result[1] == 'a test recipe':
                    cursor.execute(f'delete from recipes where id = {result[0]}')
                cursor.connection.commit()

                cursor.execute(f'insert into recipes (title, ingredients, \
                instructions, prep_time, cook_time) values ("{title}", \
                "{ingredients}", "{instructions}", "{prep}", "{cook}")')
                cursor.connection.commit()
                self.conn.close()
                return cursor.lastrowid
            except (pymysql.InternalError) as error:
                print(error)

        def first_recipe(self):
            try:
                self.conn = pymysql.connect(host=settings.HOST, user=settings.USER, \
                passwd=settings.PASSWD, database=settings.DB, port=settings.PORT)

                cursor = self.conn.cursor()
                cursor.execute('select id, title from recipes limit 1')
                result = cursor.fetchone()
                letter = result[1][0]
                recipe_id = result[0]
                return letter, recipe_id
            except (pymysql.InternalError) as error:
                print(error)

else:
    print('Unknown database type.')
