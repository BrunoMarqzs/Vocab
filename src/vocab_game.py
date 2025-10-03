class VocabGame:
    def __init__(self):
        self.palavra_secreta = ""
    
    def iniciar_jogo(self):
        self.palavra_secreta = "CASAL"  # Para teste
    
    def analisar_palpite(self, palpite):
        """
        UC-03: Implementação ERRADA de propósito para TDD
        """
        # ❌ SEMPRE RETORNA 'inexistente' (ERRADO)
        feedback = []
        for letra in palpite:
            feedback.append({'letra': letra, 'status': 'inexistente'})
        return feedback