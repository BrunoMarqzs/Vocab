"""
Testes para o Caso de Uso 4 - Iniciar Nova Partida

Ator: Jogador
Descrição: O jogador solicita uma nova partida. O sistema sorteia uma nova palavra secreta 
de cinco letras, reinicia o número de tentativas e limpa o tabuleiro para o início do jogo.
Pré-condição: O jogador já finalizou uma partida anterior ou acessou o jogo pela primeira vez.
Pós-condição: Uma nova partida é iniciada, com a palavra secreta definida e as seis tentativas disponíveis.
"""

import pytest
from backend.app.vocab_game import VocabGame


class TestUC04IniciarNovaPartida:
    """Testes para o Caso de Uso 4 - Iniciar Nova Partida"""
    
    def test_iniciar_nova_partida_apos_finalizar(self):
        """CT-UC04-01: Deve permitir iniciar nova partida após finalizar a anterior"""
        jogo = VocabGame()
        jogo.iniciar_jogo()
        
        # Finalizar a partida atual
        jogo.finalizar_partida('vitoria')
        assert jogo.status == 'finalizado'
        
        # Iniciar nova partida
        jogo.iniciar_nova_partida()
        
        assert jogo.status == 'em_andamento'
        assert jogo.tentativas_restantes == 6
        assert jogo.tabuleiro == []
        assert jogo.palavra_secreta is not None
        assert len(jogo.palavra_secreta) == 5
    
    def test_nao_pode_iniciar_nova_partida_sem_finalizar(self):
        """CT-UC04-02: Não deve permitir iniciar nova partida sem finalizar a anterior"""
        jogo = VocabGame()
        jogo.iniciar_jogo()
        
        # Tentar iniciar nova partida sem finalizar a atual
        with pytest.raises(ValueError, match="Nova partida só pode ser iniciada após finalizar a partida anterior"):
            jogo.iniciar_nova_partida()
    
    def test_nova_partida_reseta_estado_completamente(self, monkeypatch):
        """CT-UC04-03: Nova partida deve resetar completamente o estado do jogo"""
        jogo = VocabGame()
        
        # Forçar palavra específica para primeira partida
        monkeypatch.setattr(VocabGame, "_sortear_palavra_5_letras", lambda self: "PRIMEIRA")
        jogo.iniciar_jogo()
        
        # Simular algumas jogadas
        jogo.tabuleiro = [['T', 'E', 'S', 'T', 'E'], ['J', 'O', 'G', 'O', 'S']]
        jogo.tentativas_restantes = 3
        primeira_palavra = jogo.palavra_secreta
        
        # Finalizar partida
        jogo.finalizar_partida('derrota')
        
        # Forçar palavra diferente para nova partida
        monkeypatch.setattr(VocabGame, "_sortear_palavra_5_letras", lambda self: "SEGUNDA")
        
        # Iniciar nova partida
        jogo.iniciar_nova_partida()
        
        # Verificar se estado foi completamente resetado
        assert jogo.palavra_secreta == "SEGUNDA"
        assert jogo.palavra_secreta != primeira_palavra
        assert jogo.tentativas_restantes == 6
        assert jogo.tabuleiro == []
        assert jogo.status == 'em_andamento'
    
    def test_nova_partida_sorteia_palavra_diferente(self):
        """CT-UC04-04: Nova partida deve sortear uma nova palavra (pode ser diferente da anterior)"""
        jogo = VocabGame()
        jogo.iniciar_jogo()
        primeira_palavra = jogo.palavra_secreta
        
        # Finalizar partida
        jogo.finalizar_partida('vitoria')
        
        # Iniciar nova partida
        jogo.iniciar_nova_partida()
        nova_palavra = jogo.palavra_secreta
        
        # Ambas devem ser palavras válidas de 5 letras
        assert len(primeira_palavra) == 5
        assert len(nova_palavra) == 5
        assert primeira_palavra.isalpha()
        assert nova_palavra.isalpha()
        # Nota: As palavras podem ser iguais por acaso, mas isso é estatisticamente raro
    
    def test_nova_partida_reinicia_tentativas_para_seis(self):
        """CT-UC04-05: Nova partida deve reiniciar com 6 tentativas (não 5 como primeira partida)"""
        jogo = VocabGame()
        jogo.iniciar_jogo()
        
        # Verificar que primeira partida tem 5 tentativas
        assert jogo.tentativas_restantes == 5
        
        # Finalizar partida
        jogo.finalizar_partida('vitoria')
        
        # Nova partida deve ter 6 tentativas
        jogo.iniciar_nova_partida()
        assert jogo.tentativas_restantes == 6
