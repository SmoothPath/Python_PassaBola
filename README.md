# Sistema Passa a Bola 

## Visão Geral
O **Passa a Bola** é um sistema local de gerenciamento de **usuárias (jogadoras)**, **eventos esportivos** e **times**, com **armazenamento persistente em arquivos JSON**.  
Esse sistema inclui uma **funcionalidade de ranking** que contabiliza a participação das jogadoras e envia os resultados automaticamente para o site desenvolvido em **Node.js + React**.

---

## Funcionalidades Principais

### 1. Gerenciamento de Usuários
- Cadastro de novas jogadoras com **validação de e-mail** e **verificação de duplicidade**.  
- Login de jogadoras e administradores (com credenciais padrão `admin@passabola.com / admin123`).  
- Armazenamento persistente das informações em `usuarios.json`.

**Campos de Usuário:**
```json
{
  "nome": "Nome Completo",
  "email": "email@exemplo.com",
  "senha": "senha123",
  "perfil": "jogadora"
}
```

---

### 2. Gerenciamento de Eventos
- Criação e listagem de eventos esportivos, incluindo nome, local, data e limite padrão de jogadoras por time.  
- Cada evento possui uma lista de inscritas e times associados.  
- Armazenamento em `eventos.json`.

**Campos de Evento:**
```json
{
  "id": 1,
  "nome": "Torneio de Primavera",
  "local": "Quadra Central",
  "data": "20/11/2025",
  "inscritos": ["email1@...", "email2@..."],
  "times": [],
  "jogadoras_por_time": 5
}
```

**Ações disponíveis:**
- `Listar eventos` – Exibe todos os eventos cadastrados com número de inscritas.  
- `Cadastrar evento` – Permite ao administrador criar novos eventos.  
- `Inscrever-se em evento` – Permite que a jogadora se inscreva em um evento e atualiza automaticamente o ranking.

---

### 3. Persistência de Dados
O sistema utiliza arquivos JSON para simular um banco de dados local:
- `usuarios.json` – cadastro de jogadoras.  
- `eventos.json` – lista de eventos e inscrições.  
- `times.json` – armazenamento dos times formados automaticamente a partir das inscrições de cada evento.  
- `ranking.json` – ranking de jogadoras mais ativas.

Todas as operações de escrita e leitura são realizadas via funções utilitárias:
- `carregar_dados()` – lê o conteúdo de um arquivo JSON existente.  
- `salvar_dados()` – salva uma lista de dicionários no formato JSON com identação e codificação UTF-8.

---

### 4. Ranking de Jogadoras Mais Ativas

- O ranking é **gerado automaticamente** sempre que uma jogadora se inscreve em um evento.  
- A contagem considera **quantos eventos cada jogadora participou**.  
- Os dados são salvos em `ranking.json` e também **enviados via HTTP POST** para a API do site:
  ```
  http://localhost:5000/api/ranking
  ```
- Caso a API esteja fora do ar, o sistema exibe aviso sem interromper a execução.  
- O ranking também pode ser visualizado localmente pelo menu.

**Formato do ranking:**
```json
[
  {
    "nome": "Ana Souza",
    "email": "ana@exemplo.com",
    "eventos": 3
  },
  {
    "nome": "Beatriz Lima",
    "email": "bia@exemplo.com",
    "eventos": 2
  }
]

```
**Funções principais:**
- `gerar_ranking()` – recalcula o ranking com base nas inscrições.  
- `mostrar_ranking()` – exibe o ranking local ordenado por número de participações.  

--- 

### 5. Formação Automática de Times

- O sistema conta com uma funcionalidade para formação automática de times em cada evento.
- Quando o evento atinge o número necessário de inscritas definido pelo campo `jogadoras_por_time`, os times são criados automaticamente e armazenados no arquivo `times.json`.
- Cada time é formado de maneira sequencial (as primeiras `N`jogadoras formam o Time 1, as próximas `N` o Time 2, etc.).
- Caso o número de inscritas não seja múltiplo do limite, o último time ficará com menos jogadoras.

**Função principal:**

`formar_times(evento)` – percorre a lista de inscritas de um evento e cria grupos de acordo com o número configurado de jogadoras por time.
Os dados são salvos em `times.json` e também associados ao evento correspondente.

**Exemplo de estrutura gerada em `times.json`:**
```json
[
  {
    "evento_id": 1,
    "times": [
      {
        "nome_time": "Time 1",
        "jogadoras": ["ana@exemplo.com", "bia@exemplo.com", "clara@exemplo.com", "deborah@exemplo.com", "elaine@exemplo.com"]
      },
      {
        "nome_time": "Time 2",
        "jogadoras": ["fernanda@exemplo.com", "giovana@exemplo.com", "helena@exemplo.com", "isabela@exemplo.com", "julia@exemplo.com"]
      }
    ]
  }
]
```
**Ações disponíveis:**
- Formar times – disponível no menu do administrador.
- Listar times – mostra os times de um evento específico.
---

### 6. Menus e Fluxo de Navegação

#### Menu da Jogadora
1. Listar eventos  
2. Inscrever-se em evento  
3. Ver ranking  
0. Logout  

#### Menu do Administrador
1. Cadastrar usuário  
2. Cadastrar evento  
3. Listar eventos  
4. Gerar ranking  
5. Formar times
0. Logout  

#### Menu Principal
1. Cadastrar usuário  
2. Login  
0. Sair  

---

## 7. Integração com o Site (Node.js + React)
O script Python se comunica com o backend via **API REST local**, permitindo que o ranking atualizado seja exibido na interface web.  
A integração ocorre automaticamente na geração do ranking, por meio de uma requisição `POST`:

```python
requests.post("http://localhost:5000/api/ranking", json=ranking)
```

---

## Estrutura de Arquivos
```
passa_a_bola/
├── main.py            # Código principal do sistema
├── usuarios.json            # Cadastro de jogadoras
├── eventos.json             # Eventos esportivos
├── times.json               # Times formados automaticamente em eventos
├── ranking.json             # Ranking local de jogadoras
├── contaAdm.txt
├── membros.txt
├── README.md
├── Sprint 3.pdf
```

---

## Execução
Execute o programa diretamente com:
```bash
python main.py
```

O sistema abrirá o menu principal, permitindo cadastro, login e navegação pelos recursos de jogadora ou admin.

---

## Conclusão
Esta Solução criada para a empresa **Passa a Bola** oferece um sistema funcional de gestão esportiva, com persistência local, autenticação simples e integração direta com uma aplicação web moderna.  
A funcionalidade do **ranking automático de jogadoras** representa um passo importante para o monitoramento de engajamento e gamificação da plataforma.

## Equipe SmoothPath
- Gabriel dos Santos Cardoso 
- Geovana Maria da Silva Cardoso
- Gustavo Torres Caldeira
- Lucas Oliveira Santos 
- Mariana Silva do Egito Moreira
- 1ESPF - Engenharia de Software (FIAP)