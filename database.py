import os
import urllib
from sqlalchemy  import create_engine
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


host_server = os.environ.get('host_server', 'localhost')
db_server_port = urllib.parse.quote_plus(str(os.environ.get('db_server_port', '5432')))
database_name = os.environ.get('database_name', 'leave_wfh_db')
db_username = urllib.parse.quote_plus(str(os.environ.get('db_username', 'leave_user')))
db_password = urllib.parse.quote_plus(str(os.environ.get('db_password', 'leave_user@123')))
#ssl_mode = urllib.parse.quote_plus(str(os.environ.get('ssl_mode','prefer')))
DATABASE_URL = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(db_username, db_password, host_server, db_server_port, database_name)

engine = create_engine(DATABASE_URL,echo=True)
sessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()


# To connect to database 
# $ psql -U leave_user -d leave_wfh_db