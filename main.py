
# === IMPORTAÇÕES =============================================================
import re


# === DADOS EM MEMÓRIA ========================================================
usuarios: list[dict] = []          # {"nome": str, "email": str, "senha": str}
usuario_logado: dict | None = None

eventos: list[dict] = []           # {"id": int, "tipo": str, "jogadoras_por_time": int, "times": list[int]}
times: list[dict] = []             # {"id": int, "nome": str, "event_id": int, "jogadoras": list[str]}

_next_ids = {"evento": 1, "time": 1}


# === HELPERS / UTILITÁRIOS ==================================================
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

def _novo_id(kind: str) -> int:
    _next_ids[kind] += 1
    return _next_ids[kind] - 1

def pausa() -> None:
    input("\nPressione ENTER para continuar...")

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

def le_nao_vazio(msg: str) -> str:
    while True:
        s = input(msg).strip()
        if s:
            return s
        print("O valor não pode ser vazio.")

def obter_evento_por_id(eid: int) -> dict | None:
    return next((e for e in eventos if e["id"] == eid), None)

def obter_time_por_id(tid: int) -> dict | None:
    return next((t for t in times if t["id"] == tid), None)

def escolher_evento_id() -> int | None:
    """
    Lista e solicita um ID de evento válido.
    """
    if not eventos:
        print("= Não há eventos. Crie um antes.")
        return None
    listar_eventos()
    while True:
        s = input("ID do evento: ").strip()
        if not s.isdigit():
            print("Digite um número válido.")
            continue
        eid = int(s)
        if any(ev["id"] == eid for ev in eventos):
            return eid
        print(" Evento não encontrado.")

def escolher_time_id(eid: int | None = None) -> int | None:
    """
    Lista e solicita um ID de time válido (opcionalmente filtrado por evento).
    """
    if not times:
        print("(sem times cadastrados)")
        return None

    if eid is not None:
        listar_times_por_evento(eid)
        base = [t for t in times if t["event_id"] == eid]
        if not base:
            print(f"(evento #{eid} ainda não tem times)")
            return None
    else:
        listar_times()

    while True:
        s = input("ID do time: ").strip()
        if not s.isdigit():
            print("Digite um número válido.")
            continue
        tid = int(s)
        t = obter_time_por_id(tid)
        if t and (eid is None or t["event_id"] == eid):
            return tid
        print(" Time não encontrado.")

        
# === USUÁRIO / AUTENTICAÇÃO =================================================
def digita_email(checagem_unicidade: bool = False) -> str:
    """
    Lê um e-mail válido. Se checagem_unicidade=True, impede duplicados.
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
    Senha válida:
    - mínimo 8 chars
    - 1 maiúscula, 1 minúscula, 1 número e 1 símbolo
    """
    senha: str = input("Digite a sua senha: ").strip()
    while not (len(senha) >= 8 and
               re.search(r"[A-Z]", senha) and
               re.search(r"[a-z]", senha) and
               re.search(r"[0-9]", senha) and
               re.search(r"[\W_]", senha)):
        senha = input(
            "A senha deve ter pelo menos 8 caracteres, um número, uma letra maiúscula e minúscula, "
            "e um símbolo. Digite a senha novamente: "
        ).strip()
    return senha

def aceita_termos() -> None:
    while True:
        v = input("Você aceita os termos de uso? (s/n) ").strip().lower()
        if v == "s":
            return
        print("Você precisa aceitar os termos de uso para continuar (responda 's').")

def cadastra_usuario() -> None:
    """
    Solicita nome completo, e-mail único, senha válida e termos.
    """
    nome: str = input("Digite o seu nome e sobrenome: ").strip()
    while len([p for p in nome.split() if p]) < 2:
        nome = input("O nome deve ter pelo menos duas palavras. Digite o nome novamente: ").strip()

    email: str = digita_email(checagem_unicidade=True)
    senha: str = digita_senha()
    aceita_termos()

    usuarios.append({"nome": nome, "email": email, "senha": senha})
    print(" Usuário cadastrado com sucesso!")

def fazer_login() -> None:
    """
    Autentica por e-mail (case-insensitive) e senha.
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
    Faz logout do usuário logado.
    """
    global usuario_logado
    if usuario_logado:
        usuario_logado = None
        print("Você saiu da conta.\n")
    else:
        print("Você não está logado.\n")

