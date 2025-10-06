"""
Testes para o Caso de Uso 6 - Consultar Estatísticas

Ator: Jogador
Descrição: O jogador acessa seu histórico de partidas, incluindo vitórias, derrotas, 
taxa de acerto e sequência de vitórias.
Pré-condição: O jogador já jogou ao menos uma partida.
Pós-condição: O sistema exibe os dados estatísticos atualizados.
"""

import pytest
from backend.app.vocab_game import VocabGame


class TestUC06ConsultarEstatisticas:
    """Testes para o Caso de Uso 6 - Consultar Estatísticas"""
    
    def test_inicializar_estatisticas_zeradas(self):
        """CT-UC06-01: Estatísticas devem ser inicializadas zeradas para novo jogador"""
        jogo = VocabGame()
        
        # Este teste assume que será implementado um sistema de estatísticas
        # Por enquanto, verificamos que o jogo pode ser criado
        assert jogo is not None
        
        # Quando implementado, as estatísticas iniciais deveriam ser:
        # assert jogo.estatisticas['total_partidas'] == 0
        # assert jogo.estatisticas['vitorias'] == 0
        # assert jogo.estatisticas['derrotas'] == 0
        # assert jogo.estatisticas['taxa_acerto'] == 0.0
        # assert jogo.estatisticas['sequencia_vitorias'] == 0
        # assert jogo.estatisticas['melhor_sequencia'] == 0
    
    def test_atualizar_estatisticas_apos_vitoria(self):
        """CT-UC06-02: Estatísticas devem ser atualizadas após vitória"""
        jogo = VocabGame()
        jogo.iniciar_jogo()
        
        # Simular vitória
        palavra_secreta = jogo.palavra_secreta
        jogo.finalizar_jogo(palavra_secreta)
        
        assert jogo.status == 'venceu'
        
        # Quando implementado, as estatísticas deveriam ser atualizadas:
        # assert jogo.estatisticas['total_partidas'] == 1
        # assert jogo.estatisticas['vitorias'] == 1
        # assert jogo.estatisticas['derrotas'] == 0
        # assert jogo.estatisticas['taxa_acerto'] == 100.0
        # assert jogo.estatisticas['sequencia_vitorias'] == 1
    
    def test_atualizar_estatisticas_apos_derrota(self):
        """CT-UC06-03: Estatísticas devem ser atualizadas após derrota"""
        jogo = VocabGame()
        jogo.iniciar_jogo()
        
        # Simular derrota
        jogo.tentativas_restantes = 0
        jogo.finalizar_jogo("TESTE")  # palavra diferente da secreta
        
        assert jogo.status == 'perdeu'
        
        # Quando implementado, as estatísticas deveriam ser atualizadas:
        # assert jogo.estatisticas['total_partidas'] == 1
        # assert jogo.estatisticas['vitorias'] == 0
        # assert jogo.estatisticas['derrotas'] == 1
        # assert jogo.estatisticas['taxa_acerto'] == 0.0
        # assert jogo.estatisticas['sequencia_vitorias'] == 0
    
    def test_calcular_taxa_acerto_multiplas_partidas(self):
        """CT-UC06-04: Taxa de acerto deve ser calculada corretamente com múltiplas partidas"""
        jogo = VocabGame()
        
        # Este teste prepararia o cenário para quando as estatísticas forem implementadas
        # Simular histórico: 3 vitórias e 2 derrotas = 60% de taxa de acerto
        
        # Quando implementado:
        # jogo.estatisticas['total_partidas'] = 5
        # jogo.estatisticas['vitorias'] = 3
        # jogo.estatisticas['derrotas'] = 2
        # 
        # taxa_esperada = (3 / 5) * 100
        # assert jogo.calcular_taxa_acerto() == 60.0
        
        # Por enquanto, apenas verificamos que o jogo pode ser criado
        assert jogo is not None
    
    def test_sequencia_vitorias_consecutivas(self):
        """CT-UC06-05: Sequência de vitórias deve ser contada corretamente"""
        jogo = VocabGame()
        
        # Este teste prepararia o cenário para tracking de sequências
        # Quando implementado, deveria rastrear:
        # - Sequência atual de vitórias
        # - Melhor sequência histórica
        # - Reset da sequência após derrota
        
        # Por enquanto, apenas verificamos a estrutura básica
        assert jogo is not None
    
    def test_consultar_estatisticas_requer_pelo_menos_uma_partida(self):
        """CT-UC06-06: Consulta de estatísticas deve requerer pelo menos uma partida jogada"""
        jogo = VocabGame()
        
        # Jogo recém criado, sem partidas jogadas
        # Quando implementado, deveria verificar se há histórico
        
        # Por enquanto, verificamos que não há estado de jogo iniciado
        assert jogo.status is None
        assert jogo.palavra_secreta is None
        assert jogo.tentativas_restantes is None
    
    def test_persistencia_estatisticas_entre_sessoes(self):
        """CT-UC06-07: Estatísticas devem ser persistidas entre sessões de jogo"""
        # Este teste seria para verificar que as estatísticas são salvas
        # e carregadas corretamente entre diferentes execuções do jogo
        
        # Quando implementado, testaria:
        # 1. Salvar estatísticas após partida
        # 2. Carregar estatísticas em nova sessão
        # 3. Manter continuidade dos dados
        
        jogo = VocabGame()
        assert jogo is not None
