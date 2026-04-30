

https://fastapidozero.dunossauro.com/estavel/

### Instalar versão especifica do python e criar o projeto.

* Para utilizarmos uma versão específica do Python em nosso ambiente, devemos solicitar ao Poetry que instale essa versão:
```bash
poetry python install 3.13
```
* Criando um projeto

Agora que temos o poetry e a versão do python que usaremos disponível, podemos iniciar a criação do nosso projeto. O primeiro passo é criar um novo projeto utilizando o Poetry, com o comando poetry new. Em seguida, navegaremos até o diretório criado:
```bash
poetry new --flat fast_zero 
cd fast_zero
```

Ele criará uma estrutura de arquivos e pastas

Com a estrutura inicial do projeto criada e estando no diretório do projeto, podemos informar ao Poetry que queremos usar a versão do Python que instalamos. Para isso, utilizamos o seguinte comando:
```bash
poetry env use 3.13
```

Em conjunto com essa instrução, devemos também especificar no Poetry que usaremos exatamente a versão 3.13 em nosso projeto. Para isso, alteramos o arquivo de configuração pyproject.toml na raiz do projeto:

```toml
pyproject.toml
[project]
# ...
requires-python = ">=3.13,<4.0" 
```

Antes de iniciarmos nossa aplicação, temos que fazer um passo importante, habilitar o ambiente virtual, para que o python consiga enxergar nossas dependências instaladas. O poetry tem um comando específico para isso:
```bash
poetry shell
```

## Utilizando o ruff

poetry run ruff check .

## Criar gitignore

pipx run ignr -p python > .gitignore

## Alembic

* Gerar uma migration
```bash
alembic revision --autogenerate -m "create users table"
```

* Executar a migration para última versão
```bash
alembic upgrade head
```

# Reverter a migrate

```bash
alembic downgrade -1
```

# pytest

```bash
task test --collect-only
task test -k test_create_user
task test tests/test_db.py
```


## Conceitos
* SOC - separed of concernes

## Lives
* Live de sqlalchemy

* Serie Opentelemetry

* Live migrations


## site 4devs gerar cpf, cnpj, etc..