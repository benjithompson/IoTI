"""Flask API"""

#imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__, instance_path='C:/Code/Python/IoTI/ioti/instance')

app.config.from_object(config.ini)
app.config.from_envvar('IOTI_SETTINGS')
