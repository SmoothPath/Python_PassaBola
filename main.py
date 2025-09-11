#Importando bibliotecas
import re

usuarios: list = []
usuario_logado = None

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
    print("[3] Ver Perfil")
    print("[4] Sair da Conta")
    print("[5] Consultar Eventos")
    print("[0] Sair do Programa")
    print("---------------------------------")
   
def digita_email() -> str:
    """
    Essa função solicita que o usuário digite um e-mail,
    valida esse e-mail e retorna ele em string
    """
    email: str = input("Digite o seu e-mail: ")

    while "@" not in email or not email.endswith(".com"):
        email: str = input("E-mail inválido. Digite o e-mail novamente:exemplo@email.com ")

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

def cadastra_usuario() -> None:
    """
    Essa função solicita o nome do usuário,
    valida esse nome, chama as funções email e senha,
    e adiciona o usuário à lista de usuários.
    """
    nome: str = input("Digite o seu nome e sobrenome: ").strip()
    
    while len(nome.split(" ")) < 2:
        nome: str = input("O nome deve ter pelo menos duas palavras. Digite o nome novamente: ").strip()
        
    email: str = digita_email()

    for usuario in usuarios:
        while usuario[1] == email:
            email = input("E-mail já cadastrado. Digite o e-mail novamente: ")

    senha: str = digita_senha()

    termos_uso: str = input("Você aceita os termos de uso? (s/n) ")
   

    while termos_uso.lower() != "s":
        termos_uso: str = input("Você precisa aceitar os termos de uso para continuar (s): ")

    usuarios.append({"nome":nome, "email": email, "senha":senha})
    print("Usuário cadastrado com sucesso!")    



def fazer_login() -> None:
    """
    Essa função solicita o e-mail e senha do usuário e,
    caso corresponderem com algum usuário na lista,
    armazena esse usuário na variável do usuario_logado
    """
    global usuario_logado

    if not usuario_logado:
        email = digita_email()
        senha = digita_senha()

        for usuario in usuarios:
            if usuario[1] == email and usuario[2] == senha:
                usuario_logado = usuario
                print(f"Login realizado com sucesso! Bem-vindo, {usuario[0]}.\n")
                return

        print("E-mail ou senha incorretos.\n")
        return

    print("Você já está logado.\n")

def sair_da_conta() -> None:
    """
    Essa função muda a variável do usuário logado,
    fazendo um logout
    """
    global usuario_logado
    if usuario_logado:
        usuario_logado = None
        print("Você saiu da conta.\n")
    else:
        print("Você não está logado.\n")

def ver_perfil() -> None:
    """
    Essa função exibe os dados do usuário logado
    """
    if usuario_logado:
        print("\n------ Perfil ------")
        print(f"Nome: {usuario_logado[0]}")
        print(f"E-mail: {usuario_logado[1]}")
        
    else:
        print("Você precisa estar logado para ver o perfil.\n")

def menu_eventos_times() -> None:
    "Essa função é responsavel pela gestao do menu de criar eventos"
    while True:
        print("\n--- Eventos e Times ---")
        print("[1] Criar evento")
        print("[2] Listar eventos")
        print("[0] Voltar")
        op = input("Escolha: ").strip()

        if op == "1":
            criar_evento()
        elif op == "2":
            listar_eventos()
        elif op == "0":
            return
        else:
            print("Opção inválida.")

def criar_evento() -> None:
    """
    Cria um evento com: tipo de jogo e nº de jogadores por time.
    """
    print("\n--- Criar Evento ---")
    tipo = input("Tipo de jogo (ex.: Grupo idependente, Grupo patrocinado, Jogador avulso): ").strip()
    if not tipo:
        print(" Tipo de jogo não pode ser vazio.")
        return

    while True:
        n = input("Nº de jogadores por time (ex.: 5, 7, 11): ").strip()
        if not n.isdigit() or int(n) <= 0:
            print("Informe um número.")
            continue
        jogadores_por_time = int(n)
        break

    id = _novo_id("evento")
    eventos.append({
        "id": id,
        "tipo": tipo,
        "jogadores_por_time": jogadores_por_time,
        "times": []
    })
    print(f"✅ Evento #{id} criado: {tipo} | {jogadores_por_time} jogadores/time")


def listar_eventos() -> None:
    """
    Lista eventos cadastrados para conferência.
    """
    print("\n--- Eventos Cadastrados ---")
    if not eventos:
        print("(sem eventos)")
        return
    for ev in eventos:
        print(f"#{ev['id']} – {ev['tipo']} | {ev['jogadores_por_time']} por time | Times: {len(ev['times'])}")



def mostra_menu() -> None:
    print("---------------------------------")
    print("| BEM VINDO(A) AO PASSA A BOLA! |")
    print("| O que você deseja acessar?    |")
    print("---------------------------------")
    print("[1] Cadastrar Usuário")
    print("[2] Fazer Login")
    print("[3] Ver Perfil")
    print("[4] Sair da Conta")
    print("[5] Consultar Eventos")
    print("[0] Sair do Programa")
    print("---------------------------------")

def le_opcao_menu() -> int:
    while True:
        op = input("Digite a ação que deseja realizar: ").strip()
        if not op.isdigit():
            print("Informe um número válido.")
            continue
        return int(op)

while True:
    mostra_menu()
    numero_menu = le_opcao_menu()

    if numero_menu == 1:
        cadastra_usuario()
    elif numero_menu == 2:
        fazer_login()
    elif numero_menu == 3:
        ver_perfil()
    elif numero_menu == 4:
        sair_da_conta()
    elif numero_menu == 5:
        menu_eventos_times()    
    elif numero_menu == 6:
        print("Módulo de eventos ainda não implementado.\n")
    elif numero_menu == 0:
        print("Encerrando... até logo!")
        break
    else:
        print("Opção inválida.\n")
