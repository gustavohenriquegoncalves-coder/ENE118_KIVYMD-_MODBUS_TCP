# Projeto MODBUS TCP com Interface Gráfica em KivyMD

Projeto desenvolvido para a disciplina de Informática Industrial.

O objetivo do projeto é desenvolver uma aplicação gráfica em Python, utilizando KivyMD, capaz de realizar leitura e escrita de dados em um servidor Modbus TCP.

## Funcionalidades

A aplicação permite:

* Conectar a um servidor Modbus TCP por IP e porta.
* Ler e escrever Holding Registers.
* Ler e escrever Coils.
* Ler e escrever valores float.
* Ler um bit específico de um registrador.
* Alterar um bit específico de um registrador.
* Alterar múltiplos bits de um registrador.
* Realizar leitura única ou leitura recorrente usando o módulo Clock do Kivy.

## Estrutura do projeto

```text
Projeto_MODBUS/
├── cliente/
│   ├── main.py
│   ├── interface_usuario.py
│   ├── clientemodbus.py
│   └── requirements.txt
│
├── servidor/
│   ├── main.py
│   ├── servidormodbus.py
│   └── requirements.txt
│
├── .gitignore
└── README.md
```

## Organização do código

O projeto foi organizado separando a interface gráfica da lógica de comunicação Modbus.

A classe `ClienteMODBUS`, presente no arquivo `cliente/clientemodbus.py`, contém os métodos de conexão, leitura, escrita e conversão de dados Modbus.

A interface gráfica, presente no arquivo `cliente/interface_usuario.py`, apenas coleta os dados informados pelo usuário e chama os métodos da classe `ClienteMODBUS`.

A classe de comunicação Modbus foi reaproveitada da atividade anterior. Foram mantidos os métodos de conexão, leitura e escrita de Holding Registers, leitura e escrita de valores float e manipulação de bits. Foram adicionados apenas os métodos necessários para atender aos novos requisitos da atividade, como leitura e escrita de Coils, verificação de conexão, leitura de bit específico e alteração de múltiplos bits.

## Servidor Modbus de teste

O projeto contém um servidor Modbus TCP de teste na pasta `servidor`.

Esse servidor é usado para validar a comunicação com a aplicação gráfica. Ele permite testar leitura e escrita de Holding Registers, Coils, valores float e bits de registradores.

O servidor também atualiza periodicamente o Holding Register de endereço `1000` com um valor aleatório próximo de `400`, permitindo testar a função de leitura recorrente da interface gráfica.

Para testar a aplicação, primeiro execute o servidor e, em seguida, execute o cliente gráfico.

Caso seja utilizado um servidor Modbus TCP externo, basta informar o IP e a porta desse servidor nos campos da interface gráfica.

## Execução do servidor

Entre na pasta do servidor:

```cmd
cd servidor
```

Crie o ambiente virtual:

```cmd
python -m venv .venv
```

Ative o ambiente virtual:

```cmd
.venv\Scripts\activate.bat
```

Instale as dependências:

```cmd
python -m pip install -r requirements.txt
```

Execute o servidor:

```cmd
python main.py
```

## Execução do cliente

Abra outro terminal e entre na pasta do cliente:

```cmd
cd cliente
```

Crie o ambiente virtual:

```cmd
python -m venv .venv
```

Ative o ambiente virtual:

```cmd
.venv\Scripts\activate.bat
```

Instale as dependências:

```cmd
python -m pip install -r requirements.txt
```

Execute o cliente:

```cmd
python main.py
```

## Como testar

Com o servidor em execução, abra o cliente e utilize:

```text
IP: localhost
Porta: 502
```

Clique em `Conectar`.

## Teste de Holding Register

Selecione:

```text
Tipo: holding
Endereço: 2000
Quantidade para leitura: 1
Valor para escrita: 1234
Bit específico: 0
```

Clique em `Escrever`.

Depois clique em `Ler`.

