import requests
import random
import time
import unicodedata


class VocabGame:    
    def __init__(self):
        self.palavra_secreta = None
        self.tentativas_restantes = None
        self.tabuleiro = None
        self.status = None
    
    def iniciar_jogo(self):
        # Não permite iniciar nova partida se a atual não foi finalizada
        if self.status == 'em_andamento':
            return False
            
        self.palavra_secreta = self._sortear_palavra_5_letras()
        self.tentativas_restantes = 5
        self.tabuleiro = []
        self.status = 'em_andamento'
        return True
    
    def forcar_novo_jogo(self):
        """
        Força o início de um novo jogo, independente do status atual.
        Usado para 'Nova Partida' e 'Reiniciar'.
        """
        self.palavra_secreta = self._sortear_palavra_5_letras()
        self.tentativas_restantes = 5
        self.tabuleiro = []
        self.status = 'em_andamento'
        return True

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
        return True

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
        palavras_fallback = ["MUNDO", "TEMPO", "JOGO", "LUGAR"]
        return random.choice(palavras_fallback)
    
    def validar_palavra(self, palavra):
        """ Método para validação simples de palavra - retorna True/False """
        # 1. Validar se tem 5 letras
        if len(palavra) != 5:
            return False
        
        # 2. Validar se são apenas letras
        if not palavra.isalpha():
            return False
        
        return True

    def remover_acentos(self, s):
        return ''.join(c for c in unicodedata.normalize('NFD', s)
                       if unicodedata.category(c) != 'Mn')

    def inserir_tentativa(self, palavra):
        """ UC-02 - Inserir tentativa completa no jogo """
        # 0. Verificar se o jogo foi iniciado
        if self.palavra_secreta is None or self.status != 'em_andamento':
            return {'acertou': False, 'erro': 'Jogo não foi iniciado ou já foi finalizado'}
        
        # 1. Usar validação simples primeiro
        if not self.validar_palavra(palavra):
            if len(palavra) != 5:
                return {'acertou': False, 'erro': 'Palavra deve ter 5 letras'}
            else:
                return {'acertou': False, 'erro': 'Palavra deve conter apenas letras'}
        
        # 2. Verificar se acertou a palavra (normalizando acentos)
        palavra = palavra.upper()
        palavra_normalizada = self.remover_acentos(palavra)
        secreta_normalizada = self.remover_acentos(self.palavra_secreta)
        acertou = palavra_normalizada == secreta_normalizada
        
        # 3. Processar tentativa
        feedback = self.analisar_palpite(palavra)
        self.tabuleiro.append({
            'palavra': palavra,
            'feedback': feedback
        })
        
        # 4. Reduzir tentativas restantes
        if not acertou:
            self.tentativas_restantes -= 1
        
        # 5. Verificar se o jogo terminou
        if acertou:
            self.status = 'venceu'
        elif self.tentativas_restantes <= 0:
            self.status = 'perdeu'
        
        return {'acertou': acertou, 'feedback': feedback}
    
    def obter_estado_jogo(self, incluir_palavra_secreta=False):
        # Retorna o estado atual do jogo visível ao jogador
        estado = {
            'tentativas_restantes': self.tentativas_restantes,
            'tabuleiro': self.tabuleiro.copy(),
            'status': self.status
        }
        
        # Incluir palavra secreta apenas quando solicitado (para testes ou quando o jogo terminou)
        if incluir_palavra_secreta or self.status in ['venceu', 'perdeu']:
            estado['palavra_secreta'] = self.palavra_secreta
            
        return estado
    
    def analisar_palpite(self, palpite):
        # UC-03: Receber Feedback da Tentativa
        palpite = palpite.upper()
        resultado = []
        palavra_secreta_normalizada = self.remover_acentos(self.palavra_secreta)
        palpite_normalizado = self.remover_acentos(palpite)
        for i in range(5):
            letra_palpite = palpite[i]
            letra_palpite_norm = palpite_normalizado[i]
            letra_secreta = self.palavra_secreta[i]
            letra_secreta_norm = palavra_secreta_normalizada[i]
            if letra_palpite_norm == letra_secreta_norm:
                resultado.append({'letra': letra_palpite, 'status': 'correto'})
            elif letra_palpite_norm in palavra_secreta_normalizada:
                resultado.append({'letra': letra_palpite, 'status': 'posicao_errada'})
            else:
                resultado.append({'letra': letra_palpite, 'status': 'inexistente'})
        return resultado
    
    def processar_palpite(self, palpite):
        """
        Processa um palpite completo: analisa, atualiza estado, verifica fim de jogo.
        Retorna o formato esperado pela API.
        """
        if self.status != 'em_andamento':
            raise ValueError("O jogo não está em andamento")
        
        # Analisa o palpite
        feedback = self.analisar_palpite(palpite)
        
        # Atualiza tentativas
        self.tentativas_restantes -= 1
        
        # Adiciona ao tabuleiro
        self.tabuleiro.append(feedback)
        
        # Verifica condições de fim de jogo
        palpite_upper = palpite.upper()
        if palpite_upper == self.palavra_secreta:
            self.status = 'venceu'
        elif self.tentativas_restantes <= 0:
            self.status = 'perdeu'
        
        # Prepara resposta
        resposta = {
            "feedback": feedback,
            "tentativas_restantes": self.tentativas_restantes,
            "status": self.status
        }
        
        # Inclui palavra secreta e pontuação quando o jogo termina (perdeu ou venceu)
        if self.status in ['venceu', 'perdeu']:
            resposta["palavra_secreta"] = self.palavra_secreta
            resposta["pontuacao"] = self.calcular_pontuacao()
        
        return resposta
    
    def calcular_pontuacao(self):
        # Calcula a pontuação baseada no número de letras corretas na posição certa da última tentativa.
        if not self.tabuleiro:
            return 0
        
        # Pega a última tentativa (feedback)
        ultima_tentativa = self.tabuleiro[-1]
        
        # Conta quantas letras estão na posição correta
        letras_corretas = 0
        for item in ultima_tentativa:
            if item['status'] == 'correto':
                letras_corretas += 1
        
        # 20 pontos por letra correta
        pontuacao = letras_corretas * 20
        return pontuacao


    def finalizar_jogo(self, palpite):

        if self.tentativas_restantes <= 0:
            self.status = 'perdeu'

        elif self.palavra_secreta == palpite:
            self.status = 'venceu'

        print("VOCÊ ACERTOU A PALAVRA!" if self.status == 'venceu' else "VOCÊ ERROU A PALAVRA!")
        # mostra a palara secreta se errou
        print(f"A palavra correta era: {self.palavra_secreta}" if self.status == 'perdeu' else "")
        print(self.obter_estado_jogo())
