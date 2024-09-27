from dotenv import dotenv_values
from flask_sqlalchemy import SQLAlchemy

config = dotenv_values(".env")
url = f'{config['DRIVER']}://{config['USER']}:{config['PASSWORD']}@{config['HOST']}:{config['PORT']}/{config['DB']}'

db = SQLAlchemy()