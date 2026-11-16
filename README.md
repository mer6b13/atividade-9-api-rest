# Atividade 9 — API REST de Tarefas

## Sobre o projeto

Este projeto consiste no desenvolvimento de uma API REST para gerenciamento de tarefas, utilizando Python, Flask e SQLite.

A API permite cadastrar, consultar, atualizar e excluir tarefas, utilizando requisições HTTP e dados no formato JSON.

## Tecnologias utilizadas

- Python
- Flask
- SQLite
- JSON
- Git e GitHub

## Funcionalidades

- Listar todas as tarefas.
- Buscar uma tarefa pelo ID.
- Cadastrar novas tarefas.
- Atualizar tarefas existentes.
- Excluir tarefas.
- Validar os dados recebidos pela API.
- Armazenar os dados em banco SQLite.

## Estrutura do projeto

```text
atividade-9-api-rest/
│
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
└── tarefas.db
```

O banco de dados `tarefas.db` é criado automaticamente quando a aplicação é iniciada.

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/mer6b13/atividade-9-api-rest.git
```

### 2. Entrar na pasta

```bash
cd atividade-9-api-rest
```

### 3. Criar o ambiente virtual

```bash
python3 -m venv .venv
```

### 4. Ativar o ambiente virtual

No Linux:

```bash
source .venv/bin/activate
```

### 5. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 6. Executar a aplicação

```bash
python3 app.py
```

A API estará disponível em:

http://127.0.0.1:5000

## Endpoints disponíveis

| Método HTTP | Rota | Funcionalidade |
|---|---|---|
| GET | /tarefas | Listar todas as tarefas |
| GET | /tarefas/<id> | Buscar tarefa pelo ID |
| POST | /tarefas | Cadastrar tarefa |
| PUT | /tarefas/<id> | Atualizar tarefa |
| DELETE | /tarefas/<id> | Excluir tarefa |

## Exemplo de cadastro

Para cadastrar uma tarefa, utilize uma requisição POST:

```json
{
    "titulo": "Estudar Python",
    "descricao": "Praticar API REST",
    "concluida": false
}
```

## Validações

A API verifica:

- Se o título foi informado.
- Se o título contém texto válido.
- Se a descrição é um texto.
- Se o campo concluida recebe verdadeiro ou falso.
- Se a tarefa existe antes de atualizar ou excluir.

## Códigos HTTP utilizados

- **200:** Requisição realizada com sucesso.
- **201:** Tarefa cadastrada com sucesso.
- **400:** Dados inválidos.
- **404:** Tarefa não encontrada.

## Banco de dados

O projeto utiliza SQLite para armazenar as tarefas de maneira persistente.

A tabela `tarefas` possui os seguintes campos:

- `id`: identificador da tarefa.
- `titulo`: título da tarefa.
- `descricao`: descrição da tarefa.
- `concluida`: indica se a tarefa foi concluída.

## Autor

JOÃO iT4LO 