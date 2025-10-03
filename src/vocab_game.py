class VocabGame:
    def __init__(self):
        self.palavra_secreta = ""
        self.tentativas_restantes = 6
        self.status = "nao_iniciado"
    
    def iniciar_jogo(self):
        self.palavra_secreta = "CASAL"  # Palavra fixa pra testar
        self.tentativas_restantes = 6
        self.status = "em_andamento"
    
    def analisar_palpite(self, palpite):
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