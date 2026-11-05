## O que é necessário para rodar a aplicação exemplo:

### Inicializando o ambiente

Instale o Python (www.python.org)<br/>
Instale o utilitário uv (https://docs.astral.sh/uv/)<br/>
Dentro da raiz deste repositório inicialize o ambiente virtual:<br/>
```
# Inicializa o ambiente virtual do python
uv venv init

# Instala os componentes/pacotes necessários 
uv sync
``` 
   
2. Rodando o projeto

```
# Ative o ambiente virtual previamente criado
# No windows o comando é este:
.venv\scripts\activate

# No linux o comando é este:
source .venv/bin/activate
# ou
. .venv/bin/activate

# Execute o servidor
uvicorn init:app --reload 

# O reload é interessante, pois, ele fica monitorando os fontes e se
# houver alguma alteração, ele reinicializa tudo. 
```

3. Testando a API

Para consultar os endpoints definidos:
http://localhost:8000/schema/elements
ou
http://localhost:8000/schema/swagger

Para autenticar, use o payload:
```json
{
  "username": "teste",
  "password": "123123"
}
```

Endpoints protegidos (que necessitam de autenticação prévia) são acessados passando-se
o header `X-Usuario` com o vlaor retornado na autenticação (/auth/login)
