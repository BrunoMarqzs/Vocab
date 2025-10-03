from src.vocab_game import VocabGame

# Teste rápido do UC-03
jogo = VocabGame()
jogo.palavra_secreta = "CASAL"

print("Teste UC-03 - Feedback dos palpites:")
print(f"Palavra: {jogo.palavra_secreta}")

testes = ["CASAL", "CARRO", "PORTO"]

for tentativa in testes:
    print(f"\n{tentativa}:")
    resultado = jogo.analisar_palpite(tentativa)
    
    for item in resultado:
        print(f"{item['letra']} - {item['status']}")