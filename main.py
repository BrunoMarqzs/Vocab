#!/usr/bin/env python3
from vocab_game import VocabGame


def main():
    # Criar uma nova instância do jogo
    jogo = VocabGame()
    
    # Iniciar uma partida
    jogo.iniciar_jogo()
    
    # Obter o estado atual do jogo
    estado = jogo.obter_estado_jogo()
    
    print(f"Tentativas restantes: {estado['tentativas_restantes']}")
    print(f"Tabuleiro: {estado['tabuleiro']}")
    print(f"Status: {estado['status']}")
    print(f"Jogo iniciado com sucesso!")



if __name__ == "__main__":
    main()
