from flask import Flask, jsonify, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.dialects.postgresql import JSON
import functools
import psycopg2
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@localhost:5432/tenants'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_BINDS'] = {}

db = SQLAlchemy(app)

db_migrate = Migrate(app, db)


# models

class Tenant(db.Model):
    __tablename__ = 'tenants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    database = db.Column(db.String, nullable=False)
    configdata = db.Column(JSON)

    def __init__(self, name, database, configdata=None):
        self.name = name,
        self.database = database,
        self.configdata = configdata

    def __repr__(self):
        return f"<id={self.id}, username={self.name}>"

class SurveyResult(db.Model):
    __tablename__ = 'surveyresults'
    __bind_key__ = 'tenantDB'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    answers = db.Column(JSON)
    
    def __init__(self, email, answers):
        self.email = email,
        self.answers = answers,





# decorators
def getTenantID(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        #do work before original function
        tenantID = request.path.split('/')[1]
        print(tenantID)
        tenant = Tenant.query.filter_by(name=tenantID).first()
        if not tenant:
            return 'No tenant'

        database = tenant.database

        print(database)

        if database == 'postgres':
            app.config['SQLALCHEMY_BINDS']['tenantDB'] = f'postgresql://postgres:@localhost:5432/{tenant.name}'

        
  
    

        return f(*args, **kwargs)
    

        
    return wrapped



# application

@app.route('/signup', methods=['POST'])
def index():
    data = request.get_json()
    newTenant = Tenant(data.get('name'), data.get('database'), data.get('configdata') )
    db.session.add(newTenant)
    db.session.commit()
    print('new tenant added', data.get('name'))

    return 'new tenant added!'

@app.route('/tenants', methods=['GET'])
def getTenants():
    print('getting tenants')
    tenants = Tenant.query.all()
    for tenant in tenants:
        print(tenant.name, tenant.database)

    return 'found tenants'


@app.route('/<tenantName>/surveys')
@getTenantID
def getTenantConfig(tenantName):
    #print('returning tenant config:', tenantName)
    #print(db.get_engine(app, 'db2'))  # will show sqlite db2.db
    print(db.get_tables_for_bind('tenantDB')) 
    email = 'testa@gmail.com'
    answers = json.dumps({'what is your name?': 'test',
    'will you come again?': 'yes'})
    survey = SurveyResult(email, answers)
    
     # will show remote_user table
    #print(db.get_binds(app))  # a dict mapping tables to their bound engine
   # print(tenantName)
   
    return 'surveys page'

@app.route('/hello')
def check():
    return 'all is well'



if __name__ == '__main__':
    app.run(debug=True)
