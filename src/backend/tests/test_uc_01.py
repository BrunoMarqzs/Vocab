"""
Testes para o Caso de Uso 1 - Iniciar Jogo

Ator: Jogador
Descrição: O jogador inicia a partida. O sistema sorteia uma palavra secreta de cinco letras 
e exibe o tabuleiro, juntamente com o número de tentativas restantes.
Pré-condição: O jogador acessou a tela inicial do jogo.
Pós-condição: O jogo é iniciado com a palavra secreta definida e as tentativas disponíveis.
"""

import pytest
from backend.app.vocab_game import VocabGame


class TestUC01IniciarJogo:
    """Testes para o Caso de Uso 1 - Iniciar Jogo"""
    
    def test_iniciar_jogo_cria_instancia(self):
        """CT-UC01-01: O jogo deve ser criado com sucesso"""
        jogo = VocabGame()
        assert jogo is not None
    
    def test_iniciar_jogo_sorteia_palavra_secreta(self):
        """CT-UC01-02: O jogo deve sortear uma palavra secreta de 5 letras"""
        jogo = VocabGame()
        jogo.iniciar_jogo()
        
        assert jogo.palavra_secreta is not None
        assert len(jogo.palavra_secreta) == 5
        assert jogo.palavra_secreta.isalpha()
        assert jogo.palavra_secreta.isupper()
    
    def test_iniciar_jogo_define_tentativas_restantes(self):
        """CT-UC01-03: O jogo deve iniciar com o número correto de tentativas"""
        jogo = VocabGame()
        jogo.iniciar_jogo()
        
        assert jogo.tentativas_restantes == 5
    
    def test_iniciar_jogo_tabuleiro_vazio(self):
        """CT-UC01-04: O jogo deve inicializar com tabuleiro vazio"""
        jogo = VocabGame()
        jogo.iniciar_jogo()
        
        assert jogo.tabuleiro is not None
        assert len(jogo.tabuleiro) == 0
        assert isinstance(jogo.tabuleiro, list)
    
    def test_iniciar_jogo_status_em_andamento(self):
        """CT-UC01-05: O jogo deve iniciar com status 'em_andamento'"""
        jogo = VocabGame()
        jogo.iniciar_jogo()
        
        assert jogo.status == 'em_andamento'
    
    def test_obter_estado_inicial_jogo(self):
        """CT-UC01-06: O estado inicial do jogo deve conter todas as informações necessárias"""
        jogo = VocabGame()
        jogo.iniciar_jogo()
        
        estado = jogo.obter_estado_jogo()
        
        assert 'tentativas_restantes' in estado
        assert 'tabuleiro' in estado
        assert 'status' in estado
        
        assert estado['tentativas_restantes'] == 5
        assert estado['tabuleiro'] == []
        assert estado['status'] == 'em_andamento'
    
    def test_palavra_secreta_diferente_em_jogos_diferentes(self):
        """CT-UC01-07: Jogos diferentes devem ter palavras secretas potencialmente diferentes"""
        jogo1 = VocabGame()
        jogo2 = VocabGame()
        
        jogo1.iniciar_jogo()
        jogo2.iniciar_jogo()
        
        # As palavras podem ser iguais por acaso, mas ambas devem ser válidas
        assert len(jogo1.palavra_secreta) == 5
        assert len(jogo2.palavra_secreta) == 5
        assert jogo1.palavra_secreta.isalpha()
        assert jogo2.palavra_secreta.isalpha()
