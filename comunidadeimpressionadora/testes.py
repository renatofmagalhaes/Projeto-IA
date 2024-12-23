import sys
sys.path.append('.')
from comunidadeimpressionadora import app, database
from comunidadeimpressionadora.models import Usuario
#from app import app, database
#from models import Usuario, Post

### CRIANDO O BANCO DE DADOS ###    
# with app.app_context():
#    database.create_all()

### CRIANDO USUÁRIOS ###
#with app.app_context():
#    usuario1 = Usuario(nome="Renato", 
#                      email="renato@gmail.com", 
#                      senha="Rfm33@12")
#    usuario2 = Usuario(nome="Maria", 
#                      email="maria@gmail.com", 
#                      senha="Mar11@12")
    
#    database.session.add(usuario1)
#    database.session.add(usuario2)
#    database.session.commit()

### CONSULTANDO USUÁRIOS ###
# with app.app_context():
#    usuario1 = Usuario.query.filter_by(nome="Renato").first()
#    print(f"ID: {usuario1.id}")
#    print(f"Nome: {usuario1.nome}")
#    print(f"Email: {usuario1.email}")
#    print(f"Senha: {usuario1.senha}")

# with app.app_context():
#     usuario2 = Usuario.query.filter_by(nome="Maria").first()
#     print(f"ID: {usuario2.id}")
#     print(f"Nome: {usuario2.nome}")
#     print(f"Email: {usuario2.email}")
#     print(f"Senha: {usuario2.senha}")

#with app.app_context():
#    usuario = Usuario.query.filter_by(id=2).first()
#    print(f"Email do usuário {usuario.nome}: {usuario.email}")

### CONSULTANDO POSTS ###
# with app.app_context():
#    posts = Post.query.all()
#    
#    print("\nTodos os Posts do Banco de Dados:")
#    for post in posts:
#        print("\n=== Post ===")
#        print(f"ID: {post.id}")
#        print(f"Título: {post.titulo}")
#        print(f"Corpo: {post.corpo}")
#        print(f"ID do Usuário: {post.id_usuario}")
#        print(f"Autor: {post.autor.nome}")

### RESETANDO O BANCO DE DADOS ###
#with app.app_context():
    # Apaga todas as tabelas
    #database.drop_all()
    
    # Recria todas as tabelas
    # database.create_all()
    # print("Banco de dados resetado com sucesso!")
    
