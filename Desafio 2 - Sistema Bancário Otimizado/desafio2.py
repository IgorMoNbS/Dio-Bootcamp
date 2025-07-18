import textwrap

def menu():
    menu_text = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nu]\tNovo usuário
    [nc]\tNova conta
    [lc]\tListar contas
    [lu]\tListar usuários
    [q]\tSair
    => """
    return input(textwrap.dedent(menu_text))

# --- Funções Auxiliares de Validação de Entrada ---

def ler_valor_float(mensagem):
    while True:
        try:
            valor = float(input(mensagem))
            if valor < 0: # Não permite valores negativos para operações
                print("\n@@@ Operação falhou! O valor deve ser positivo. @@@")
                continue
            return valor
        except ValueError:
            print("\n@@@ Operação falhou! Entrada inválida. Digite um número. @@@")

def ler_numero_int(mensagem):
    while True:
        try:
            numero = int(input(mensagem))
            if numero < 0:
                print("\n@@@ Operação falhou! O número deve ser positivo. @@@")
                continue
            return numero
        except ValueError:
            print("\n@@@ Operação falhou! Entrada inválida. Digite um número inteiro. @@@")

# --- Funções para operações bancárias ---

def depositar(conta, valor, /):
    if valor > 0:
        conta["saldo"] += valor
        conta["extrato"] += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        # Esta validação já é feita em ler_valor_float, mas mantida por redundância ou clareza.
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

def sacar(*, conta, valor, limite, limite_saques):
    excedeu_saldo = valor > conta["saldo"]
    excedeu_limite = valor > limite
    excedeu_saques = conta["numero_saques_hoje"] >= limite_saques

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite (R$ %.2f). @@@" % limite)
    elif excedeu_saques:
        print(f"\n@@@ Operação falhou! Número máximo de saques diários ({limite_saques}) excedido para esta conta. @@@")
    elif valor > 0:
        conta["saldo"] -= valor
        conta["extrato"] += f"Saque:\t\tR$ {valor:.2f}\n"
        conta["numero_saques_hoje"] += 1
        print("\n=== Saque realizado com sucesso! ===")
    else:
        # Esta validação já é feita em ler_valor_float, mas mantida por redundância ou clareza.
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

def exibir_extrato(conta, /):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not conta["extrato"] else conta["extrato"])
    print(f"\nSaldo:\t\tR$ {conta['saldo']:.2f}")
    print("==========================================")

# --- Funções para Gerenciamento de Usuários e Contas ---

def criar_usuario(usuarios):
    while True:
        cpf = input("Informe o CPF (somente números, 11 dígitos): ")
        if not cpf.isdigit() or len(cpf) != 11:
            print("\n@@@ CPF inválido! O CPF deve conter exatamente 11 números. @@@")
            continue
        break # Sai do loop se o CPF for válido

    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Já existe usuário com este CPF! Retornando ao menu. @@@")
        return # Retorna sem criar o usuário

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("=== Usuário criado com sucesso! ===")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def filtrar_conta(numero_conta, contas):
    contas_filtradas = [conta for conta in contas if conta["numero_conta"] == numero_conta]
    return contas_filtradas[0] if contas_filtradas else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário para vincular a conta: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if not usuario:
        print("\n@@@ Usuário não encontrado! Fluxo de criação de conta encerrado. Retornando ao menu. @@@")
        return None # Retorna None para indicar que a conta não foi criada

    conta = {
        "agencia": agencia,
        "numero_conta": numero_conta,
        "usuario": usuario,
        "saldo": 0.0,
        "extrato": "",
        "numero_saques_hoje": 0
    }
    print("\n=== Conta criada com sucesso! ===")
    return conta

def listar_contas(contas):
    if not contas:
        print("\n@@@ Nenhuma conta cadastrada. @@@")
        return

    print("\n============== CONTAS BANCÁRIAS ==============")
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
            CPF Titular:\t{conta['usuario']['cpf']}
            Saldo:\t\tR$ {conta['saldo']:.2f}
            """
        print("-" * 40)
        print(textwrap.dedent(linha))
    print("==============================================")

def listar_usuarios(usuarios):
    if not usuarios:
        print("\n@@@ Nenhum usuário cadastrado. @@@")
        return

    print("\n============== USUÁRIOS CADASTRADOS ==============")
    for usuario in usuarios:
        linha = f"""\
            Nome:\t\t{usuario['nome']}
            CPF:\t\t{usuario['cpf']}
            Data Nasc.:\t{usuario['data_nascimento']}
            Endereço:\t{usuario['endereco']}
            """
        print("-" * 40)
        print(textwrap.dedent(linha))
    print("==================================================")


# --- Função principal para execução do programa ---
def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            numero_conta = ler_numero_int("Informe o número da conta para depósito: ")
            if numero_conta is None: # Se a leitura falhou, volta para o menu
                continue

            conta = filtrar_conta(numero_conta, contas)

            if not conta:
                print("\n@@@ Conta não encontrada! Retornando ao menu. @@@")
                continue

            valor = ler_valor_float("Informe o valor do depósito: ")
            if valor is None: # Se a leitura falhou, volta para o menu
                continue

            depositar(conta, valor)

        elif opcao == "s":
            numero_conta = ler_numero_int("Informe o número da conta para saque: ")
            if numero_conta is None:
                continue

            conta = filtrar_conta(numero_conta, contas)

            if not conta:
                print("\n@@@ Conta não encontrada! Retornando ao menu. @@@")
                continue

            valor = ler_valor_float("Informe o valor do saque: ")
            if valor is None:
                continue

            sacar(conta=conta, valor=valor, limite=500, limite_saques=LIMITE_SAQUES)

        elif opcao == "e":
            numero_conta = ler_numero_int("Informe o número da conta para extrato: ")
            if numero_conta is None:
                continue

            conta = filtrar_conta(numero_conta, contas)

            if not conta:
                print("\n@@@ Conta não encontrada! Retornando ao menu. @@@")
                continue

            exibir_extrato(conta)

        elif opcao == "nu":
            criar_usuario(usuarios) # A função criar_usuario já gerencia o retorno para o menu

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta: # Apenas adiciona se a conta foi realmente criada
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "lu":
            listar_usuarios(usuarios)

        elif opcao == "q":
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

# Ponto de entrada do programa
if __name__ == "__main__":
    main()