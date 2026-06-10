from pymodbus.client import ModbusTcpClient


class ClienteMODBUS:

    def __init__(self, server_ip="localhost", porta=502):
        self._cliente = ModbusTcpClient(host=server_ip, port=porta)

    def conectar(self):
        return self._cliente.connect()

    def fechar(self):
        self._cliente.close()

    def esta_conectado(self):
        #alteracao usado pela interface grafica
        return self._cliente.connected

    def ler_holding_registers(self, endereco, quantidade):
        resposta = self._cliente.read_holding_registers(
            address=endereco,
            count=quantidade,
            device_id=1
        )

        if resposta and not resposta.isError():
            return resposta.registers

        return None

    def ler_holding_register(self, endereco):
        registradores = self.ler_holding_registers(endereco, 1)

        if registradores is None:
            return None

        return registradores[0]

    def escrever_holding_register(self, endereco, valor):
        """
        Escreve um valor inteiro em um Holding Register.
        """
        resposta = self._cliente.write_register(
            address=endereco,
            value=int(valor),
            device_id=1
        )

        return resposta and not resposta.isError()

    def escrever_holding_registers(self, endereco, valores):
        """
        Escreve vários Holding Registers consecutivos.
        """
        resposta = self._cliente.write_registers(
            address=endereco,
            values=valores,
            device_id=1
        )

        return resposta and not resposta.isError()

    def escrever_float(self, endereco, valor):
        registradores = self._cliente.convert_to_registers(
            float(valor),
            self._cliente.DATATYPE.FLOAT32
        )

        return self.escrever_holding_registers(endereco, registradores)

    def ler_float(self, endereco):
        registradores = self.ler_holding_registers(endereco, 2)

        if registradores is None:
            return None

        valor = self._cliente.convert_from_registers(
            registradores,
            self._cliente.DATATYPE.FLOAT32
        )

        return valor

    def ler_bits_registrador(self, endereco):
        #alteracao leitura dos bits por operacao direta no inteiro
        valor = self.ler_holding_register(endereco)

        if valor is None:
            return None

        bits = []

        for posicao in range(16):
            bit = (valor >> posicao) & 1
            bits.append(bit)

        return bits

    def ler_bit_registrador(self, endereco, posicao_bit):
        #alteracao leitura de um bit especifico
        valor = self.ler_holding_register(endereco)

        if valor is None:
            return None

        posicao_bit = int(posicao_bit)

        if posicao_bit < 0 or posicao_bit > 15:
            return None

        bit = (valor >> posicao_bit) & 1

        return bit

    def alterar_bit_registrador(self, endereco, posicao_bit, novo_estado):
        # alteracao altera bit 
        valor_atual = self.ler_holding_register(endereco)

        if valor_atual is None:
            return False

        posicao_bit = int(posicao_bit)
        novo_estado = int(novo_estado)

        if posicao_bit < 0 or posicao_bit > 15:
            return False

        if novo_estado == 1:
            valor_novo = valor_atual | (1 << posicao_bit)
        else:
            valor_novo = valor_atual & ~(1 << posicao_bit)

        return self.escrever_holding_register(endereco, valor_novo)

    def alterar_bits_registrador(self, endereco, posicao_inicial, estados):
        # alteracao multiplos bits
        valor_atual = self.ler_holding_register(endereco)

        if valor_atual is None:
            return False

        posicao_inicial = int(posicao_inicial)

        for indice, estado in enumerate(estados):
            posicao = posicao_inicial + indice

            if 0 <= posicao < 16:
                if int(estado) == 1:
                    valor_atual = valor_atual | (1 << posicao)
                else:
                    valor_atual = valor_atual & ~(1 << posicao)

        return self.escrever_holding_register(endereco, valor_atual)

    def ler_coils(self, endereco, quantidade):
        #alteracao  coils
        resposta = self._cliente.read_coils(
            address=endereco,
            count=quantidade,
            device_id=1
        )

        if resposta and not resposta.isError():
            return resposta.bits[:quantidade]

        return None

    def ler_coil(self, endereco):
        #alteracao leitura de um coil
        coils = self.ler_coils(endereco, 1)

        if coils is None:
            return None

        return coils[0]

    def escrever_coil(self, endereco, valor):
        #alteracao escrita de um coil
        estado = bool(int(valor))

        resposta = self._cliente.write_coil(
            address=endereco,
            value=estado,
            device_id=1
        )

        return resposta and not resposta.isError()

    def escrever_coils(self, endereco, valores):
        #alteracao escrita de multiplos coils
        estados = [bool(int(valor)) for valor in valores]

        resposta = self._cliente.write_coils(
            address=endereco,
            values=estados,
            device_id=1
        )

        return resposta and not resposta.isError()