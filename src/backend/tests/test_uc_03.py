from backend.app.vocab_game import VocabGame

def test_feedback_correto():
    jogo = VocabGame()
    jogo.palavra_secreta = "CASAL"
    
    feedback = jogo.analisar_palpite("CASAL")
    assert all(item['status'] == 'correto' for item in feedback)

def test_feedback_inexistente():
    jogo = VocabGame()
    jogo.palavra_secreta = "CASAL"
    
    feedback = jogo.analisar_palpite("PORTO")
    assert all(item['status'] == 'inexistente' for item in feedback)

def test_feedback_misto():
    jogo = VocabGame()
    jogo.palavra_secreta = "CASAL"
    
    feedback = jogo.analisar_palpite("CARRO")
    statuses = [item['status'] for item in feedback]
    assert statuses == ['correto', 'correto', 'inexistente', 'inexistente', 'inexistente']