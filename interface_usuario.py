from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from kivymd.uix.boxlayout import MDBoxLayout

from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.menu import MDDropdownMenu

from clientemodbus import ClienteMODBUS


class AplicacaoModbus(MDApp):
    """
    Interface gráfica em KivyMD.

    Esta classe apenas coleta dados da tela e chama os métodos da classe
    ClienteMODBUS. A lógica de comunicação Modbus fica separada.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._cliente = None
        self._evento_leitura = None

        self.tipo_selecionado = "holding"
        self.menu_tipo = None

        self.campo_ip = None
        self.campo_porta = None
        self.botao_tipo = None
        self.campo_endereco = None
        self.campo_quantidade = None
        self.campo_valor = None
        self.campo_bit = None
        self.checkbox_recorrente = None
        self.label_status = None
        self.label_resultado = None

    def build(self):
        self.title = "Cliente Modbus TCP - KivyMD"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"

        scroll = ScrollView()

        layout = MDBoxLayout(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(12),
            size_hint_y=None
        )

        layout.bind(minimum_height=layout.setter("height"))

        titulo = MDLabel(
            text="Cliente Modbus TCP",
            halign="center",
            font_style="H5",
            size_hint_y=None,
            height=dp(50)
        )

        layout.add_widget(titulo)

        self.campo_ip = self._criar_campo("IP do servidor", "localhost")
        self.campo_porta = self._criar_campo("Porta", "502")
        self.campo_endereco = self._criar_campo("Endereço Modbus", "1000")
        self.campo_quantidade = self._criar_campo("Quantidade para leitura", "1")
        self.campo_valor = self._criar_campo("Valor para escrita", "0")
        self.campo_bit = self._criar_campo("Bit específico", "0")

        layout.add_widget(self.campo_ip)
        layout.add_widget(self.campo_porta)

        label_tipo = MDLabel(
            text="Tipo de dado Modbus",
            halign="left",
            size_hint_y=None,
            height=dp(24)
        )

        self.botao_tipo = MDRaisedButton(
            text="holding",
            size_hint_y=None,
            height=dp(48)
        )
        self.botao_tipo.bind(on_release=self.abrir_menu_tipo)

        itens_menu = [
            {
                "text": "coil",
                "viewclass": "OneLineListItem",
                "height": dp(48),
                "on_release": lambda x="coil": self.selecionar_tipo(x),
            },
            {
                "text": "holding",
                "viewclass": "OneLineListItem",
                "height": dp(48),
                "on_release": lambda x="holding": self.selecionar_tipo(x),
            },
            {
                "text": "float",
                "viewclass": "OneLineListItem",
                "height": dp(48),
                "on_release": lambda x="float": self.selecionar_tipo(x),
            },
            {
                "text": "bits",
                "viewclass": "OneLineListItem",
                "height": dp(48),
                "on_release": lambda x="bits": self.selecionar_tipo(x),
            },
        ]

        self.menu_tipo = MDDropdownMenu(
            caller=self.botao_tipo,
            items=itens_menu,
            width_mult=4
        )

        layout.add_widget(label_tipo)
        layout.add_widget(self.botao_tipo)

        layout.add_widget(self.campo_endereco)
        layout.add_widget(self.campo_quantidade)
        layout.add_widget(self.campo_valor)
        layout.add_widget(self.campo_bit)

        linha_checkbox = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(8),
            size_hint_y=None,
            height=dp(48)
        )

        self.checkbox_recorrente = MDCheckbox(
            size_hint=(None, None),
            size=(dp(48), dp(48))
        )

        texto_checkbox = MDLabel(
            text="Leitura recorrente",
            valign="center"
        )

        linha_checkbox.add_widget(self.checkbox_recorrente)
        linha_checkbox.add_widget(texto_checkbox)

        layout.add_widget(linha_checkbox)

        botao_conectar = MDRaisedButton(
            text="Conectar",
            size_hint_y=None,
            height=dp(48)
        )
        botao_conectar.bind(on_release=self.conectar)

        botao_ler = MDRaisedButton(
            text="Ler",
            size_hint_y=None,
            height=dp(48)
        )
        botao_ler.bind(on_release=self.ler)

        botao_escrever = MDRaisedButton(
            text="Escrever",
            size_hint_y=None,
            height=dp(48)
        )
        botao_escrever.bind(on_release=self.escrever)

        botao_parar = MDRaisedButton(
            text="Parar leitura recorrente",
            size_hint_y=None,
            height=dp(48)
        )
        botao_parar.bind(on_release=self.parar_leitura_recorrente)

        layout.add_widget(botao_conectar)
        layout.add_widget(botao_ler)
        layout.add_widget(botao_escrever)
        layout.add_widget(botao_parar)

        self.label_status = MDLabel(
            text="Status: desconectado",
            halign="center",
            size_hint_y=None,
            height=dp(40)
        )

        self.label_resultado = MDLabel(
            text="Resultado:",
            halign="left",
            size_hint_y=None,
            height=dp(180)
        )

        layout.add_widget(self.label_status)
        layout.add_widget(self.label_resultado)

        scroll.add_widget(layout)

        return scroll

    def _criar_campo(self, hint, texto_inicial):
        return MDTextField(
            hint_text=hint,
            text=texto_inicial,
            mode="rectangle",
            size_hint_y=None,
            height=dp(60)
        )

    def abrir_menu_tipo(self, *args):
        self.menu_tipo.open()

    def selecionar_tipo(self, tipo):
        self.tipo_selecionado = tipo
        self.botao_tipo.text = tipo
        self.menu_tipo.dismiss()

    def conectar(self, *args):
        try:
            ip = self.campo_ip.text.strip()
            porta = int(self.campo_porta.text.strip())

            self._cliente = ClienteMODBUS(ip, porta)

            if self._cliente.conectar():
                self.label_status.text = f"Status: conectado em {ip}:{porta}"
            else:
                self.label_status.text = "Status: falha ao conectar"

        except Exception as erro:
            self.label_status.text = f"Erro ao conectar: {erro}"

    def ler(self, *args):
        if not self._verificar_conexao():
            return

        if self.checkbox_recorrente.active:
            self._iniciar_leitura_recorrente()
        else:
            self._realizar_leitura()

    def escrever(self, *args):
        if not self._verificar_conexao():
            return

        try:
            tipo = self.tipo_selecionado
            endereco = int(self.campo_endereco.text.strip())
            valor_texto = self.campo_valor.text.strip()
            bit_especifico = int(self.campo_bit.text.strip())

            sucesso = False

            if tipo == "coil":
                sucesso = self._cliente.escrever_coil(endereco, valor_texto)

            elif tipo == "holding":
                sucesso = self._cliente.escrever_holding_register(
                    endereco,
                    int(valor_texto)
                )

            elif tipo == "float":
                sucesso = self._cliente.escrever_float(
                    endereco,
                    float(valor_texto)
                )

            elif tipo == "bits":
                # alteracao: escrita de bit unico ou multiplos bits
                valores = self._converter_lista_valores(valor_texto)

                if len(valores) == 1:
                    sucesso = self._cliente.alterar_bit_registrador(
                        endereco,
                        bit_especifico,
                        valores[0]
                    )
                else:
                    sucesso = self._cliente.alterar_bits_registrador(
                        endereco,
                        bit_especifico,
                        valores
                    )

            if sucesso:
                self.label_resultado.text = "Escrita realizada com sucesso."
            else:
                self.label_resultado.text = "Falha na escrita."

        except Exception as erro:
            self.label_resultado.text = f"Erro na escrita: {erro}"

    def _realizar_leitura(self):
        try:
            tipo = self.tipo_selecionado
            endereco = int(self.campo_endereco.text.strip())
            quantidade = int(self.campo_quantidade.text.strip())
            bit_especifico = int(self.campo_bit.text.strip())

            if tipo == "coil":
                resultado = self._cliente.ler_coils(endereco, quantidade)

            elif tipo == "holding":
                resultado = self._cliente.ler_holding_registers(
                    endereco,
                    quantidade
                )

            elif tipo == "float":
                resultado = self._cliente.ler_float(endereco)

            elif tipo == "bits":
                # alteracao: mostra somente um bit por vez
                bit_lido = self._cliente.ler_bit_registrador(
                    endereco,
                    bit_especifico
                )

                resultado = f"Bit {bit_especifico}: {bit_lido}"

            else:
                resultado = None

            self.label_resultado.text = (
                f"Leitura realizada\n"
                f"Tipo: {tipo}\n"
                f"Endereço: {endereco}\n"
                f"Resultado: {resultado}"
            )

        except Exception as erro:
            self.label_resultado.text = f"Erro na leitura: {erro}"

    def _iniciar_leitura_recorrente(self):
        if self._evento_leitura is None:
            self._evento_leitura = Clock.schedule_interval(
                self._leitura_recorrente,
                1
            )

        self.label_status.text = "Status: leitura recorrente ativa"

    def _leitura_recorrente(self, dt):
        self._realizar_leitura()

    def parar_leitura_recorrente(self, *args):
        if self._evento_leitura is not None:
            self._evento_leitura.cancel()
            self._evento_leitura = None

        if self.checkbox_recorrente is not None:
            self.checkbox_recorrente.active = False

        if self._cliente is not None and self._cliente.esta_conectado():
            self.label_status.text = "Status: conectado"
        else:
            self.label_status.text = "Status: desconectado"

    def _verificar_conexao(self):
        if self._cliente is None or not self._cliente.esta_conectado():
            self.label_status.text = "Status: conecte ao servidor primeiro"
            return False

        return True

    def _converter_lista_valores(self, texto):
        """
        Converte entradas como:
        '1'
        '0'
        '1,0,1,1'
        """

        partes = texto.replace(" ", "").split(",")
        return [int(parte) for parte in partes if parte != ""]

    def on_stop(self):
        self.parar_leitura_recorrente()

        if self._cliente is not None:
            self._cliente.fechar()