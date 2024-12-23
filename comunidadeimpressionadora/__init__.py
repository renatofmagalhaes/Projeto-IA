from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# CONFIGURAÇÃO DO FLASK
app = Flask(__name__)
app.config['SECRET_KEY'] = 'NQakBgJZoIZ71FoCIsyXctfHJeOR526c'

# CONFIGURAÇÃO DO SQLALCHEMY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# CRIANDO A INSTÂNCIA DO SQLALCHEMY
database = SQLAlchemy(app)

# CRIANDO A INSTÂNCIA DO BCRYPT
bcrypt = Bcrypt(app)

# CRIANDO A INSTÂNCIA DO LOGIN MANAGER
login_manager = LoginManager(app)
# REDIRECIONA PARA A PÁGINA LOGIN CASO O USUÁRIO NÃO ESTEJA LOGADO
login_manager.login_view = 'login'
# MENSAGEM DE SUCESSO
login_manager.login_message_category = 'alert-info'

# Mensagens em português
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
login_manager.login_message_category = 'info'
login_manager.needs_refresh_message = 'Por favor, faça login novamente para acessar esta página.'
login_manager.needs_refresh_message_category = 'info'

# Outras mensagens que podem ser úteis
login_manager.login_view = 'login'  # nome da sua função de login
login_manager.refresh_view = 'login'  # nome da função para renovar login
login_manager.session_protection = 'strong'  # nível de proteção da sessão

# IMPORTANDO AS ROTAS
from comunidadeimpressionadora import routes