Resultado esperado:

```text
[1234]
```

## Teste de Coil

Selecione:

```text
Tipo: coil
Endereço: 1000
Quantidade para leitura: 1
Valor para escrita: 1
Bit específico: 0
```

Clique em `Escrever`.

Depois clique em `Ler`.

Resultado esperado:

```text
[True]
```

Depois altere o valor para `0`, clique em `Escrever` e depois em `Ler`.

Resultado esperado:

```text
[False]
```

## Teste de Float

Selecione:

```text
Tipo: float
Endereço: 3000
Quantidade para leitura: 1
Valor para escrita: 12.5
Bit específico: 0
```

Clique em `Escrever`.

Depois clique em `Ler`.

Resultado esperado:

```text
12.5
```

Dependendo da representação interna do float, o valor pode aparecer com uma pequena diferença decimal.

## Teste de bit específico

Primeiro escreva um valor inteiro em um registrador:

```text
Tipo: holding
Endereço: 4000
Quantidade para leitura: 1
Valor para escrita: 10
Bit específico: 0
```

Clique em `Escrever`.

O valor `10` em binário é `1010`.

Depois selecione:

```text
Tipo: bits
Endereço: 4000
Quantidade para leitura: 1
Valor para escrita: 0
Bit específico: 1
```

Clique em `Ler`.

Resultado esperado:

```text
Bit 1: 1
```

Também é possível testar:

```text
Bit 0: 0
Bit 1: 1
Bit 2: 0
Bit 3: 1
```

## Teste de alteração de bit específico

Com o registrador `4000` contendo o valor `10`, selecione:

```text
Tipo: bits
Endereço: 4000
Quantidade para leitura: 1
Valor para escrita: 1
Bit específico: 0
```

Clique em `Escrever`.

Depois selecione:

```text
Tipo: holding
Endereço: 4000
Quantidade para leitura: 1
```

Clique em `Ler`.

Resultado esperado:

```text
[11]
```

Isso ocorre porque o valor `10` em binário é `1010`. Ao alterar o bit 0 para `1`, o valor passa a ser `1011`, que corresponde a `11` em decimal.

## Teste de múltiplos bits

Selecione:

```text
Tipo: bits
Endereço: 4000
Quantidade para leitura: 1
Valor para escrita: 1,1,1,1
Bit específico: 0
```

Clique em `Escrever`.

Depois selecione:

```text
Tipo: holding
Endereço: 4000
Quantidade para leitura: 1
```

Clique em `Ler`.

Resultado esperado:

```text
[15]
```

Isso ocorre porque os quatro primeiros bits ficam em `1111`, que corresponde ao valor decimal `15`.

## Teste de leitura recorrente

Selecione:

```text
Tipo: holding
Endereço: 1000
Quantidade para leitura: 1
Valor para escrita: 0
Bit específico: 0
```

Marque a opção `Leitura recorrente`.

Clique em `Ler`.

O valor lido deve ser atualizado periodicamente.

Para parar, clique em `Parar leitura recorrente`.

## Instruções gerais de teste

1. Execute primeiro o servidor, localizado na pasta `servidor`.
2. Em outro terminal, execute o cliente gráfico, localizado na pasta `cliente`.
3. Na interface do cliente, utilize:

   * IP: `localhost`
   * Porta: `502`
4. Clique em `Conectar`.
5. Realize os testes de leitura e escrita usando os campos da interface.

## Observações

As pastas `.venv` não devem ser enviadas para o repositório. Elas podem ser recriadas utilizando os arquivos `requirements.txt`.

O servidor incluído no projeto é apenas um servidor de teste para validar a comunicação Modbus TCP com o cliente gráfico.

O repositório contém o código da aplicação gráfica em KivyMD, a classe de comunicação Modbus reutilizada da última aula, o servidor Modbus de teste, os arquivos `requirements.txt`, o arquivo `README.md` com instruções de execução e o arquivo `.gitignore`.
