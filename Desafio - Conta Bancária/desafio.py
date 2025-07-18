# Definindo o menu fora do loop para clareza
MENU = """
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

def depositar(saldo, valor, extrato, /): # O '/' indica que parâmetros anteriores a ele são somente posicionais
    """Realiza a operação de depósito."""
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n" # Adicionando uma tabulação para alinhamento
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques): # O '*' indica que parâmetros posteriores a ele são somente nomeados
    """Realiza a operação de saque."""
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
    elif excedeu_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
    elif valor <= 0: # Adicionado para tratar valor negativo ou zero
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    else:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n" # Adicionando tabulações
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")

    return saldo, extrato, numero_saques

def exibir_extrato(saldo, extrato, /):
    """Exibe o extrato de movimentações e o saldo atual."""
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}") # Alinhamento para o saldo
    print("==========================================")

def main():
    """Função principal que gerencia o fluxo do sistema bancário."""
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3 # Mantido como constante na função principal

    while True:
        opcao = input(MENU)

        if opcao == "d":
            try:
                valor = float(input("Informe o valor do depósito: "))
                saldo, extrato = depositar(saldo, valor, extrato)
            except ValueError:
                print("\n@@@ Valor inválido! Digite um número. @@@")

        elif opcao == "s":
            try:
                valor = float(input("Informe o valor do saque: "))
                saldo, extrato, numero_saques = sacar(
                    saldo=saldo,
                    valor=valor,
                    extrato=extrato,
                    limite=limite,
                    numero_saques=numero_saques,
                    limite_saques=LIMITE_SAQUES
                )
            except ValueError:
                print("\n@@@ Valor inválido! Digite um número. @@@")

        elif opcao == "e":
            exibir_extrato(saldo, extrato)

        elif opcao == "q":
            print("\nObrigado por usar nosso sistema bancário! Volte sempre!\n")
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

# Para garantir que a função main() seja chamada quando o script for executado
if __name__ == "__main__":
    main()