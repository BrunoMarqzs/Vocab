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
        self.tentativas_restantes = 5
        self.tabuleiro = []
        self.status = 'em_andamento'

    def iniciar_nova_partida(self):
        """
        UC-04: só pode iniciar nova partida se a anterior foi finalizada.
        Reinicia tentativas, tabuleiro e sorteia nova palavra.
        """
        if self.status != 'finalizado':
            raise ValueError("Nova partida só pode ser iniciada após finalizar a partida anterior.")
        # reinicia como um novo jogo
        self.palavra_secreta = self._sortear_palavra_5_letras()
        self.tentativas_restantes = 6
        self.tabuleiro = []
        self.status = 'em_andamento'

    def finalizar_partida(self, resultado: str):
        """
        Marca a partida como finalizada.
        `resultado` pode ser 'vitoria', 'derrota' etc. (por ora não usamos).
        """
        self.status = 'finalizado'
    
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
    
    def inserir_tentativa(self, palavra):
        """ UC-02 """
        # 1. Validar se tem 5 letras
        if len(palavra) != 5:
            return False
        
        # 2. Validar se são apenas letras
        if not palavra.isalpha():
            return False
        
        return True
    
    def obter_estado_jogo(self):
        # Retorna o estado atual do jogo visível ao jogador sem incluir a palavra secreta.
        return {
            'tentativas_restantes': self.tentativas_restantes,
            'tabuleiro': self.tabuleiro.copy(),
            'status': self.status
        }
    
    def analisar_palpite(self, palpite):
        # UC-03: Receber Feedback da Tentativa
        palpite = palpite.upper()
        resultado = []
    
        for i in range(5):
            letra = palpite[i]
            if letra == self.palavra_secreta[i]:
                resultado.append({'letra': letra, 'status': 'correto'})
            elif letra in self.palavra_secreta:
                resultado.append({'letra': letra, 'status': 'posicao_errada'})
            else:
                resultado.append({'letra': letra, 'status': 'inexistente'})
        
        return resultado


    def finalizar_jogo(self, palpite):

        if self.tentativas_restantes <= 0:
            self.status = 'perdeu'

        elif self.palavra_secreta == palpite:
            self.status = 'venceu'

        print("VOCÊ ACERTOU A PALAVRA!" if self.status == 'venceu' else "VOCÊ ERROU A PALAVRA!")
        # mostra a palara secreta se errou
        print(f"A palavra correta era: {self.palavra_secreta}" if self.status == 'perdeu' else "")
        print(self.obter_estado_jogo())
