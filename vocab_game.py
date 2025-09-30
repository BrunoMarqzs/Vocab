import requests
import random
import time


class VocabGame:    
    def __init__(self):
        self.palavra_secreta = None
        self.tentativas_restantes = None
        self.tabuleiro = None
        self.status = None
    
    def iniciar_jogo(self):
        self.palavra_secreta = self._sortear_palavra_5_letras()
        self.tentativas_restantes = 6
        self.tabuleiro = []
        self.status = 'em_andamento'
    
    def _sortear_palavra_5_letras(self):
        # Sorteia uma palavra de 5 letras usando a API do dicionário aberto.
        # Retorna a palavra em maiúsculas.
        url = "https://api.dicionario-aberto.net/random"
        
        tentativas = 0
        while tentativas < 50:
            try:
                resposta = requests.get(url, timeout=5)
                
                if resposta.status_code == 200:
                    dados = resposta.json()
                    palavra = dados["word"].upper()
                    
                    if len(palavra) == 5 and palavra.isalpha():
                        return palavra
                
                tentativas += 1
                time.sleep(0.1)
                
            except (requests.RequestException, KeyError):
                tentativas += 1
                time.sleep(0.1)
        
        # Fallback: se não conseguir da API, usa uma palavra padrão
        palavras_fallback = ["MUNDO", "TEMPO", "PESSOA", "LUGAR"]
        return random.choice(palavras_fallback)
    
    def obter_estado_jogo(self):
        # Retorna o estado atual do jogo visível ao jogador sem incluir a palavra secreta.
        return {
            'tentativas_restantes': self.tentativas_restantes,
            'tabuleiro': self.tabuleiro.copy(),
            'status': self.status
        }


    def finalizar_jogo(self, palpite):

        if self.tentativas_restantes <= 0:
            self.status = 'perdeu'

        elif self.palavra_secreta == palpite:
            self.status = 'venceu'

        print("VOCÊ ACERTOU A PALAVRA!" if self.status == 'venceu' else "VOCÊ ERROU A PALAVRA!")
        # mostra a palara secreta se errou
        print(f"A palavra correta era: {self.palavra_secreta}" if self.status == 'perdeu' else "")
        print(self.obter_estado_jogo())
