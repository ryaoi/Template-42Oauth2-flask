from flask import Flask
from os import urandom
import datetime

app = Flask(__name__)
#app.secret_key = urandom(24)
app.secret_key = "a"*24
app.permanent_session_lifetime = datetime.timedelta(days=7)

from app import routes
