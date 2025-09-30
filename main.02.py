from src.vocab_game import VocabGame

def main():
    jogo = VocabGame()
    jogo.iniciar_jogo()
    
    print("=== JOGO TERMO ===")
    print("UC-02: Inserir Tentativa")
    print("Digite palavras de 5 letras para testar a validação")
    
    while True:
        palavra = input("\nDigite uma palavra (5 letras): ").strip().upper()
        
        if jogo.inserir_tentativa(palavra):
            print("✅ PALPITE VÁLIDO - UC-02 funcionando!")
        else:
            print("❌ Palpite inválido! Digite exatamente 5 letras.")
        
        continuar = input("\nTestar outra? (s/n): ").strip().lower()
        if continuar != 's':
            break
    
    print("\nUC-02 concluído com sucesso!")

if __name__ == "__main__":
    main()
