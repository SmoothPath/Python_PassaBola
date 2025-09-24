import json
import os
import re
from typing import List, Dict, Optional
from math import ceil

# ============================================================
# ARQUIVOS DE DADOS
# ============================================================
ARQ_USUARIOS = "usuarios.json"
ARQ_EVENTOS = "eventos.json"
ARQ_TIMES = "times.json"

# ============================================================
# CARREGAR E SALVAR DADOS
# ============================================================
def carregar_dados(arquivo: str) -> List[Dict]:
    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def salvar_dados(arquivo: str, dados: List[Dict]) -> None:
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

# ============================================================
# VARIÁVEIS GLOBAIS
# ============================================================
usuarios: List[Dict] = carregar_dados(ARQ_USUARIOS)
eventos: List[Dict] = carregar_dados(ARQ_EVENTOS)
times: List[Dict] = carregar_dados(ARQ_TIMES)
usuario_logado: Optional[Dict] = None
_next_ids = {"evento": len(eventos)+1, "time": len(times)+1}

# ============================================================
# CONTA PADRÃO ADMIN
# ============================================================
ADMIN_PADRAO = {
    "nome": "Admin Principal",
    "email": "admin@passabola.com",
    "senha": "admin123",
    "perfil": "admin"
}

# ============================================================
# VALIDAÇÃO
# ============================================================
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

def input_int(msg: str) -> int:
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("⚠️ Digite um número válido.")

def input_str(msg: str) -> str:
    while True:
        valor = input(msg).strip()
        if valor:
            return valor
        print("⚠️ O campo não pode ficar vazio.")

def _novo_id(kind: str) -> int:
    _next_ids[kind] += 1
    return _next_ids[kind] - 1

# ============================================================
# USUÁRIOS / LOGIN
# ============================================================
def cadastrar_usuario() -> None:
    print("\n--- Cadastro de Usuário ---")
    nome = input_str("Nome completo: ")
    while len(nome.split()) < 2:
        nome = input_str("O nome deve ter pelo menos duas palavras. Digite novamente: ")
    while True:
        email = input_str("Email: ")
        if not EMAIL_REGEX.match(email):
            print("E-mail inválido. Exemplo: nome@dominio.com")
            continue
        if any(u["email"].lower() == email.lower() for u in usuarios):
            print("E-mail já cadastrado. Informe outro.")
            continue
        break
    senha = input_str("Senha: ")
    usuarios.append({"nome": nome, "email": email, "senha": senha, "perfil": "jogadora"})
    salvar_dados(ARQ_USUARIOS, usuarios)
    print("✅ Usuário cadastrado com sucesso!")

def login() -> Optional[Dict]:
    print("\n--- Login ---")
    print("1. Jogadora")
    print("2. Admin")
    tipo = input_int("Escolha: ")
    email = input_str("Email: ")
    senha = input_str("Senha: ")

    if tipo == 1:
        for u in usuarios:
            if u["email"] == email and u["senha"] == senha and u["perfil"] == "jogadora":
                print(f"✅ Bem-vinda, {u['nome']}!")
                return u
        print("❌ Email ou senha incorretos para jogadora.")
        return None
    elif tipo == 2:
        if email == ADMIN_PADRAO["email"] and senha == ADMIN_PADRAO["senha"]:
            print(f"✅ Bem-vindo, {ADMIN_PADRAO['nome']}!")
            return ADMIN_PADRAO
        else:
            print("❌ Email ou senha incorretos para admin.")
            return None
    else:
        print("⚠️ Tipo inválido.")
        return None

def ver_perfil(usuario: Dict) -> None:
    print("\n--- Perfil ---")
    print(f"Nome: {usuario['nome']}")
    print(f"Email: {usuario['email']}")
    print(f"Perfil: {usuario['perfil']}")

# ============================================================
# EVENTOS
# ============================================================
def listar_eventos() -> None:
    print("\n--- Eventos ---")
    if not eventos:
        print("⚠️ Nenhum evento cadastrado.")
        return
    for i, e in enumerate(eventos, 1):
        inscritos = len(e.get("inscritos", []))
        print(f"{i}. {e['nome']} - {e['local']} - {e['data']} ({inscritos} inscritos)")

def cadastrar_evento() -> None:
    print("\n--- Cadastrar Evento ---")
    nome = input_str("Nome: ")
    local = input_str("Local: ")
    data = input_str("Data: ")
    eventos.append({"id": _novo_id("evento"), "nome": nome, "local": local, "data": data, "inscritos": [], "times": [], "jogadoras_por_time": 5})
    salvar_dados(ARQ_EVENTOS, eventos)
    print("✅ Evento cadastrado!")

def inscrever_em_evento(jogadora: Dict) -> None:
    listar_eventos()
    if not eventos: return
    escolha = input_int("Número do evento para inscrição: ")
    if 1 <= escolha <= len(eventos):
        evento = eventos[escolha-1]
        if jogadora["email"] not in evento.get("inscritos", []):
            evento["inscritos"].append(jogadora["email"])
            salvar_dados(ARQ_EVENTOS, eventos)
            print(f"✅ {jogadora['nome']} inscrita em {evento['nome']}")
        else:
            print("⚠️ Já inscrita neste evento.")
    else:
        print("⚠️ Evento inválido.")

