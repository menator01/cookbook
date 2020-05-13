#! /usr/bin/env python3.8

# For header image. the images I used for test was width 954px height 61px
# Format IMG = 'images/your_logo.png'
IMG = 'images/cookbook_logo.png'
ICOIMG = 'images/cropped_book2.png' # if you wish to use a png icon
ALERT = 'sounds/alert.mp3'
BTN = 'sounds/beep.mp3'
LNK = 'sounds/lnk.mp3'
WINDOW_OPEN = 'sounds/window_open.mp3'
WINDOW_CLOSE = 'sounds/window_close.mp3'

# db_type is for the type of database you want to use
# Options mysql or sqlite3 - default sqlite3
# mysql the database needs to exist. The script will create the table.
DB_TYPE = 'sqlite3'

HOST = ''      # localhost or ip address
USER = ''      # username for mysql database
PASSWD = ''    # password for mysql database
DB = ''        # database name
PORT = 3306    # port for mysql database default is 3306
