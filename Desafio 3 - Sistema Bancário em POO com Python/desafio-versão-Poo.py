import textwrap
from abc import ABC, abstractmethod # Usamos abstractmethod para tudo, pois abstractproperty foi depreciado
from datetime import datetime


# ==================== CLASSES DO MODELO UML ====================

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        # Adicionei a validação para garantir que é uma Transacao
        if isinstance(transacao, Transacao):
            transacao.registrar(conta)
        else:
            print("\n@@@ Transação inválida. Objeto de transação não reconhecido. @@@")

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
            return False # Adicionado retorno False para consistência
        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False # Adicionado retorno False para consistência

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite # Usei _limite para manter a convenção de atributo interno
        self._limite_saques = limite_saques # Usei _limite_saques para manter a convenção de atributo interno

    # Adicionando properties para limite e limite_saques para acesso consistente
    @property
    def limite(self):
        return self._limite

    @property
    def limite_saques(self):
        return self._limite_saques

    def sacar(self, valor):
        # A sua lógica de contar saques pelo histórico é mais robusta para limite geral/sem reset diário
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite # Acessando via property
        excedeu_saques = numero_saques >= self.limite_saques # Acessando via property

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
            return False
        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
            return False
        else:
            return super().sacar(valor) # Chama o sacar da classe pai (Conta)

    def __str__(self): # Excelente método para representação da conta
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"), # Correção: %S para segundos
            }
        )


class Transacao(ABC):
    @property
    @abstractmethod # Correção: usar abstractmethod para propriedades abstratas
    def valor(self):
        pass

    @abstractmethod # Correção: usar abstractmethod para métodos de instância abstratos
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
            return True # Adicionado retorno para consistência
        return False # Adicionado retorno para consistência


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
            return True # Adicionado retorno para consistência
        return False # Adicionado retorno para consistência


# ==================== FUNÇÕES DE INTERAÇÃO (MAIN) ====================

def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

def recuperar_conta_cliente(cliente, numero_conta):
    contas_do_cliente = cliente.contas
    conta_encontrada = [conta for conta in contas_do_cliente if conta.numero == numero_conta]
    return conta_encontrada[0] if conta_encontrada else None


def depositar_operacao(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    numero_conta = int(input("Informe o número da conta: "))
    conta = recuperar_conta_cliente(cliente, numero_conta)

    if not conta:
        print("\n@@@ Conta não encontrada para este cliente! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))
    deposito = Deposito(valor)
    cliente.realizar_transacao(conta, deposito)


def sacar_operacao(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    numero_conta = int(input("Informe o número da conta: "))
    conta = recuperar_conta_cliente(cliente, numero_conta)

    if not conta:
        print("\n@@@ Conta não encontrada para este cliente! @@@")
        return

    valor = float(input("Informe o valor do saque: "))
    saque = Saque(valor)
    cliente.realizar_transacao(conta, saque)


def exibir_extrato_operacao(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    numero_conta = int(input("Informe o número da conta: "))
    conta = recuperar_conta_cliente(cliente, numero_conta)

    if not conta:
        print("\n@@@ Conta não encontrada para este cliente! @@@")
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato_str = ""
    if not transacoes:
        extrato_str = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato_str += f"{transacao['tipo']}:\tR$ {transacao['valor']:.2f} ({transacao['data']})\n"

    print(extrato_str)
    print(f"\nSaldo:\t\tR$ {conta.saldo:.2f}")
    print("==========================================")


def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)

    print("=== Cliente criado com sucesso! ===")

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def criar_conta_operacao(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta) # Adiciona a conta ao cliente

    print("\n=== Conta criada com sucesso! ===")


def listar_contas_operacao(contas):
    if not contas:
        print("\n@@@ Nenhuma conta cadastrada. @@@")
        return

    for conta in contas:
        # Usando o __str__ que você adicionou em ContaCorrente, que é mais Pythonic
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


def main():
    clientes = []
    contas = []
    
    while True:
        opcao = menu()

        if opcao == "d":
            depositar_operacao(clientes)

        elif opcao == "s":
            sacar_operacao(clientes)

        elif opcao == "e":
            exibir_extrato_operacao(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta_operacao(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas_operacao(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()