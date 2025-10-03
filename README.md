# Vocab

## Descrição

O **Vocab** é um jogo de adivinhação de palavras secretas inspirado no Wordle. O objetivo é descobrir uma palavra de 5 letras em até cinco tentativas.

## Como Executar

### Opção 1: Usando Docker (Recomendado)

#### Pré-requisitos
- Docker
- Docker Compose

#### Comandos Docker

```bash
# Construir as imagens primeiro
docker-compose build

# Executar o jogo
docker-compose run --rm vocab-game

# Executar os testes
docker-compose run --rm vocab-tests
```

### Opção 2: Instalação Local

#### Pré-requisitos
1. Python 3.7 ou superior
2. Instalar as dependências:

```bash
pip install -r requirements.txt
python main.py
```

## Desenvolvimento

Este projeto segue a metodologia **TDD (Test-Driven Development)**:

1. Escrever os testes primeiro
2. Implementar o código mínimo para passar nos testes
3. Refatorar mantendo os testes passando

## Casos de Uso Implementados

- [x] **UC-01**: Iniciar Jogo - Sorteia palavra secreta e configura estado inicial

## API Utilizada

O jogo utiliza a [API do Dicionário Aberto](https://dicionario-aberto.net/) para obter palavras aleatórias em português.