import pytest
from src.vocab_game import VocabGame

class TestUC03ReceberFeedback:
    def test_feedback_todas_letras_corretas(self):
        """CT-UC03-01: Todas as letras na posição correta → tudo 'correto'"""
        jogo = VocabGame()
        jogo.palavra_secreta = "CASAL"
        
        feedback = jogo.analisar_palpite("CASAL")
        expected = [
            {'letra': 'C', 'status': 'correto'},
            {'letra': 'A', 'status': 'correto'},
            {'letra': 'S', 'status': 'correto'},
            {'letra': 'A', 'status': 'correto'},
            {'letra': 'L', 'status': 'correto'}
        ]
        assert feedback == expected  # ✅ VAI FALHAR! Método não existe ainda
    
    def test_feedback_todas_letras_inexistentes(self):
        """CT-UC03-02: Todas as letras inexistentes → tudo 'inexistente'"""
        jogo = VocabGame()
        jogo.palavra_secreta = "CASAL"
        
        feedback = jogo.analisar_palpite("PORTO")
        expected = [
            {'letra': 'P', 'status': 'inexistente'},
            {'letra': 'O', 'status': 'inexistente'},
            {'letra': 'R', 'status': 'inexistente'},
            {'letra': 'T', 'status': 'inexistente'},
            {'letra': 'O', 'status': 'inexistente'}
        ]
        assert feedback == expected  # ✅ VAI FALHAR!