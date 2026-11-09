# Exemplo de uso do Litestar

Projeto de exemplo de uma API REST com [Litestar](https://litestar.dev/): cadastro de
usuários e produtos, login, guards, middlewares e injeção de dependências, com
persistência em SQLite via [SQLModel](https://sqlmodel.tiangolo.com/).

> [!WARNING]
> Este projeto é apenas didático. As senhas ficam em texto puro e são devolvidas pela API,
> e a "autenticação" consiste em informar um id de usuário no header `X-Usuario`, sem
> nenhuma validação. Não use esse modelo em produção.

## Requisitos

- [uv](https://docs.astral.sh/uv/), que gerencia o Python, o ambiente virtual e os pacotes
- Python 3.15 ou superior
- cURL, para testar as chamadas

Para instalar o uv:

```bash
# Linux e macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Se o Python 3.15 ainda não estiver disponível na máquina, o uv o baixa automaticamente no
passo seguinte. Para instalá-lo antes, use `uv python install 3.15`.

## Como inicializar

Execute os comandos na raiz do repositório:

```bash
# Cria o ambiente virtual (.venv) e instala as dependências
uv sync

# Inicia o servidor em http://localhost:8000
uv run uvicorn init:app --app-dir src --reload
```

Com `--reload`, o servidor reinicia sempre que um arquivo do projeto é alterado.

Na primeira execução é criado o arquivo `database.db`, no diretório onde o servidor foi
iniciado, já com alguns registros:

| Tipo    | Id | Dados                                 |
| ------- | -- | ------------------------------------- |
| Usuário | 1  | usuário `teste`, senha `123123`       |
| Usuário | 2  | usuário `🔒`, senha `🔑`              |
| Produto | 1  | `Produto X`, preço 12.34              |
| Produto | 2  | `Produto π`, preço 3.14               |

Para voltar a esse estado inicial, pare o servidor, apague o `database.db` e inicie o
servidor novamente.

## Documentação interativa

Com o servidor em execução, os endpoints podem ser consultados em:

- <http://localhost:8000/schema/swagger>
- <http://localhost:8000/schema/elements>
- <http://localhost:8000/schema/redoc>

## Exemplos de chamadas com cURL

### Autenticação

```bash
curl -X POST http://localhost:8000/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"username": "teste", "password": "123123"}'
```

```json
{"nome":"Senhor Teste da Silva","id":1,"senha":"123123","usuario":"teste"}
```

Credenciais inválidas retornam `401 Unauthorized`.

As rotas em `/cad/*` são protegidas: envie o `id` retornado pelo login no header
`X-Usuario`. Sem ele, a resposta é `401 Unauthorized`:

```json
{"status_code":401,"detail":"Usuário não autenticado"}
```

### Informações da sessão

Rota pública, que mostra o id da sessão de banco e o usuário da requisição. Sem o header
`X-Usuario`, `usuario_id` vem como `0`.

```bash
curl http://localhost:8000/info -H 'X-Usuario: 1'
```

```json
{"db":139747248263104,"usuario_id":1}
```

### Produtos

Listar todos:

```bash
curl http://localhost:8000/cad/produto/all -H 'X-Usuario: 1'
```

```json
[{"id":1,"descricao":"Produto X","preco":12.34},{"id":2,"descricao":"Produto π","preco":3.14}]
```

Consultar por id (retorna `204 No Content` se não existir):

```bash
curl http://localhost:8000/cad/produto/1 -H 'X-Usuario: 1'
```

```json
{"id":1,"descricao":"Produto X","preco":12.34}
```

Incluir (retorna `201 Created`):

```bash
curl -X POST http://localhost:8000/cad/produto \
  -H 'X-Usuario: 1' \
  -H 'Content-Type: application/json' \
  -d '{"descricao": "Produto Z", "preco": 99.9}'
```

```json
{"id":3}
```

Alterar (retorna `202 Accepted`, ou `204 No Content` se não existir):

```bash
curl -X PUT http://localhost:8000/cad/produto/3 \
  -H 'X-Usuario: 1' \
  -H 'Content-Type: application/json' \
  -d '{"descricao": "Produto Z alterado", "preco": 89.9}'
```

```json
true
```

### Usuários

Listar todos:

```bash
curl http://localhost:8000/cad/usuario/all -H 'X-Usuario: 1'
```

```json
[{"nome":"Senhor Teste da Silva","id":1,"senha":"123123","usuario":"teste"},{"nome":"Pirata ☠","id":2,"senha":"🔑","usuario":"🔒"}]
```

Consultar por id (retorna `204 No Content` se não existir):

```bash
curl http://localhost:8000/cad/usuario/1 -H 'X-Usuario: 1'
```

```json
{"nome":"Senhor Teste da Silva","id":1,"senha":"123123","usuario":"teste"}
```

Incluir (retorna `201 Created`):

```bash
curl -X POST http://localhost:8000/cad/usuario \
  -H 'X-Usuario: 1' \
  -H 'Content-Type: application/json' \
  -d '{"nome": "Fulano de Tal", "usuario": "fulano", "senha": "abc123"}'
```

```json
{"id":3}
```

Alterar (retorna `202 Accepted`, ou `204 No Content` se não existir):

```bash
curl -X PUT http://localhost:8000/cad/usuario/3 \
  -H 'X-Usuario: 1' \
  -H 'Content-Type: application/json' \
  -d '{"nome": "Fulano Alterado", "usuario": "fulano", "senha": "nova"}'
```

```json
true
```
