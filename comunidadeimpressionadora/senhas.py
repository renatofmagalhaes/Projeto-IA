import secrets
import string

# Gera uma senha aleatória
def gerar_senha(tamanho=12):
    # Define os caracteres que podem ser usados
    letras = string.ascii_letters  # abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
    numeros = string.digits  # 0123456789
    #simbolos = string.punctuation  # !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    
    # Combina todos os caracteres
    todos_caracteres = letras + numeros # + simbolos
    
    # Gera a senha
    senha = ''.join(secrets.choice(todos_caracteres) for _ in range(tamanho))
    return senha

# Verifica a força da senha
def verificar_forca_senha(senha):
    pontos = 0
    
    if len(senha) >= 12:
        pontos += 2
    elif len(senha) >= 8:
        pontos += 1
        
    if any(c.isupper() for c in senha): pontos += 1
    if any(c.islower() for c in senha): pontos += 1
    if any(c.isdigit() for c in senha): pontos += 1
    if any(c in string.punctuation for c in senha): pontos += 1
    
    if pontos < 2:
        return "Muito fraca"
    elif pontos < 3:
        return "Fraca"
    elif pontos < 4:
        return "Média"
    elif pontos < 5:
        return "Forte"
    else:
        return "Muito forte"

# Exemplo de uso
senha = gerar_senha(32)
print(f"Senha: {senha}")
print(f"Força: {verificar_forca_senha(senha)}")
