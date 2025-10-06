"""
Testes para o Caso de Uso 3 - Finalizar Partida

Ator: Jogador
Descrição: O jogo é finalizado em duas situações:
- O jogador acertou a palavra secreta;
- O jogador esgotou todas as tentativas sem acertar.

O sistema apresenta uma mensagem de vitória ou derrota, calcula a pontuação do jogador 
(total ou parcial, conforme o desempenho) e exibe a palavra correta caso não tenha sido descoberta.
Pré-condição: Uma partida está em andamento.
Pós-condição: A partida é encerrada e a pontuação é registrada.
"""

import pytest
from backend.app.vocab_game import VocabGame


class TestUC03FinalizarPartida:
    """Testes para o Caso de Uso 3 - Finalizar Partida"""
    
    def test_finalizar_partida_por_vitoria(self):
        """CT-UC03-01: Finalizar partida quando jogador acerta a palavra"""
        jogo = VocabGame()
        jogo.iniciar_jogo()
        
        # Simular acerto da palavra secreta
        palavra_secreta = jogo.palavra_secreta
        jogo.finalizar_jogo(palavra_secreta)
        
        assert jogo.status == 'venceu'
    
    def test_finalizar_partida_por_derrota_tentativas_esgotadas(self):
        """CT-UC03-02: Finalizar partida quando tentativas se esgotam"""
        jogo = VocabGame()
        jogo.iniciar_jogo() 
        
        # Esgotar tentativas
        jogo.tentativas_restantes = 0
        jogo.finalizar_jogo("TESTE")  # palavra diferente da secreta
        
        assert jogo.status == 'perdeu'
    
    def test_feedback_palavra_correta_completa(self):
        """CT-UC03-03: Feedback deve indicar todas as letras corretas quando palavra está certa"""
        jogo = VocabGame()
        jogo.palavra_secreta = "CASAL"
        
        feedback = jogo.analisar_palpite("CASAL")
        
        assert len(feedback) == 5
        assert all(item['status'] == 'correto' for item in feedback)
        assert [item['letra'] for item in feedback] == ['C', 'A', 'S', 'A', 'L']
    
    def test_feedback_palavra_totalmente_incorreta(self):
        """CT-UC03-04: Feedback deve indicar todas as letras inexistentes quando não há nenhuma correta"""
        jogo = VocabGame()
        jogo.palavra_secreta = "CASAL"
        
        feedback = jogo.analisar_palpite("PORTO")
        
        assert len(feedback) == 5
        assert all(item['status'] == 'inexistente' for item in feedback)
        assert [item['letra'] for item in feedback] == ['P', 'O', 'R', 'T', 'O']
    
    def test_feedback_palavra_com_letras_mistas(self):
        """CT-UC03-05: Feedback deve indicar corretamente letras corretas, posição errada e inexistentes"""
        jogo = VocabGame()
        jogo.palavra_secreta = "CASAL"
        
        feedback = jogo.analisar_palpite("CARRO")
        
        statuses = [item['status'] for item in feedback]
        letras = [item['letra'] for item in feedback]
        
        assert letras == ['C', 'A', 'R', 'R', 'O']
        assert statuses == ['correto', 'correto', 'inexistente', 'inexistente', 'inexistente']
    
    def test_feedback_palavra_com_posicao_errada(self):
        """CT-UC03-06: Feedback deve indicar posição errada quando letra existe em outra posição"""
        jogo = VocabGame()
        jogo.palavra_secreta = "CASAL"
        
        feedback = jogo.analisar_palpite("ALCAR")
        
        statuses = [item['status'] for item in feedback]
        letras = [item['letra'] for item in feedback]
        
        assert letras == ['A', 'L', 'C', 'A', 'R']
        # A(pos 0): existe na pos 1 e 3 -> posicao_errada
        # L(pos 1): existe na pos 4 -> posicao_errada  
        # C(pos 2): existe na pos 0 -> posicao_errada
        # A(pos 3): correto na pos 3
        # R(pos 4): não existe -> inexistente
        assert statuses[0] == 'posicao_errada'  # A
        assert statuses[1] == 'posicao_errada'  # L
        assert statuses[2] == 'posicao_errada'  # C
        assert statuses[3] == 'correto'         # A
        assert statuses[4] == 'inexistente'     # R
    
    def test_finalizar_partida_marca_como_finalizado(self):
        """CT-UC03-07: Método finalizar_partida deve marcar status como finalizado"""
        jogo = VocabGame()
        jogo.iniciar_jogo()
        
        jogo.finalizar_partida('vitoria')
        
        assert jogo.status == 'finalizado'
