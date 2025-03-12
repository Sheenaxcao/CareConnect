import os

class Config:
    # Use Windows Authentication
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://localhost\\SQLEXPRESS/Care_Connect?driver=ODBC+Driver+17+for+SQL+Server'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24) 