def ver_perfil() -> None:
    """
    Exibe dados do usuário logado (sem mostrar senha).
    """
    if usuario_logado:
        print("\n------ Perfil ------")
        print(f"Nome:  {usuario_logado.get('nome')}")
        print(f"E-mail:{usuario_logado.get('email')}")
    else:
        print("Você precisa estar logado para ver o perfil.\n")


# === ADMIN ==================================================================
ADMIN_PIN = "1234"  # troque depois

def exige_admin() -> bool:
    """
    Pede o PIN do admin (3 tentativas).
    """
    tentativas = 3
    while tentativas > 0:
        pin = input("PIN do admin: ").strip()
        if pin == ADMIN_PIN:
            return True
        tentativas -= 1
        print(f"PIN incorreto. Tentativas restantes: {tentativas}")
    print("Acesso de admin negado.")
    return False


# === EVENTOS (CRUD BÁSICO + CONFIG) =========================================
def listar_eventos() -> None:
    """
    Lista eventos cadastrados.
    """
    print("\n--- Eventos Cadastrados ---")
    if not eventos:
        print("(sem eventos)")
        return
    for ev in eventos:
        print(f"#{ev['id']} – {ev['tipo']} | {ev['jogadoras_por_time']} por time | Times: {len(ev['times'])}")

def escolher_evento_id() -> int | None:
    """
    Lista e solicita um ID de evento válido.
    """
    if not eventos:
        print("= Não há eventos. Crie um antes.")
        return None
    listar_eventos()
    while True:
        s = input("ID do evento: ").strip()
        if not s.isdigit():
            print("Digite um número válido.")
            continue
        eid = int(s)
        if any(ev["id"] == eid for ev in eventos):
            return eid
        print(" Evento não encontrado.")

def criar_evento() -> None:
    """
    Cria um evento com: tipo de jogo e nº de jogadoras por time.
    """
    print("\n--- Criar Evento ---")
    tipo = input("Tipo de jogo (ex.: Amistoso, Oitavas, Quartas de final, Semi-final, Final): ").strip()
    if not tipo:
        print(" Tipo de jogo não pode ser vazio.")
        return

    jogadoras_por_time = le_inteiro_positivo("Nº de jogadoras por time (ex.: 5, 7, 11): ")

    evento_id = _novo_id("evento")
    eventos.append({
        "id": evento_id,
        "tipo": tipo,
        "jogadoras_por_time": jogadoras_por_time,
        "times": []
    })
    print(f" Evento #{evento_id} criado: {tipo} | {jogadoras_por_time} jogadoras/time")

def configurar_evento_jogadoras_por_time() -> None:
    """
    ADMIN: altera o nº de jogadoras por time de um evento existente.
    (Quando o módulo de times estiver ativo, bloquear redução abaixo do já inscrito.)
    """
    print("\n--- Configurar Evento (ADMIN) ---")
    if not exige_admin():
        return

    eid = escolher_evento_id()
    if eid is None:
        return

    ev = next(e for e in eventos if e["id"] == eid)
    atual = ev["jogadoras_por_time"]
    print(f"Evento #{eid} — {ev['tipo']} | atual: {atual} jogadoras/time")

    novo = le_inteiro_positivo("Novo nº de jogadoras por time: ")

   
    ev["jogadoras_por_time"] = novo
    print(f" Configurado: {atual} → {novo} jogadoras/time para o Evento #{eid}.")


# === RELATÓRIOS =============================================================
def relatorios() -> None:
    while True:
        print("\n--- Relatórios ---")
        print("[1] Usuários")
        print("[2] Eventos")
        print("[3] Times")
        print("[0] Voltar")
        op = input("Escolha: ").strip()

        if op == "1":
            relatorio_usuarios()
            pausa()
        elif op == "2":
            relatorio_eventos()
            pausa()
        elif op == "3":
            relatorio_times()
            pausa()
        elif op == "0":
            return
        else:
            print("Opção inválida.")

def relatorio_usuarios() -> None:
    print("\n— Usuários —")
    if not usuarios:
        print("(vazio)")
        return
    for i, u in enumerate(usuarios, start=1):
        nome = u.get("nome", "(sem nome)")
        email = u.get("email", "(sem e-mail)")
        print(f"{i:02d}. {nome} <{email}>")

