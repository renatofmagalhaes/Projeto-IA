from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FileField
from flask_wtf.file import FileAllowed, FileField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp, ValidationError
from comunidadeimpressionadora.models import Usuario
from flask_login import current_user


# FORMULÁRIO DE LOGIN
class FormLogin(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message='O email é obrigatório'),
        Email(message='Digite um email válido'),
        Length(min=13, max=40, message='O email deve ter entre 13 e 40 caracteres')  # max alterado para 40
    ])
    senha = PasswordField('Senha', validators=[
        DataRequired(message='A senha é obrigatória')
    ])
    lembrar_dados = BooleanField('Lembrar dados de acesso')
    botao_login = SubmitField('Login')

# FORMULÁRIO CRIAR CONTA
class FormCriarConta(FlaskForm):
    nome = StringField('Nome', validators=[
        DataRequired(message='O nome é obrigatório'),
        Length(min=3, max=30, message='O nome deve ter entre 3 e 30 caracteres')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='O email é obrigatório'),
        Email(message='Digite um email válido'),
        Length(min=13, max=40, message='O email deve ter entre 13 e 40 caracteres')  
    ])
    # FUNÇÃO DE VERIFICAÇÃO DE EMAIL - CRIAR CONTA
    def validate_email(self, email):
        # PESQUISA SE O EMAIL FOI CADASTRADO NO BANCO DE DADOS
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Email já cadastrado. Cadastre-se com outro email ou faça login para continuar')
    senha = PasswordField('Senha', validators=[
        DataRequired(message='A senha é obrigatória'),
        Length(min=8, max=20, message='A senha deve ter entre 8 e 20 caracteres'),
        Regexp(r'^(?=.*[A-Z])(?=.*[!@#$&*])(?=.*[0-9])(?=.*[a-z])',
               message='A senha deve conter pelo menos uma letra maiúscula, uma minúscula, um número e um caractere especial')
    ])
    confirmacao_senha = PasswordField('Confirmar Senha', validators=[
        DataRequired(message='A confirmação de senha é obrigatória'),
        EqualTo('senha', message='As senhas devem ser iguais')
    ])
    botao_criarconta = SubmitField('Criar Conta')

       # FORMULÁRIO CRIAR POST
class FormCriarPost(FlaskForm):
    titulo = StringField('Título', validators=[
        DataRequired(message='O título é obrigatório'),
        Length(min=2, max=120, message='O título deve ter entre 2 e 120 caracteres')
    ])
    corpo = TextAreaField('Escreva seu Post aqui', validators=[
        DataRequired(message='O corpo é obrigatório')
    ])
    botao_criarpost = SubmitField('Criar Post')

# FORMULÁRIO EDITAR PERFIL
class FormEditarPerfil(FlaskForm):
    nome = StringField('Nome', validators=[
        DataRequired(message='O nome é obrigatório'),
        Length(min=3, max=30, message='O nome deve ter entre 3 e 30 caracteres')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='O email é obrigatório'), 
        Email(message='Digite um email válido'),
        Length(min=13, max=40, message='O email deve ter entre 13 e 40 caracteres')
    ])

    # FUNÇÃO PARA VERIFICAR EMAIL - EDITAR PERFIL
    def validate_email(self, email):
        # Se o email informado for diferente do email atual do usuário
        if email.data != current_user.email:
            # pesquisa no banco de dados se existe algum usuário com o email informado
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Email já cadastrado. Cadastre-se com outro email ou faça login para continuar')

    foto_perfil = FileField('Atualizar Foto de Perfil', validators=[
        FileAllowed(['jpg', 'png'], message='Somente arquivos jpg e png são permitidos')
    ])
    curso_excel = BooleanField('Excel Impressionador')
    curso_vba = BooleanField('VBA Impressionador')
    curso_powerbi = BooleanField('Power BI Impressionador')
    curso_python = BooleanField('Python Impressionador')
    curso_ppt = BooleanField('PowerPoint Impressionador')
    curso_sql = BooleanField('SQL Impressionador')
    botao_submit_editarperfil = SubmitField('Confirmar Edição')

