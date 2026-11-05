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

Abra o navegador na página:
http://localhost:8000/schema/elements
ou
http://localhost:8000/schema/swagger