def relatorio_eventos() -> None:
    print("\n— Eventos —")
    if not eventos:
        print("(vazio)")
        return
    for ev in eventos:
        eid = ev.get("id")
        tipo = ev.get("tipo", "(sem tipo)")
        cap = ev.get("jogadoras_por_time", "?")
        qtd_times = len(ev.get("times", []))
        print(f"#{eid} • {tipo} | {cap} jogadoras/time | {qtd_times} time(s)")

def relatorio_times() -> None:
    print("\n— Times —")
    if not times:
        print("(vazio)")
        return

    for t in times:
        tid = t.get("id")
        nome = t.get("nome", "(sem nome)")
        event_id = t.get("event_id", "?")
        jogadoras = t.get("jogadoras", [])
        cap = "?"
        ev = next((e for e in eventos if e.get("id") == event_id), None)
        if ev:
            cap = ev.get("jogadoras_por_time", "?")

        print(f"Time #{tid} • {nome} | Evento #{event_id} | {len(jogadoras)}/{cap} jogadoras")
        for j in jogadoras:
            print(f"   · {j}")


# === TIMES  ====================================

def listar_times() -> None:
    print("\n— Times (geral) —")
    if not times:
        print("(vazio)")
        return
    for t in times:
        ev = obter_evento_por_id(t["event_id"])
        cap = ev["jogadoras_por_time"] if ev else "?"
        print(f"#{t['id']} • {t['nome']} | Evento #{t['event_id']} | {len(t['jogadoras'])}/{cap}")
        for j in t["jogadoras"]:
            print(f"   · {j}")

def listar_times_por_evento(eid: int) -> None:
    print(f"\n— Times do Evento #{eid} —")
    base = [t for t in times if t["event_id"] == eid]
    if not base:
        print("(nenhum time para este evento)")
        return
    ev = obter_evento_por_id(eid)
    cap = ev["jogadoras_por_time"] if ev else "?"
    for t in base:
        print(f"#{t['id']} • {t['nome']} | {len(t['jogadoras'])}/{cap}")
        for j in t["jogadoras"]:
            print(f"   · {j}")

def criar_time() -> None:
    print("\n--- Criar Time ---")
    eid = escolher_evento_id()
    if eid is None:
        return
    nome = le_nao_vazio("Nome do time: ")
    tid = _novo_id("time")
    times.append({"id": tid, "nome": nome, "event_id": eid, "jogadoras": []})
    ev = obter_evento_por_id(eid)
    ev["times"].append(tid)
    print(f" Time #{tid} criado no Evento #{eid}: {nome}")

def excluir_time() -> None:
    print("\n--- Excluir Time ---")
    eid = escolher_evento_id()
    if eid is None:
        return
    tid = escolher_time_id(eid)
    if tid is None:
        return
    t = obter_time_por_id(tid)
    ev = obter_evento_por_id(t["event_id"]) if t else None
    
    idx = next((i for i, x in enumerate(times) if x["id"] == tid), None)
    if idx is not None:
        times.pop(idx)
  
    if ev:
        ev["times"] = [x for x in ev["times"] if x != tid]
    print(f" Time #{tid} excluído.")

def adicionar_jogadora() -> None:
    print("\n--- Adicionar Jogadora ---")
    eid = escolher_evento_id()
    if eid is None:
        return
    tid = escolher_time_id(eid)
    if tid is None:
        return

    t = obter_time_por_id(tid)
    ev = obter_evento_por_id(eid)
    cap = ev["jogadoras_por_time"]

    if len(t["jogadoras"]) >= cap:
        print(" Este time já está no limite de jogadoras.")
        return

    nome = le_nao_vazio("Nome da jogadora: ")
    if nome in t["jogadoras"]:
        print(" Jogadora já está nesse time.")
        return
    t["jogadoras"].append(nome)
    print(f" Jogadora '{nome}' adicionada ao Time #{tid}.")

