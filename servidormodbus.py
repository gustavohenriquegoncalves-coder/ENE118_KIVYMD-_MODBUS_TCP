from pyModbusTCP.server import DataBank, ModbusServer
from time import sleep
import random


class ServidorMODBUS:
    """
    Classe responsável apenas pelo servidor Modbus TCP de teste.
    """

    def __init__(self, host_ip="localhost", port=502):
        self._db = DataBank()
        self._server = ModbusServer(
            host=host_ip,
            port=port,
            no_block=True,
            data_bank=self._db
        )

    def run(self):
        """
        Executa o servidor Modbus TCP.
        """

        try:
            self._server.start()
            print("Servidor MODBUS em execução.")
            print("Pressione CTRL+C para encerrar.")

            # Valores iniciais de teste.
            # Eles são definidos apenas uma vez para não sobrescrever
            # os valores escritos pelo cliente.
            self._db.set_holding_registers(2000, [0])
            self._db.set_holding_registers(3000, [0, 0])
            self._db.set_holding_registers(4000, [0])
            self._db.set_coils(1000, [False])

            while True:
                # Este endereço muda automaticamente para testar leitura recorrente.
                valor_simulado = random.randrange(
                    int(0.95 * 400),
                    int(1.05 * 400)
                )

                self._db.set_holding_registers(1000, [valor_simulado])

                print("======================")
                print("Tabela MODBUS")
                print(f"Holding Register R1000: {self._db.get_holding_registers(1000)}")
                print(f"Holding Register R2000: {self._db.get_holding_registers(2000)}")
                print(f"Holding Register R3000/R3001: {self._db.get_holding_registers(3000, 2)}")
                print(f"Holding Register R4000: {self._db.get_holding_registers(4000)}")
                print(f"Coil C1000: {self._db.get_coils(1000)}")

                sleep(1)

        except KeyboardInterrupt:
            print("\nServidor encerrado pelo usuário.")
            self._server.stop()

        except Exception as erro:
            print("Erro no servidor:", erro)
            self._server.stop()