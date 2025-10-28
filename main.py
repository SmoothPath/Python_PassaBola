"""
Sistema Passa a Bola (versão integrada)
--------------------------------------
Gerencia usuários, eventos e times com persistência em JSON.
Inclui nova funcionalidade: ranking de jogadoras mais ativas,
gerado localmente e acessível via integração com site (Node.js + React).
"""

import json
import os
import re
from typing import List, Dict, Optional

# ============================================================
# ARQUIVOS DE DADOS
# ============================================================
ARQ_USUARIOS = "usuarios.json"
ARQ_EVENTOS = "eventos.json"
ARQ_TIMES = "times.json"
ARQ_RANKING = "ranking.json"

# ============================================================
# FUNÇÕES AUXILIARES DE ARQUIVOS
# ============================================================
def carregar_dados(arquivo: str) -> List[Dict]:
    """Carrega dados de um arquivo JSON, se existir."""
    if os.path.exists(arquivo):
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"⚠️ Erro ao ler {arquivo}, iniciando vazio.")
    return []

def salvar_dados(arquivo: str, dados: List[Dict]) -> None:
    """Salva uma lista de dicionários em arquivo JSON."""
    try:
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Erro ao salvar {arquivo}: {e}")

# ============================================================
# VARIÁVEIS GLOBAIS
# ============================================================
usuarios: List[Dict] = carregar_dados(ARQ_USUARIOS)
eventos: List[Dict] = carregar_dados(ARQ_EVENTOS)
times: List[Dict] = carregar_dados(ARQ_TIMES)
usuario_logado: Optional[Dict] = None
_next_ids = {"evento": len(eventos) + 1, "time": len(times) + 1}

# ============================================================
# DADOS PADRÃO
# ============================================================
ADMIN_PADRAO = {
    "nome": "Admin Principal",
    "email": "admin@passabola.com",
    "senha": "admin123",
    "perfil": "admin"
}

EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

# ============================================================
# FUNÇÕES DE ENTRADA E VALIDAÇÃO
# ============================================================
def input_int(msg: str) -> int:
    """Solicita entrada numérica válida."""
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("Digite um número válido.")

def input_str(msg: str) -> str:
    """Solicita string não vazia."""
    while True:
        valor = input(msg).strip()
        if valor:
            return valor
        print("O campo não pode ficar vazio.")

def _novo_id(tipo: str) -> int:
    """Gera novo ID incremental."""
    _next_ids[tipo] += 1
    return _next_ids[tipo] - 1

# ============================================================
# CRUD USUÁRIOS
# ============================================================
def cadastrar_usuario() -> None:
    """Cadastra novo usuário (jogadora)."""
    print("\n--- Cadastro de Usuário ---")
    nome = input_str("Nome completo: ")
    while len(nome.split()) < 2:
        nome = input_str("Digite nome e sobrenome: ")

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
    print("Usuário cadastrado com sucesso!")

def login() -> Optional[Dict]:
    """Realiza login de jogadora ou admin."""
    print("\n--- Login ---")
    print("1. Jogadora")
    print("2. Admin")
    tipo = input_int("Escolha: ")
    email = input_str("Email: ")
    senha = input_str("Senha: ")

    try:
        if tipo == 1:
            for u in usuarios:
                if u["email"] == email and u["senha"] == senha:
                    print(f"Bem-vinda, {u['nome']}!")
                    return u
            print("Credenciais incorretas.")
        elif tipo == 2 and email == ADMIN_PADRAO["email"] and senha == ADMIN_PADRAO["senha"]:
            print(f"Bem-vindo, {ADMIN_PADRAO['nome']}!")
            return ADMIN_PADRAO
        else:
            print("Acesso negado.")
    except Exception as e:
        print(f"Erro no login: {e}")
    return None

# ============================================================
# EVENTOS
# ============================================================
def listar_eventos() -> None:
    """Lista eventos disponíveis."""
    print("\n--- Eventos ---")
    if not eventos:
        print("Nenhum evento cadastrado.")
        return
    for e in eventos:
        inscritos = len(e.get("inscritos", []))
        print(f"#{e['id']} - {e['nome']} ({e['local']} | {e['data']}) [{inscritos} inscritas]")

def cadastrar_evento() -> None:
    """Cadastra novo evento."""
    nome = input_str("Nome: ")
    local = input_str("Local: ")
    data = input_str("Data: ")
    eventos.append({
        "id": _novo_id("evento"),
        "nome": nome,
        "local": local,
        "data": data,
        "inscritos": [],
        "times": [],
        "jogadoras_por_time": 5
    })
    salvar_dados(ARQ_EVENTOS, eventos)
    print("Evento cadastrado!")

