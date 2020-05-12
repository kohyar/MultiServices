import os

class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))
    movies_url = "http://127.0.0.1:5000"
    books_url = "http://127.0.0.1:5002"




    # Uncomment the desired option
    deploy = 'docker'   # deploying on docker using mysql
    # deploy = 'mysql_local' # deploying locally using mysql
    # deploy = 'sqlite_local' # deploying locally using sqlite

    SQLALCHEMY_DATABASE_URI = ''

    if deploy == 'docker':
        SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://evaluations:evaluations@db_evaluations/evaluations'
        movies_url = "http://movies:5000"
        books_url = "http://books:5002"
    
    else:
        print("Wrong deployment option.")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
