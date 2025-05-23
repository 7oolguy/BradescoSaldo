# Script para pegar Saldo Bradesco

Documentação

## Preparo

Para Rodar, basta clicar 2 vezes o start.bat, ou se preferir seguir os seguintes passos manualmente:

Antes de iniciar certifique-se de que está usando a ultima versão do python para isso abra o CMD:

- `Win + R` e digite CMD e precione ENTER.

Uma janela preta vai abrir o Terminal e então digite:

- `winget upgrade python` e o python vai ser atualizado para a ultima versão.

Em seguida ainda pelo terminal navegue até a pasta em que o programa se encontra e digite:

- `pip install -r requirements.txt` para instalar as bibliotecas necessarias.

Agora está tudo pronto para Rodar, inicie manualmente o script main.py!

---

# Documentação do BradescoBot

## Visão Geral

Este projeto implementa um bot para automação de login e navegação no site do Bradesco Empresas. O bot utiliza a biblioteca Selenium para interagir com a interface web do banco, permitindo automatizar tarefas como login, seleção de empresa e navegação entre abas.

## Requisitos

- Python 3.x
- Selenium
- WebDriver do Chrome

## Instalação

1. Baixe o WebDriver do Chrome correspondente à versão do seu navegador.
2. Certifique-se de que o WebDriver está no PATH ou forneça o caminho ao inicializar o driver.

## Estrutura do Código

### Criar Driver

A função `criar_driver` cria uma instância configurada do Chrome WebDriver.

```python
def criar_driver(headless=False) -> webdriver.Chrome:
```

**Parâmetros:**

- `headless` (bool): Define se o navegador será executado sem interface gráfica.

**Retorno:**

- `webdriver.Chrome`: Instância do navegador configurada.

---

### Classe `BradescoBot`

A classe `BradescoBot` encapsula a lógica do bot.

```python
class BradescoBot:
```

#### Inicialização

```python
def __init__(self, headless: bool=False):
```

**Parâmetros:**

- `headless` (bool): Define se o navegador será iniciado sem interface gráfica.

---

#### Método `login`

```python
def login(self, driver: webdriver.Chrome):
```

**Parâmetros:**

- `driver` (webdriver.Chrome): Instância do navegador.

**Descrição:**
Realiza o login no site do Bradesco Empresas, preenchendo o formulário e tratando possíveis erros de acesso.

---

#### Método `selecionar_empresa`

```python
def selecionar_empresa(self, driver: webdriver.Chrome, group: int, final_cnpj: str):
```

**Parâmetros:**

- `driver` (webdriver.Chrome): Instância do navegador.
- `group` (int): Índice do grupo da empresa.
- `final_cnpj` (str): Filtro para encontrar a empresa correta pelo CNPJ.

**Descrição:**
Seleciona a empresa dentro do sistema do Bradesco, caso não esteja previamente selecionada.

---

#### Método `navigate`

```python
def navigate(self, driver: webdriver.Chrome, texto_aba: str='saldos'):
```

**Parâmetros:**

- `driver` (webdriver.Chrome): Instância do navegador.
- `texto_aba` (str): Nome da aba para onde deseja navegar (padrão: 'saldos').

**Descrição:**
Navega para a aba especificada no sistema do Bradesco.

---

#### Método `mudar_contas_pelo_select`

```python
def mudar_contas_pelo_select(self, driver: webdriver.Chrome, max_qtd: int=300):
```

**Parâmetros:**

- `driver` (webdriver.Chrome): Instância do navegador.
- `max_qtd` (int): Quantidade máxima de contas a processar.

**Descrição:**
Alterna entre diferentes contas e obtém os saldos correspondentes.

---

## Uso

```python
bot = BradescoBot(headless=True)
driver = bot._driver()
bot.login(driver)
bot.selecionar_empresa(driver, group=1, final_cnpj='1234')
bot.navigate(driver, texto_aba='saldos')
```

## Observações

- O bot requer credenciais válidas para login.
- Sites bancários possuem proteções contra automação, podendo bloquear acessos automatizados.

---

# Documentação da Função `<span>salvar_como_excel</span>`

## Descrição

A função `<span>salvar_como_excel</span>` recebe uma lista de dicionários contendo informações de contas e saldos, converte esses dados em um arquivo Excel formatado como tabela e salva no caminho especificado.

## Parâmetros

- **dados** (`<span>list[dict[str, float]]</span>`): Lista de dicionários contendo as chaves `<span>conta</span>` (int) e `<span>saldo</span>` (float).
- **nome_arquivo** (`<span>str</span>`): Nome do arquivo Excel a ser salvo. Valor padrão: `<span>"output.xlsx"</span>`.

## Funcionamento

1. Verifica se a lista de dados está vazia. Se estiver, exibe uma mensagem e retorna.
2. Checa se o arquivo já existe e está aberto. Caso esteja, solicita ao usuário que o feche.
3. Converte os dados para um `<span>DataFrame</span>` do `<span>pandas</span>`.
4. Cria um novo arquivo Excel e uma planilha chamada `<span>Contas</span>`.
5. Adiciona os dados do `<span>DataFrame</span>` à planilha.
6. Define um intervalo de tabela e aplica um estilo para melhor visualização.
7. Ajusta automaticamente a largura das colunas para melhor apresentação.
8. Salva o arquivo Excel e exibe uma mensagem confirmando a ação.

## Dependências

A função requer as seguintes bibliotecas para funcionar corretamente:

- `<span>pandas</span>`
- `<span>openpyxl</span>`
- `<span>os</span>`

## Exemplo de Uso

```python
from salvar_excel import salvar_como_excel

dados = [
    {"conta": 12345, "saldo": 1000.50},
    {"conta": 67890, "saldo": 2500.75}
]

salvar_como_excel(dados, "contas.xlsx")
```

## Autor

Desenvolvido por Yan Souza Silva.
