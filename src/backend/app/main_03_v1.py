#!/usr/bin/env python3
from src.vocab_game import VocabGame

def testar_uc_03_errado():
    print(" UC-03")
    
    jogo = VocabGame()
    jogo.iniciar_jogo()
    
    print(f"Palavra escolhida pelo jogo: {jogo.palavra_secreta}\n")
    
    palpites = [
        "CASAL",  # Esperado: tudo verde
        "PORTO",  # Esperado: tudo cinza
    ]
    
    for palpite in palpites:
        print(f"Palpite: {palpite}")
        feedback = jogo.analisar_palpite(palpite)
        
        print("  Resultado obtido:")
        for item in feedback:
            print(f"    {item['letra']} → {item['status']}")
        
        print("  Resultado esperado:")
        if palpite == "CASAL":
            print("    C → correto, A → correto, S → correto, A → correto, L → correto")
        else:
            print("    P → inexistente, O → inexistente, R → inexistente, T → inexistente, O → inexistente")
        
        print("⚠ Diferença detectada entre obtido e esperado.\n")


def main():
    print("1. Executar teste inicial do UC-03")
    print("2. Rodar testes automatizados")
    print("3. Sair")
    
    while True:
        opcao = input("\nEscolha (1-3): ").strip()
        
        if opcao == "1":
            testar_uc_03_errado()
        elif opcao == "2":
            print("Execute no terminal:")
            print("   python -m pytest tests/test_uc_03.py -v")
        elif opcao == "3":
            break
        else:
            print("❌ Opção inválida!")


if __name__ == "__main__":
    main()
