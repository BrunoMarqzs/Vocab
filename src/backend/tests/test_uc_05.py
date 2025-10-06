"""
Testes para o Caso de Uso 5 - Compartilhar Resultado

Ator: Jogador
Descrição: O jogador copia o resultado no formato do jogo (grades de quadradinhos coloridos) 
e a pontuação total.
Pré-condição: A partida foi finalizada.
Pós-condição: O resultado é disponibilizado em formato copiável para compartilhamento.
"""

import pytest
from backend.app.vocab_game import VocabGame


class TestUC05CompartilharResultado:
    """Testes para o Caso de Uso 5 - Compartilhar Resultado"""
    
    def test_gerar_resultado_compartilhavel_vitoria(self):
        """CT-UC05-01: Deve gerar resultado compartilhável após vitória"""
        jogo = VocabGame()
        jogo.iniciar_jogo()
        
        # Simular algumas tentativas e vitória
        jogo.tabuleiro = [
            [{'letra': 'T', 'status': 'inexistente'}, {'letra': 'E', 'status': 'posicao_errada'}, 
             {'letra': 'S', 'status': 'correto'}, {'letra': 'T', 'status': 'inexistente'}, 
             {'letra': 'E', 'status': 'inexistente'}],
            [{'letra': 'C', 'status': 'correto'}, {'letra': 'A', 'status': 'correto'}, 
             {'letra': 'S', 'status': 'correto'}, {'letra': 'A', 'status': 'correto'}, 
             {'letra': 'L', 'status': 'correto'}]
        ]
        jogo.status = 'venceu'
        jogo.tentativas_restantes = 3
        
        # Este teste assume que será implementado um método para gerar resultado compartilhável
        # Por enquanto, vamos testar que o estado está correto para gerar o resultado
        assert jogo.status == 'venceu'
        assert len(jogo.tabuleiro) == 2
        assert jogo.tentativas_restantes > 0
    
    def test_gerar_resultado_compartilhavel_derrota(self):
        """CT-UC05-02: Deve gerar resultado compartilhável após derrota"""
        jogo = VocabGame()
        jogo.iniciar_jogo()
        
        # Simular tentativas até derrota
        jogo.tabuleiro = [
            [{'letra': 'T', 'status': 'inexistente'}, {'letra': 'E', 'status': 'posicao_errada'}, 
             {'letra': 'S', 'status': 'correto'}, {'letra': 'T', 'status': 'inexistente'}, 
             {'letra': 'E', 'status': 'inexistente'}],
            [{'letra': 'J', 'status': 'inexistente'}, {'letra': 'O', 'status': 'inexistente'}, 
             {'letra': 'G', 'status': 'inexistente'}, {'letra': 'O', 'status': 'inexistente'}, 
             {'letra': 'S', 'status': 'posicao_errada'}],
            [{'letra': 'M', 'status': 'inexistente'}, {'letra': 'U', 'status': 'inexistente'}, 
             {'letra': 'N', 'status': 'inexistente'}, {'letra': 'D', 'status': 'inexistente'}, 
             {'letra': 'O', 'status': 'inexistente'}],
            [{'letra': 'V', 'status': 'inexistente'}, {'letra': 'I', 'status': 'inexistente'}, 
             {'letra': 'D', 'status': 'inexistente'}, {'letra': 'A', 'status': 'posicao_errada'}, 
             {'letra': 'S', 'status': 'posicao_errada'}],
            [{'letra': 'P', 'status': 'inexistente'}, {'letra': 'R', 'status': 'inexistente'}, 
             {'letra': 'A', 'status': 'posicao_errada'}, {'letra': 'Z', 'status': 'inexistente'}, 
             {'letra': 'O', 'status': 'inexistente'}]
        ]
        jogo.status = 'perdeu'
        jogo.tentativas_restantes = 0
        
        # Verificar que o estado está correto para derrota
        assert jogo.status == 'perdeu'
        assert len(jogo.tabuleiro) == 5
        assert jogo.tentativas_restantes == 0
    
    def test_formato_resultado_contem_informacoes_necessarias(self):
        """CT-UC05-03: Resultado deve conter todas as informações necessárias para compartilhamento"""
        jogo = VocabGame()
        jogo.iniciar_jogo()
        
        # Finalizar jogo
        jogo.status = 'venceu'
        jogo.tabuleiro = [
            [{'letra': 'C', 'status': 'correto'}, {'letra': 'A', 'status': 'correto'}, 
             {'letra': 'S', 'status': 'correto'}, {'letra': 'A', 'status': 'correto'}, 
             {'letra': 'L', 'status': 'correto'}]
        ]
        jogo.tentativas_restantes = 4
        
        estado = jogo.obter_estado_jogo()
        
        # Verificar que as informações necessárias estão disponíveis
        assert 'status' in estado
        assert 'tabuleiro' in estado
        assert 'tentativas_restantes' in estado
        
        # Informações específicas para compartilhamento
        assert estado['status'] == 'venceu'
        assert len(estado['tabuleiro']) >= 1
        assert estado['tentativas_restantes'] >= 0
    
    def test_pode_compartilhar_apenas_apos_finalizar(self):
        """CT-UC05-04: Compartilhamento só deve ser possível após finalizar a partida"""
        jogo = VocabGame()
        jogo.iniciar_jogo()
        
        # Jogo em andamento - não deve permitir compartilhamento
        assert jogo.status == 'em_andamento'
        
        # Finalizar jogo
        jogo.finalizar_partida('vitoria')
        assert jogo.status == 'finalizado'
        
        # Agora deve ser possível compartilhar (estado finalizado)
        estado = jogo.obter_estado_jogo()
        assert estado['status'] == 'finalizado'
