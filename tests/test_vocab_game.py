import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vocab_game import VocabGame


class TestVocabGame:    
    def test_iniciar_jogo(self):
        """Teste 1: O jogo deve ser criado com sucesso"""
        jogo = VocabGame()
        assert jogo is not None
    
    def test_sortear_palavra(self):
        """Teste 2: O jogo deve sortear uma palavra secreta de 5 letras"""
        jogo = VocabGame()
        jogo.iniciar_jogo()
        
        assert jogo.palavra_secreta is not None
        assert len(jogo.palavra_secreta) == 5
        assert jogo.palavra_secreta.isalpha()
        assert jogo.palavra_secreta.isupper()
    
    def test_iniciar_tentativas_restantes(self):
        """Teste 3: O jogo deve iniciar com 6 tentativas"""
        jogo = VocabGame()
        jogo.iniciar_jogo()
        
        assert jogo.tentativas_restantes == 6
    
    def test_iniciar_tabuleiro_vazio(self):
        """Teste 4: O jogo deve inicializar com tabuleiro vazio"""
        jogo = VocabGame()
        jogo.iniciar_jogo()
        
        assert jogo.tabuleiro is not None
        assert len(jogo.tabuleiro) == 0
    
    def test_iniciar_status_em_andamento(self):
        """Teste 5: O jogo deve iniciar com status 'em_andamento'"""
        jogo = VocabGame()
        jogo.iniciar_jogo()
        
        assert jogo.status == 'em_andamento'
    
    def test_obter_estado_jogo(self):
        """Teste 6: O método obter_estado_jogo deve retornar todas as informações necessárias"""
        jogo = VocabGame()
        jogo.iniciar_jogo()
        
        estado = jogo.obter_estado_jogo()
        
        assert 'tentativas_restantes' in estado
        assert 'tabuleiro' in estado
        assert 'status' in estado
        assert estado['tentativas_restantes'] == 6
        assert estado['tabuleiro'] == []
        assert estado['status'] == 'em_andamento'
        assert 'palavra_secreta' not in estado