def ver_inscricoes(jogadora: Dict) -> None:
    print("\n--- Meus Eventos ---")
    encontrou = False
    for e in eventos:
        if jogadora["email"] in e.get("inscritos", []):
            print(f"- {e['nome']} ({e['data']}, {e['local']})")
            encontrou = True
    if not encontrou:
        print("⚠️ Nenhum evento inscrito.")

# ============================================================
# TIMES
# ============================================================
def listar_times() -> None:
    print("\n--- Times ---")
    if not times:
        print("⚠️ Nenhum time cadastrado.")
        return
    for t in times:
        ev = next((e for e in eventos if e["id"] == t["event_id"]), None)
        cap = ev["jogadoras_por_time"] if ev else "?"
        print(f"#{t['id']} • {t['nome']} | Evento #{t['event_id']} | {len(t['jogadoras'])}/{cap}")
        for j in t["jogadoras"]:
            print(f" · {j}")

def criar_time() -> None:
    listar_eventos()
    eid = input_int("ID do evento para criar time: ")
    evento = next((e for e in eventos if e["id"] == eid), None)
    if not evento:
        print("⚠️ Evento inválido.")
        return
    nome_time = input_str("Nome do time: ")
    tid = _novo_id("time")
    times.append({"id": tid, "nome": nome_time, "event_id": eid, "jogadoras": []})
    evento["times"].append(tid)
    salvar_dados(ARQ_EVENTOS, eventos)
    salvar_dados(ARQ_TIMES, times)
    print(f"✅ Time {nome_time} criado para o evento {evento['nome']}.")

# Função de adicionar jogadora a time
def adicionar_jogadora_time() -> None:
    listar_times()
    tid = input_int("ID do time: ")
    t = next((t for t in times if t["id"] == tid), None)
    if not t:
        print("⚠️ Time inválido.")
        return
    ev = next((e for e in eventos if e["id"] == t["event_id"]), None)
    if not ev:
        print("⚠️ Evento não encontrado.")
        return
    cap = ev["jogadoras_por_time"]
    if len(t["jogadoras"]) >= cap:
        print("⚠️ Time cheio.")
        return
    nome = input_str("Nome da jogadora: ")
    if nome in t["jogadoras"]:
        print("⚠️ Jogadora já neste time.")
        return
    t["jogadoras"].append(nome)
    salvar_dados(ARQ_TIMES, times)
    print(f"✅ Jogadora {nome} adicionada ao time {t['nome']}.")

# ============================================================
# MENUS
# ============================================================
def menu_jogadora(jogadora: Dict) -> None:
    while True:
        print("\n--- Menu Jogadora ---")
        print("1. Listar eventos")
        print("2. Inscrever-se em evento")
        print("3. Meus eventos")
        print("0. Logout")
        opc = input_int("Escolha: ")
        if opc == 1: listar_eventos()
        elif opc == 2: inscrever_em_evento(jogadora)
        elif opc == 3: ver_inscricoes(jogadora)
        elif opc == 0: break
        else: print("⚠️ Opção inválida.")

def menu_admin(admin: Dict) -> None:
    while True:
        print("\n--- Menu Admin ---")
        print("1. Cadastrar usuário")
        print("2. Listar usuários")
        print("3. Cadastrar evento")
        print("4. Listar eventos")
        print("5. Criar time")
        print("6. Listar times")
        print("7. Adicionar jogadora a time")
        print("0. Logout")
        opc = input_int("Escolha: ")
        if opc == 1: cadastrar_usuario()
        elif opc == 2:
            for i, u in enumerate(usuarios, 1):
                print(f"{i}. {u['nome']} - {u['email']} ({u['perfil']})")
        elif opc == 3: cadastrar_evento()
        elif opc == 4: listar_eventos()
        elif opc == 5: criar_time()
        elif opc == 6: listar_times()
        elif opc == 7: adicionar_jogadora_time()
        elif opc == 0: break
        else: print("⚠️ Opção inválida.")

def menu_principal() -> None:
    global usuario_logado
    while True:
        print("\n=== Passa a Bola ===")
        print("1. Cadastrar usuário")
        print("2. Login")
        print("0. Sair")
        opc = input_int("Escolha: ")
        if opc == 1: cadastrar_usuario()
        elif opc == 2:
            usuario_logado = login()
            if usuario_logado:
                if usuario_logado["perfil"] == "jogadora": menu_jogadora(usuario_logado)
                elif usuario_logado["perfil"] == "admin": menu_admin(usuario_logado)
        elif opc == 0: break
        else: print("⚠️ Opção inválida.")

# ============================================================
# EXECUÇÃO
# ============================================================
if __name__ == "__main__":
    menu_principal()
