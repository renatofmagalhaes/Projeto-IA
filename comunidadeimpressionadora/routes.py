from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost
from flask import render_template, flash, request, redirect, url_for, current_app, abort
from comunidadeimpressionadora.models import Usuario, Post
from flask_login import login_required, login_user, logout_user, current_user
import secrets
import os
from PIL import Image



@app.route('/')
def home():
    todos_posts = Post.query.order_by(Post.data_criacao.desc()).all()  # Obtém todos os posts em ordem decrescente pela data de criação
    return render_template('home.html', posts=todos_posts)

@app.route('/usuarios')
@login_required
def usuarios():
    todos_usuarios = Usuario.query.all()  # Obtém todos os usuários do banco de dados
    return render_template('usuarios.html', 
                           usuarios=todos_usuarios)

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    if request.method == 'POST':
        if 'botao_login' in request.form:
            # SE OS DADOS DO FORMULÁRIO DE LOGIN FOREM VÁLIDOS
            if form_login.validate_on_submit():
                # PESQUISA SE O USUÁRIO EXISTE NO BANCO DE DADOS
                usuario = Usuario.query.filter_by(email=form_login.email.data).first()
                # PESQUISA SE A SENHA É VÁLIDA E SE PERTENCE AO USUÁRIO
                if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
                    # LOGA O USUÁRIO SE O USUARIO EXISTE E SE A SENHA É VÁLIDA
                    login_user(usuario, remember=form_login.lembrar_dados.data)
                    # EXIBE MENSAGEM DE SUCESSO
                    flash('Login realizado com sucesso!', 'success')
                    par_next = request.args.get('next')
                    if par_next:
                        return redirect(par_next)
                    else:
                        # REDIRECIONA O USUÁRIO PARA A PÁGINA HOME
                        return redirect(url_for('home'))
                else:
                    # EXIBE MENSAGEM DE ERRO
                    flash('E-mail ou Senha Inválidos!', 'danger')
                    # REDIRECIONA O USUÁRIO PARA A PÁGINA LOGIN
                    return redirect(url_for('login'))
        else:
            # SE OS DADOS DO FORMUL��RIO DE CRIAR CONTA FOREM VÁLIDOS
            if form_criarconta.validate_on_submit():                
                # CRIPTOGRAFA A SENHA
                senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data).decode('utf-8')
                # CRIA O USUÁRIO - (OBJETO DA CLASSE USUÁRIO)
                usuario = Usuario(nome=form_criarconta.nome.data,
                                email=form_criarconta.email.data,
                                senha=senha_cript)   
                # ADICIONA O USUÁRIO (OBJETO DA CLASSE USUÁRIO) À SESSÃO DO BANCO DE DADOS
                database.session.add(usuario)
                # COMMIT - CONFIRMA A INSERÇÃO DO USUÁRIO (OBJETO DA CLASSE USUÁRIO) NO BANCO DE DADOS
                database.session.commit()
                # EXIBE MENSAGEM DE SUCESSO
                flash('Conta criada com sucesso!', 'success')
                # REDIRECIONA O USUÁRIO PARA A PÁGINA HOME
                return redirect(url_for('home'))
    # RENDERIZA A PÁGINA LOGIN
    return render_template('login.html', 
                         form_login=form_login, 
                         form_criarconta=form_criarconta)

@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    # Cria uma instância do formulário de criar post
    form = FormCriarPost()
    # Se o método da requisição for POST e os dados do formulário forem válidos
    if form.validate_on_submit():
        # Cria o post - (objeto da classe Post)
        post = Post(titulo=form.titulo.data,
                   corpo=form.corpo.data,
                   autor=current_user)
        # Adiciona o post à sessão do banco de dados
        database.session.add(post)
        # Commit - confirma a inserção do post no banco de dados
        database.session.commit()
        # Exibe mensagem de sucesso
        flash('Post criado com sucesso!', 'success')
        # Redireciona o usuário para a página home
        return redirect(url_for('home'))
    # Renderiza a página de criar post
    return render_template('criarpost.html', form=form)

@app.route('/perfil')
@login_required
def perfil():

    # Obtém a foto de perfil do usuário logado
    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    # {{ url_for('static', filename='fotos_perfil/{}'.format(usuario.foto_perfil)) }}
    
    # Renderiza a página de perfil passando os dados do usuário logado
    return render_template('perfil.html', foto_perfil=foto_perfil)

def salvar_imagem(imagem):
    # Gera um código aleatório para o nome da imagem
    codigo = secrets.token_hex(8)
    # Separa o nome do arquivo da extensão
    nome, extensao = os.path.splitext(imagem.filename)
    # Cria o novo nome da imagem com o código aleatório
    nome_arquivo = nome + codigo + extensao
    # Define o caminho completo onde a imagem será salva
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    
    # Reduz o tamanho da imagem
    tamanho = (400, 400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    
    # Salva a imagem reduzida
    imagem_reduzida.save(caminho_completo)
    
    return nome_arquivo

def atualizar_cursos(form):
    # Lista para armazenar os cursos selecionados
    lista_cursos = []
    
    # Verifica cada campo de curso no formulário
    if form.curso_excel.data:
        lista_cursos.append('Excel Impressionador')
    if form.curso_vba.data:
        lista_cursos.append('VBA Impressionador')
    if form.curso_powerbi.data:
        lista_cursos.append('Power BI Impressionador')
    if form.curso_python.data:
        lista_cursos.append('Python Impressionador')
    if form.curso_ppt.data:
        lista_cursos.append('PowerPoint Impressionador')
    if form.curso_sql.data:
        lista_cursos.append('SQL Impressionador')
        
    # Se nenhum curso foi selecionado, retorna 'Não Informado'
    if not lista_cursos:
        return 'Não Informado'
    # Caso contrário, retorna os cursos separados por vírgula
    return '; '.join(lista_cursos)

 
@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    # Renderiza a página de editar perfil, a foto de perfil e o formulário
    if form.validate_on_submit():
        # Atualiza os dados do usuário com os dados do formulário
        current_user.nome = form.nome.data
        current_user.email = form.email.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil =  nome_imagem 
        # Atualiza os cursos do usuário com os cursos selecionados no formulário
        current_user.cursos = atualizar_cursos(form)

        # Commit - confirma a atualização dos dados no banco de dados
        database.session.commit()
        # Exibe mensagem de sucesso
        flash('Perfil atualizado com sucesso!', 'success')
        # Redireciona o usuário para a página de perfil
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        # Preenche o formulário com os dados atuais do usuário
        form.nome.data = current_user.nome
        form.email.data = current_user.email
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)

@app.route('/sair')
@login_required
def sair():
    # Faz o logout do usuário
    logout_user()
    # Exibe mensagem de sucesso
    flash('Logout realizado com sucesso!', 'success')
    # Redireciona o usuário para a página home
    return redirect(url_for('home'))

@app.route('/post/<int:post_id>', methods= ['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user == post.autor:
        form = FormCriarPost() 
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Post atualizado com sucesso!', 'success')
            return redirect(url_for('exibir_post', post_id=post.id))
    else:
        form = None  
    return render_template('post.html', post=post, form=form)

@app.route('/post/<int:post_id>/excluir', methods=['POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get_or_404(post_id)    
    if post.autor == current_user:  # Verifica se o usuário é o autor do post
        database.session.delete(post)  # Deleta o post
        database.session.commit()  # Confirma a exclusão
        flash('Post excluído com sucesso!', 'success')
        
        return redirect(url_for('home'))  # Redireciona para a página inicial
    else:
        abort(403)