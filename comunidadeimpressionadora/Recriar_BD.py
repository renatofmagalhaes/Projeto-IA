import sys
sys.path.append('.')
from comunidadeimpressionadora import app, database
#from comunidadeimpressionadora.models import Usuario

### RESETANDO O BANCO DE DADOS ###
with app.app_context():
    # APAGA TODAS AS TABELAS
    database.drop_all()
    
    # RECRIA TODAS AS TABELAS
    database.create_all()
    print("Banco de dados resetado com sucesso!")

