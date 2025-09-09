#Importando bibliotecas
import re


def mostra_menu() -> None:
    """
    Essa função exibe um menu com as funcionalidades do sistema
    """
    print("---------------------------------")
    print("| BEM VINDO(A) AO PASSA A BOLA! |")
    print("|                               |")
    print("| O que você deseja acessar?    |")
    print("---------------------------------")
    print("[1] Cadastrar Usuário")
    print("[2] Fazer Login")
    print("[3] Consultar Eventos")
    print("[4] Sair da Conta")
    print("[5] Ver Perfil")
    print("---------------------------------")
   
def digita_email() -> str:
    """
    Essa função solicita que o usuário digite um e-mail,
    valida esse e-mail e retorna ele em string
    """
    email: str = input("Digite o seu e-mail: ")

    while not email.find("@") or not email.endswith(".com"):
        email: str = input("E-mail inválido. Digite o e-mail novamente: ")

    return email


def digita_senha() -> str:
    """
    Essa função solicita que o usuário digite uma senha,
    valida ela, e retorna ela em string
    """
    senha: str = input("Digite a sua senha: ")

    while not (len(senha) >= 8 and
           re.search(r"[A-Z]", senha) and
           re.search(r"[a-z]", senha) and
           re.search(r"[0-9]", senha) and
           re.search(r"[\W_]", senha)):

        senha: str = input("A senha deve ter pelo menos 8 caracteres, um número, uma letra maiúscula e minúscula, e um simbolo. Digite a senha novamente: ")


    return senha

