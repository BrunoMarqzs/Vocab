# Vocab

## Descrição

O **Vocab** é um jogo de adivinhação de palavras secretas inspirado no Wordle. O objetivo é descobrir uma palavra de 5 letras em até 6 tentativas.

### Regras do Jogo

1. Cada palavra enviada deve ter cinco letras e estar presente no dicionário do jogo
2. O jogador possui 6 tentativas para adivinhar a palavra da partida
3. Após cada tentativa:
   - **Verde**: Letra correta na posição correta
   - **Amarelo**: Letra existe na palavra mas está em posição diferente
   - **Sem destaque**: Letra não faz parte da palavra sorteada

### Pontuação

- **Vitória**: Acertar todas as letras nas posições corretas
- **Derrota**: Esgotar as 6 tentativas sem acertar
- **Pontuação parcial**: Na última tentativa, pontos equivalentes aos acertos

## Como Executar

### Pré-requisitos

1. Python 3.7 ou superior
2. Instalar as dependências:

```bash
pip install pytest requests
```

### Executar os Testes

Para executar todos os testes do projeto:

```bash
# Executar todos os testes
pytest

# Executar com saída detalhada
pytest -v

# Executar apenas testes específicos
pytest tests/test_vocab_game.py
```

### Executar o Jogo

Para testar o jogo em funcionamento:

```bash
python main.py
```

### Usar o Jogo (Programaticamente)

```python
from vocab_game import VocabGame

# Criar uma nova instância do jogo
jogo = VocabGame()

# Iniciar uma partida
jogo.iniciar_jogo()

# Obter o estado atual do jogo
estado = jogo.obter_estado_jogo()
print(f"Tentativas restantes: {estado['tentativas_restantes']}")
print(f"Status: {estado['status']}")
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