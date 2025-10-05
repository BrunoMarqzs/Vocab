from backend.app.vocab_game import VocabGame

class TestUC02InserirTentativa:
    def test_palpite_valido_5_letras(self):
        """CT-UC02-01: Palpite válido de 5 letras"""
        jogo = VocabGame()
        resultado = jogo.inserir_tentativa("CASAL")
        assert resultado == True
    
    def test_palpite_invalido_menos_5_letras(self):
        """CT-UC02-02: Palpite inválido - menos de 5 letras"""
        jogo = VocabGame()
        resultado = jogo.inserir_tentativa("ABC")
        assert resultado == False
    
    def test_palpite_invalido_mais_5_letras(self):
        """CT-UC02-03: Palpite inválido - mais de 5 letras"""
        jogo = VocabGame()
        resultado = jogo.inserir_tentativa("ABCDEF")
        assert resultado == False
    
    def test_palpite_invalido_caracteres_nao_alfabeticos(self):
        """CT-UC02-04: Palpite com caracteres não alfabéticos"""
        jogo = VocabGame()
        resultado = jogo.inserir_tentativa("A1C2E")
        assert resultado == False

class TestVocabGameUC02:
    def test_fazer_tentativa_palavra_correta(self):
        """Teste UC-02.1: Fazer tentativa com palavra correta"""
        jogo = VocabGame()
        jogo.iniciar_jogo()
        
        # Simular tentativa com a palavra secreta (vitória)
        palavra_secreta = jogo.palavra_secreta
        resultado = jogo.inserir_tentativa(palavra_secreta)
        
        assert resultado['acertou'] == True
        assert jogo.status == 'vitoria'
        assert len(jogo.tabuleiro) == 1
           
    def test_fazer_tentativa_palavra_correta_v2(self):
        jogo = VocabGame()
        jogo.iniciar_jogo()

    # Simular tentativa com a palavra secreta (vitória)
        palavra_secreta = jogo.palavra_secreta
        acertou = jogo.inserir_tentativa(palavra_secreta)

        assert acertou == True
        
    def test_fazer_tentativa_palavra_incorreta(self):
        """Teste UC-02.2: Fazer tentativa com palavra incorreta"""
        jogo = VocabGame()
        jogo.iniciar_jogo()
        
        # Fazer tentativa com palavra diferente da secreta
        tentativa = "TESTE"  # Assumindo que não é a palavra secreta
        if tentativa == jogo.palavra_secreta:
            tentativa = "JOGAR"  # Fallback
            
        resultado = jogo.inserir_tentativa(tentativa)
        
        assert resultado['acertou'] == False
        assert jogo.status == 'em_andamento'
        assert jogo.tentativas_restantes == 5
        assert len(jogo.tabuleiro) == 1