def remover_jogadora() -> None:
    print("\n--- Remover Jogadora ---")
    eid = escolher_evento_id()
    if eid is None:
        return
    tid = escolher_time_id(eid)
    if tid is None:
        return

    t = obter_time_por_id(tid)
    if not t["jogadoras"]:
        print(" Este time não possui jogadoras.")
        return

    nome = le_nao_vazio("Nome da jogadora para remover: ")
    if nome not in t["jogadoras"]:
        print(" Jogadora não encontrada no time.")
        return
    t["jogadoras"].remove(nome)
    print(f" Jogadora '{nome}' removida do Time #{tid}.")

def _chunks_round_robin(itens: list[str], n_grupos: int) -> list[list[str]]:
    grupos = [[] for _ in range(n_grupos)]
    for i, x in enumerate(itens):
        grupos[i % n_grupos].append(x)
    return grupos

def montar_times_automaticamente() -> None:
    """
    responsavel por receber, verificar e criar times auto
    """
    print("\n--- Montar Times Automaticamente ---")
    eid = escolher_evento_id()
    if eid is None:
        return
    ev = obter_evento_por_id(eid)
    cap = ev["jogadoras_por_time"]

    nomes_raw = le_nao_vazio("Cole os nomes separados por vírgula: ")
    nomes = [n.strip() for n in nomes_raw.split(",") if n.strip()]
    if not nomes:
        print("Nenhum nome informado.")
        return

    
    from math import ceil
    n_times = ceil(len(nomes) / cap)

 
    grupos = _chunks_round_robin(nomes, n_times)

    # cria times com nomes padrão (Time A, B, C...)
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i, grupo in enumerate(grupos):
        tid = _novo_id("time")
        nome_time = f"Time {alfabeto[i]}" if i < len(alfabeto) else f"Time {i+1}"
        times.append({"id": tid, "nome": nome_time, "event_id": eid, "jogadoras": grupo[:cap]})
        ev["times"].append(tid)
        print(f" Criado #{tid} • {nome_time} ({len(grupo[:cap])}/{cap})")

    print(" Times gerados com sucesso!")

def menu_times() -> None:
    """
    Menu de gestão de times.
    """
    while True:
        print("\n--- Times ---")
        print("[1] Criar time")
        print("[2] Listar times (geral)")
        print("[3] Listar times por evento")
        print("[4] Adicionar jogadora em um time")
        print("[5] Remover jogadora de um time")
        print("[6] Excluir time")
        print("[7] Montar times automaticamente (lista de nomes)")
        print("[0] Voltar")
        op = input("Escolha: ").strip()

        if op == "1":
            criar_time(); pausa()
        elif op == "2":
            listar_times(); pausa()
        elif op == "3":
            eid = escolher_evento_id()
            if eid is not None:
                listar_times_por_evento(eid)
            pausa()
        elif op == "4":
            adicionar_jogadora(); pausa()
        elif op == "5":
            remover_jogadora(); pausa()
        elif op == "6":
            excluir_time(); pausa()
        elif op == "7":
            montar_times_automaticamente(); pausa()
        elif op == "0":
            return
        else:
            print("Opção inválida.")



# === MENUS / UI =============================================================
def mostra_menu() -> None:
    """
    Exibe o menu principal do sistema.
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
    print("[5] Eventos e Times")
    print("[6] Relatórios")
    print("[0] Sair do Programa")
    print("---------------------------------")

def le_opcao_menu() -> int:
    while True:
        op = input("Digite a ação que deseja realizar: ").strip()
        if not op.isdigit():
            print("Informe um número válido.")
            continue
        return int(op)

def menu_eventos_times() -> None:
    """
    Menu de gestão de eventos (e, futuramente, times).
    """
    while True:
        print("\n--- Eventos e Times ---")
        print("[1] Criar evento")
        print("[2] Listar eventos")
        print("[3] Configurar jogadoras/time (ADMIN)")
        print("[4] Times")
        print("[0] Voltar")
        op = input("Escolha: ").strip()

        if op == "1":
            criar_evento()
           
        elif op == "2":
            listar_eventos()
            
        elif op == "3":
            configurar_evento_jogadoras_por_time()
            
        elif op == "4":
            menu_times()
               
        elif op == "0":
            return
        else:
            print("Opção inválida.")


# === LOOP PRINCIPAL =========================================================
if __name__ == "__main__":
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
            relatorios()
        elif numero_menu == 0:
            print("Encerrando... até logo!")
            break
        else:
            print("Opção inválida.\n")