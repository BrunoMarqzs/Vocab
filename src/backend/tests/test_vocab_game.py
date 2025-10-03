import pytest
from backend.app.vocab_game import VocabGame

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
        assert 'palavra_secreta' in estado
        
        assert estado['tentativas_restantes'] == 6
        assert estado['tabuleiro'] == []
        assert estado['status'] == 'em_andamento'
        assert len(estado['palavra_secreta']) == 5
    
    def test_nao_pode_iniciar_nova_partida_sem_finalizar(self):
        """Teste para o UC-6"""
        jogo = VocabGame()
        jogo.iniciar_jogo()
        
        # Tentar iniciar uma nova partida sem finalizar a atual
        resultado = jogo.iniciar_jogo()
        
        # O jogo não deve permitir iniciar nova partida
        assert resultado == False
        
    def test_iniciar_nova_partida_reseta_estado(self, monkeypatch):
        """Teste para o UC-7"""
        jogo = VocabGame()
        
        # Força palavras previsíveis para testarmos troca entre partidas
        monkeypatch.setattr(VocabGame, "_sortear_palavra_5_letras", lambda self: "VIDAS")
        
        # Primeira partida
        jogo.iniciar_jogo()
        primeira_palavra = jogo.palavra_secreta
        
        # Simular algumas jogadas
        jogo.fazer_tentativa("TESTE")
        jogo.fazer_tentativa("JOGOS")
        
        # Finalizar a partida atual (forçar derrota)
        jogo.tentativas_restantes = 0
        jogo.status = 'derrota'
        
        # Trocar para nova palavra para segunda partida
        monkeypatch.setattr(VocabGame, "_sortear_palavra_5_letras", lambda self: "JOGAR")
        
        # Iniciar nova partida
        resultado = jogo.iniciar_jogo()
        
        # Verificar se nova partida foi iniciada com sucesso
        assert resultado == True
        assert jogo.palavra_secreta == "JOGAR"
        assert jogo.palavra_secreta != primeira_palavra
        assert jogo.tentativas_restantes == 6
        assert jogo.tabuleiro == []
        assert jogo.status == 'em_andamento'