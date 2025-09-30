import requests
import random
import time

class VocabGame:
    def __init__(self):
        self.palavra_secreta = ""
        self.tentativas_restantes = 6
        self.status = "em_andamento"
    
    def _buscar_palavra_aleatoria(self):
        """UC-01: Já implementado"""
        url = "https://api.dicionario-aberto.net/random"
        tentativas = 0
        
        while tentativas < 10:
            try:
                resposta = requests.get(url, timeout=3)
                if resposta.status_code == 200:
                    dados = resposta.json()
                    palavra = dados["word"].upper()
                    
                    if len(palavra) == 5 and palavra.isalpha():
                        return palavra
                
                tentativas += 1
                time.sleep(0.05)
                
            except requests.exceptions.RequestException:
                tentativas += 1
                time.sleep(0.05)
        
        return random.choice(["CASAL", "TEMPO", "FESTA", "LIVRO", "VERDE"])
    
    def iniciar_jogo(self):
        
        self.palavra_secreta = self._buscar_palavra_aleatoria()
        self.tentativas_restantes = 6
        self.status = "em_andamento"
    
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
        
        return {
            'tentativas_restantes': self.tentativas_restantes,
            'status': self.status,
            'palavra_secreta': "*****"  
        }
