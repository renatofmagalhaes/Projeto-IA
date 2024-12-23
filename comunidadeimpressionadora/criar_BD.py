import sys
sys.path.append('.')
from comunidadeimpressionadora import app, database
#from comunidadeimpressionadora.models import Usuario

### CRIANDO O BANCO DE DADOS ###    
with app.app_context():
    database.create_all()