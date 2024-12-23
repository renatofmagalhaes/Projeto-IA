from comunidadeimpressionadora import database, login_manager   
from datetime import datetime
from flask_login import UserMixin

# FUNÇÃO DE CARREGAMENTO DO USUÁRIO
@login_manager.user_loader
def load_user(id_usuario):
    return Usuario.query.get(int(id_usuario))


# CLASSE USUÁRIO
class Usuario(database.Model, UserMixin ):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String(30), nullable=False)
    email = database.Column(database.String(40), unique=True, nullable=False)
    senha = database.Column(database.String(60), nullable=False)
    foto_perfil = database.Column(database.String(20), nullable=False, default='default.jpg')
    cursos = database.Column(database.String(100), nullable=False, default='Não Informado')
    posts = database.relationship('Post', backref='autor', lazy=True)
    
    # FUNÇÃO PARA CONTAR OS POSTS DO USUÁRIO
    def contar_posts(self):
        return len(self.posts)

    def __repr__(self):
        return f'<Usuario {self.email}>'

# CLASSE POST
class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String(100), nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)

    def __repr__(self):
        return f'<Post {self.titulo}>'
    