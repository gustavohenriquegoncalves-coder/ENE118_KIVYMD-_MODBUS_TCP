from servidormodbus import ServidorMODBUS


if __name__ == "__main__":
    servidor = ServidorMODBUS("localhost", 502)
    servidor.run()