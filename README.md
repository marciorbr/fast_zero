# Fast Zero

Este é o projeto desenvolvido durante o curso [FastAPI do Zero](https://fastapidozero.dunossauro.com/), ministrado pelo Eduardo Mendes (Dunossauro). O objetivo do projeto é construir uma API robusta, testada e pronta para produção, utilizando as melhores práticas do ecossistema Python.

## 🚀 Tecnologias Utilizadas

- **[FastAPI](https://fastapi.tiangolo.com/):** Framework web moderno e de alta performance.
- **[Poetry](https://python-poetry.org/):** Gerenciamento de dependências e ambientes virtuais.
- **[SQLAlchemy](https://www.sqlalchemy.org/):** ORM para interação com o banco de dados (Async).
- **[Alembic](https://alembic.sqlalchemy.org/):** Ferramenta de migrações para o banco de dados.
- **[Pydantic](https://docs.pydantic.dev/):** Validação de dados e configurações usando tipos Python.
- **[Pytest](https://docs.pytest.org/):** Framework de testes automatizados.
- **[Ruff](https://beta.ruff.rs/docs/):** Linter e formatador de código extremamente rápido.
- **[Docker](https://www.docker.com/):** Containerização da aplicação e do banco de dados (PostgreSQL).
- **[Taskipy](https://github.com/taskipy/taskipy):** Executor de tarefas para simplificar comandos comuns.

## 🛠️ Configuração do Ambiente

### Pré-requisitos
- Python 3.13+
- Poetry
- Docker (opcional, para rodar via container)

### Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd fast_zero
```

2. Instale as dependências:
```bash
poetry install
```

3. Ative o ambiente virtual:
```bash
poetry shell
```

## 🗄️ Banco de Dados e Migrações

O projeto utiliza o **Alembic** para gerenciar o esquema do banco de dados.

- Gerar uma nova migration (após alterar `models.py`):
```bash
alembic revision --autogenerate -m "descrição da mudança"
```

- Aplicar as migrations:
```bash
alembic upgrade head
```

- Reverter a última migration:
```bash
alembic downgrade -1
```

## 🏃 Executando a Aplicação

Para iniciar o servidor de desenvolvimento:

```bash
task run
```
A API estará disponível em `http://127.0.0.1:8000` e a documentação interativa em `/docs`.

## 🧪 Testes e Qualidade

O projeto preza pela alta cobertura de testes e qualidade de código.

- **Executar testes:**
```bash
task test
```

- **Linting (Ruff):**
```bash
task lint
```

- **Formatação de código:**
```bash
task format
```

## 🐳 Docker

Para rodar a aplicação completa (API + Banco de Dados PostgreSQL) via Docker Compose:

```bash
docker compose up -d
```

## 🏗️ Estrutura do Projeto

```text
fast_zero/
├── fast_zero/        # Código fonte da aplicação
│   ├── routers/      # Definição das rotas (users, auth, todos)
│   ├── models.py     # Modelos do SQLAlchemy
│   ├── schemas.py    # Esquemas do Pydantic
│   ├── security.py   # Lógica de autenticação e JWT
│   └── app.py        # Ponto de entrada da aplicação
├── migrations/       # Arquivos de migração do Alembic
├── tests/           # Testes automatizados
├── pyproject.toml    # Configurações do Poetry e ferramentas
└── docker-compose.yml
```

## 📝 Aprendizados Principais

- Desenvolvimento de APIs assíncronas com FastAPI.
- Implementação de CRUD completo com autenticação JWT.
- Testes de integração e unitários com alta cobertura.
- Containerização e CI/CD com GitHub Actions.
- Separação de responsabilidades (SOC) e organização modular de rotas.

---
Projeto desenvolvido seguindo os ensinamentos da comunidade [Live de Python](https://www.youtube.com/@Dunossauro).