def inscrever_em_evento(jogadora: Dict) -> None:
    """Inscreve jogadora em evento."""
    listar_eventos()
    if not eventos:
        return
    escolha = input_int("ID do evento: ")
    evento = next((e for e in eventos if e["id"] == escolha), None)
    if not evento:
        print("Evento inválido.")
        return
    if jogadora["email"] in evento["inscritos"]:
        print("Já inscrita.")
        return
    evento["inscritos"].append(jogadora["email"])
    salvar_dados(ARQ_EVENTOS, eventos)
    print(f"{jogadora['nome']} inscrita em {evento['nome']}.")
    gerar_ranking()  # Atualiza ranking automaticamente

# ============================================================
# NOVA FUNCIONALIDADE: RANKING
# ============================================================
def gerar_ranking() -> None:
    """
    Gera um ranking de jogadoras baseado na quantidade de eventos em que estão inscritas.
    Salva o resultado em ranking.json e envia para o servidor Node.js.
    """
    try:
        import requests  # <--- Adicione aqui

        contagem = {}
        for e in eventos:
            for email in e.get("inscritos", []):
                contagem[email] = contagem.get(email, 0) + 1

        ranking = []
        for email, qtd in sorted(contagem.items(), key=lambda x: x[1], reverse=True):
            jogadora = next((u for u in usuarios if u["email"] == email), None)
            if jogadora:
                ranking.append({
                    "nome": jogadora["nome"],
                    "email": email,
                    "eventos": qtd
                })

        salvar_dados(ARQ_RANKING, ranking)
        print("🏆 Ranking atualizado com sucesso!")

        # Enviar ranking para o Node.js
        try:
            response = requests.post(
                "http://localhost:5000/api/ranking",
                json=ranking,
                timeout=5
            )
            if response.status_code == 200:
                print("✅ Ranking enviado ao site com sucesso!")
            else:
                print(f"⚠️ Falha ao enviar ranking: {response.status_code}")
        except Exception as e:
            print(f"🚫 Erro ao conectar ao Node.js: {e}")

    except Exception as e:
        print(f"Erro ao gerar ranking: {e}")


def mostrar_ranking() -> None:
    """Exibe o ranking local."""
    ranking = carregar_dados(ARQ_RANKING)
    print("\n--- Ranking de Participação ---")
    if not ranking:
        print("Nenhum dado disponível.")
        return
    for i, j in enumerate(ranking, 1):
        print(f"{i}. {j['nome']} ({j['eventos']} eventos)")

# ============================================================
# MENUS
# ============================================================
def menu_jogadora(jogadora: Dict) -> None:
    """Menu para jogadoras."""
    while True:
        print("\n--- Menu Jogadora ---")
        print("1. Listar eventos")
        print("2. Inscrever-se em evento")
        print("3. Ver ranking")
        print("0. Logout")
        opc = input_int("Escolha: ")
        if opc == 1:
            listar_eventos()
        elif opc == 2:
            inscrever_em_evento(jogadora)
        elif opc == 3:
            mostrar_ranking()
        elif opc == 0:
            break
        else:
            print("Opção inválida.")

def menu_admin(admin: Dict) -> None:
    """Menu para administradores."""
    while True:
        print("\n--- Menu Admin ---")
        print("1. Cadastrar usuário")
        print("2. Cadastrar evento")
        print("3. Listar eventos")
        print("4. Gerar ranking")
        print("0. Logout")
        opc = input_int("Escolha: ")
        if opc == 1:
            cadastrar_usuario()
        elif opc == 2:
            cadastrar_evento()
        elif opc == 3:
            listar_eventos()
        elif opc == 4:
            gerar_ranking()
        elif opc == 0:
            break
        else:
            print("Opção inválida.")

# ============================================================
# EXECUÇÃO PRINCIPAL
# ============================================================
def menu_principal() -> None:
    """Interface inicial do sistema."""
    global usuario_logado
    while True:
        print("\n=== Passa a Bola ===")
        print("1. Cadastrar usuário")
        print("2. Login")
        print("0. Sair")
        opc = input_int("Escolha: ")
        if opc == 1:
            cadastrar_usuario()
        elif opc == 2:
            usuario_logado = login()
            if usuario_logado:
                if usuario_logado["perfil"] == "jogadora":
                    menu_jogadora(usuario_logado)
                elif usuario_logado["perfil"] == "admin":
                    menu_admin(usuario_logado)
        elif opc == 0:
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu_principal()
