# Vocab

## Descrição

O **Vocab** é um jogo de adivinhação de palavras secretas inspirado no Wordle. O objetivo é descobrir uma palavra de 5 letras em até cinco tentativas.

## Pré-requisitos

### Instalação Local
- Python 3.7+ 
- Node.js 18+
- npm 8+

### Docker
- Docker
- Docker Compose

## Instalação de Dependências

```bash
# Backend
pip install fastapi uvicorn requests

# Frontend
cd src/frontend
npm install
```

## Como Executar

### Opção 1: Execução Local (Recomendado)

```bash
# 1. Backend (Terminal 1)
cd src/backend/app
uvicorn api:app --reload --host 127.0.0.1 --port 8000

# 2. Frontend (Terminal 2) 
cd src/frontend
npm run dev
```

### Opção 2: Usando Docker

```bash
# Aplicação completa
docker-compose up backend frontend-dev

# Apenas testes
docker-compose run --rm vocab-tests
```

## Acessar a Aplicação

- **Jogo**: http://localhost:3000
- **API**: http://localhost:8000/docs

## Executar Testes

```bash
# Navegar para a raiz do projeto
cd Vocab

# Executar todos os testes
PYTHONPATH=src python -m pytest src/backend/tests -v

# Executar teste específico
PYTHONPATH=src python -m pytest src/backend/tests/test_uc_01.py -v
```

## Desenvolvimento e Testes

### Casos de Uso com TDD
- ✅ UC-01: Iniciar Jogo (`test_uc_01.py`)  
- ✅ UC-02: Inserir Tentativa (`test_uc_02.py`)
- ✅ UC-03: Finalizar Partida (`test_uc_03_finalizar.py`)
- ✅ UC-04: Iniciar Nova Partida (`test_uc_04.py`)
- ✅ UC-05: Compartilhar Resultado (`test_uc_05.py`)
- ✅ UC-06: Consultar Estatísticas (`test_uc_06.py`)

### Tecnologias
- **Backend**: Python + FastAPI + Uvicorn
- **Frontend**: React + Vite + Tailwind CSS
- **Testes**: Pytest com metodologia TDD
- **API Externa**: [Dicionário Aberto](https://dicionario-aberto.net/)

## Troubleshooting

### Problemas Comuns

**Frontend mostra tela branca ou erros de conexão:**
1. Certifique-se que o backend está rodando primeiro
2. Use `127.0.0.1:8000` em vez de `localhost:8000` se houver problemas IPv6
3. Verifique se as portas 8000 (backend) e 3000 (frontend) estão livres

**Dependências não encontradas:**
```bash
# Se faltar uvicorn/fastapi
pip install fastapi uvicorn requests

# Se faltar dependências do Node.js  
cd src/frontend && npm install
```