import os
import urllib
from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.orm import session
from sqlalchemy.ext.declaration import declarative_base



host_server = os.environ.get('host_server', 'localhost')
db_server_port = urllib.parse.quote_plus(str(os.environ.get('db_server_port', '5432')))
database_name = os.environ.get('database_name', 'employee')
db_username = urllib.parse.quote_plus(str(os.environ.get('db_username', 'sabihanaaz')))
db_password = urllib.parse.quote_plus(str(os.environ.get('db_password', 'naaz@5968')))
ssl_mode = urllib.parse.quote_plus(str(os.environ.get('ssl_mode','prefer')))
DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}?sslmode={}'.format(db_username, db_password, host_server, db_server_port, database_name, ssl_mode)


engine = create_engine(DATABASE_URL,echo=True)
sessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()
