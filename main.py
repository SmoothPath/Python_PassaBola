#Importando bibliotecas
import re

usuarios: list = []
usuario_logado = None

# === Estruturas para eventos (necessárias para o menu de eventos) ===
eventos: list[dict] = []   # cada evento: {"id": int, "tipo": str, "jogadores_por_time": int, "times": list[int]}

_next_ids = {"evento": 1, "time": 1}
def _novo_id(kind: str) -> int:
    _next_ids[kind] += 1
    return _next_ids[kind] - 1

# === Helpers de validação ===
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

def le_inteiro_positivo(msg: str) -> int:
    while True:
        s = input(msg).strip()
        if not s or not s.isdigit():
            print("Informe um número inteiro positivo.")
            continue
        n = int(s)
        if n <= 0:
            print("O número deve ser maior que zero.")
            continue
        return n

def aceita_termos() -> None:
    while True:
        v = input("Você aceita os termos de uso? (s/n) ").strip().lower()
        if v == "s":
            return
        print("Você precisa aceitar os termos de uso para continuar (responda 's').")


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
   
def digita_email(checagem_unicidade: bool = False) -> str:
    """
    Lê um e-mail válido (regex).
    Se checagem_unicidade=True, impede e-mails já cadastrados.
    """
    while True:
        email: str = input("Digite o seu e-mail: ").strip()
        if not EMAIL_REGEX.match(email):
            print("E-mail inválido. Exemplo válido: nome@dominio.com")
            continue

        if checagem_unicidade and any(u["email"].lower() == email.lower() for u in usuarios):
            print("E-mail já cadastrado. Informe outro.")
            continue

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
        
    while True:
        email: str = digita_email()
        if any(u["email"].lower() == email.lower() for u in usuarios):
            print("❌ E-mail já cadastrado. Digite outro.")
            continue
        break

    senha: str = digita_senha()

    termos_uso: str = input("Você aceita os termos de uso? (s/n) ")
   

    while termos_uso.lower() != "s":
        termos_uso: str = input("Você precisa aceitar os termos de uso para continuar (s): ")

    usuarios.append({"nome":nome, "email": email, "senha":senha})
    print("Usuário cadastrado com sucesso!")    



def fazer_login() -> None:
    """
    Autentica usando dicts {nome, email, senha}.
    Compara e-mail de forma case-insensitive.
    """
    global usuario_logado

    if usuario_logado:
        print("Você já está logado.\n")
        return

    email = input("E-mail: ").strip()
    senha = input("Senha: ").strip()

    for u in usuarios:
        if u.get("email", "").lower() == email.lower() and u.get("senha", "") == senha:
            usuario_logado = u
            print(f" Login realizado com sucesso! Bem-vindo, {u.get('nome','usuário')}.\n")
            return

    print(" E-mail ou senha incorretos.\n")


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
        print(f"Nome: {usuario_logado.get('nome')}")
        print(f"E-mail: {usuario_logado.get('email')}")
        
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
    tipo = input("Tipo de jogo (ex.: Amistoso, Oitavas, quartas de final, semi-final, final): ").strip()
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
