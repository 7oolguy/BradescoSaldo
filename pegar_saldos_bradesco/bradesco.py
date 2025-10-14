import os
import time
import re
from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


def criar_driver(headless=False) -> webdriver.Chrome:
    """
        Cria e retorna uma instância do driver do Chrome com as configurações especificadas.

        Parâmetros:
            headless (bool): Se True, executa o navegador em modo headless (sem interface gráfica).

        Retorna:
            webdriver.Chrome: Instância do driver do Chrome configurado.
    """

    # Criando uma instância de ChromeOptions para configurar o navegador
    chrome_options = webdriver.ChromeOptions()

    # Se o modo headless for ativado, adiciona argumentos para rodar sem interface gráfica
    if headless:
        print("Modo invisível ativado.")  # Mensagem indicando que o modo headless está ativado
        chrome_options.add_argument("--headless")  # Ativa o modo sem interface gráfica
        chrome_options.add_argument("--disable-gpu")  # Evita problemas gráficos no modo headless

    # Configurações para evitar a detecção de automação pelo site
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Remove a flag de automação
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36"
    )  # Define um user-agent customizado para imitar um usuário real
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Remove a mensagem de automação
    chrome_options.add_experimental_option("useAutomationExtension", False)  # Desativa extensões automáticas do ChromeDriver

    # Configuração de logs do navegador (log-level 0 = nenhum log extra no console)
    chrome_options.add_argument("--log-level=0")

    # Obtém o diretório atual do script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Calcula o diretório do backend subindo três níveis acima
    backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))

    # Define o diretório padrão para downloads do Chrome
    prefs = {
        "download.default_directory": f"{backend_dir}"  # Define a pasta onde os downloads serão salvos
    }
    chrome_options.add_experimental_option("prefs", prefs)  # Aplica as preferências ao Chrome

    # Cria uma instância do driver do Chrome com as opções configuradas
    driver = webdriver.Chrome(options=chrome_options)

    # Executa um script no navegador para remover a propriedade "webdriver", dificultando a detecção de bot
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )

    print("Instância do Chrome foi iniciada.")  # Mensagem informando que o driver foi iniciado com sucesso
    return driver  # Retorna o driver criado

class BradescoBot:
    def __init__(self, headless: bool=False):
        """
        Inicializa a classe BradescoBot.

        Parâmetros:
        - headless (bool): Indica se o navegador será iniciado sem interface gráfica (modo headless).
        """
        self.headless = headless
        self.url = "https://www.ne12.bradesconetempresa.b.br/ibpjlogin/login.jsf"
        self.usuario = ""  # Nome de usuário para login
        self.senha = ""    # Senha para login

    def _driver(self) -> webdriver.Chrome:
        """
        Cria e retorna uma instância do navegador Chrome com as configurações definidas.
        """
        return criar_driver(headless=self.headless)

    def login(self, driver: webdriver.Chrome):
        """
        Realiza o login no site do Bradesco.

        Parâmetros:
        - driver (webdriver.Chrome): Instância do navegador controlada pelo Selenium.
        """
        driver.maximize_window()  # Maximiza a janela do navegador
        wait = WebDriverWait(driver, 10)  # Configura um tempo de espera explícito de 10 segundos

        while True:
            try:
                driver.get(self.url)  # Abre a URL de login

                # Aguarda até que o elemento do tipo de acesso esteja visível e clica nele
                try:
                    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="rdoTipoAcesso02"]')))
                    driver.find_element(By.XPATH, '//*[@id="rdoTipoAcesso02"]').click()
                except:
                    print("O Botão para escolher o tipo de acesso não foi encontrado, continuando ...")
                    pass 
                
                # Tentativas de login
                tentativa = 0
                tentativa_maxima = 3
                while tentativa < tentativa_maxima:
                    try:
                        # Campo do usuário
                        wait.until(EC.presence_of_element_located((By.ID, "identificationForm:txtUsuario")))
                        driver.find_element(By.ID, "identificationForm:txtUsuario").clear()
                        driver.find_element(By.ID, "identificationForm:txtUsuario").send_keys(self.usuario)

                        # Campo da senha
                        wait.until(EC.presence_of_element_located((By.ID, "identificationForm:txtSenha")))
                        driver.find_element(By.ID, "identificationForm:txtSenha").clear()
                        driver.find_element(By.ID, "identificationForm:txtSenha").send_keys(self.senha)
                        break  # Se conseguiu preencher os campos, sai do loop
                    except Exception as e:
                        print(f"Não foi possível realizar o login. Tentativa {tentativa + 1} -> {e}")
                        tentativa += 1
                        time.sleep(1)  # Aguarda um segundo antes de tentar novamente

                # Aguarda e clica no botão de login
                wait.until(EC.element_to_be_clickable((By.ID, "identificationForm:botaoAvancar")))
                driver.find_element(By.ID, "identificationForm:botaoAvancar").click()

                # Verifica se o login falhou
                try:
                    close_modal = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="btnFecharModal"]')))
                    if close_modal:
                        close_modal.click()  # Fecha o modal de erro
                        driver.get(self.url)  # Recarrega a página

                        # Tentativas de login novamente
                        tentativa = 0
                        while tentativa < tentativa_maxima:
                            try:
                                # Campo do usuário
                                wait.until(EC.presence_of_element_located((By.ID, "identificationForm:txtUsuario")))
                                driver.find_element(By.ID, "identificationForm:txtUsuario").clear()
                                driver.find_element(By.ID, "identificationForm:txtUsuario").send_keys(self.usuario)

                                # Campo da senha
                                wait.until(EC.presence_of_element_located((By.ID, "identificationForm:txtSenha")))
                                driver.find_element(By.ID, "identificationForm:txtSenha").clear()
                                driver.find_element(By.ID, "identificationForm:txtSenha").send_keys(self.senha)
                                break  # Sai do loop se os campos forem preenchidos corretamente
                            except Exception as e:
                                print(f"Não foi possível realizar o login. Tentativa {tentativa + 1} -> {e}")
                                tentativa += 1
                                time.sleep(1)
                        wait.until(EC.element_to_be_clickable((By.ID, "identificationForm:botaoAvancar")))
                        driver.find_element(By.ID, "identificationForm:botaoAvancar").click()
                except:
                    pass  # Se não houver modal de erro, segue normalmente

                # Aguarda até que a URL mude para a página inicial, indicando que o login foi bem-sucedido
                try:
                    WebDriverWait(driver, 120).until(EC.url_contains("paginaInicial"))
                    break  # Sai do loop principal se o login foi concluído
                except TimeoutException:
                    raise ValueError("Login Falhou")

            except ValueError as e:
                print(f"Tentativa: {tentativa + 1} -> {e}")
                try:
                    # Verifica se existe um modal de erro e tenta fechá-lo
                    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="cancelarAcessoModalForm:_id378"]')))
                    driver.find_element(By.XPATH, '//*[@id="cancelarAcessoModalForm:_id378"]').click()
                except Exception as e:
                    print(f"Erro durante a tentativa de reiniciar: {e}")

    def selecionar_empresa(self, driver: webdriver.Chrome, group, final_cnpj):
        """
        Seleciona a empresa desejada dentro do sistema Bradesco.

        Parâmetros:
        - driver (webdriver.Chrome): Instância do navegador controlada pelo Selenium.
        - group (int): Índice do grupo econômico da empresa na tabela.
        - final_cnpj (str): Últimos dígitos do CNPJ para identificar a empresa correta.
        """
        wait = WebDriverWait(driver, 15)  # Define um tempo de espera explícito de 15 segundos

        try:
            try:
                # Fecha qualquer modal de overlay que possa estar bloqueando a tela
                wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'jqmOverlay')))
                driver.find_element(By.CLASS_NAME, 'jqmOverlay').click()
            except:
                wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body[1]/div')))
                driver.find_element(By.XPATH, '/html/body[1]/div').click()
        except:
            pass  # Se não houver modal, continua normalmente

        try:
            # Aguarda a presença do elemento que contém o CNPJ da empresa atualmente selecionada
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="_id118"]')))
            el_text = driver.find_element(By.XPATH, '//*[@id="_id118"]').text

            # Verifica se a empresa correta já está selecionada
            if final_cnpj not in el_text:
                # Se a empresa errada estiver selecionada, clica para abrir a lista de empresas
                wait.until(EC.element_to_be_clickable((By.ID, "lnkGrupoEconomico")))
                driver.find_element(By.ID, "lnkGrupoEconomico").click()

                attempt = 0
                max_tries = 3
                while attempt < max_tries:
                    try:
                        # Aguarda a abertura do modal de seleção de empresa e alterna para o frame correspondente
                        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="modal_infra_estrutura"]')))
                        driver.switch_to.frame(
                            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="modal_infra_estrutura"]')))
                        )
                        break
                    except Exception as e:
                        attempt += 1
                        time.sleep(1)  # Aguarda um segundo antes de tentar novamente

                # Seleciona a empresa pelo índice fornecido (group)
                wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="tabelaEmpresas"]/tbody/tr[{group}]/td[1]')))
                driver.find_element(By.XPATH, f'//*[@id="tabelaEmpresas"]/tbody/tr[{group}]/td[1]').click()

                # Retorna para o conteúdo principal da página
                driver.switch_to.default_content()

                while True:
                    try:
                        # Aguarda e clica no botão de confirmação
                        wait.until(EC.element_to_be_clickable((By.ID, "_id351")))
                        driver.find_element(By.ID, "_id351").click()
                        break
                    except:
                        try:
                            # Caso haja um modal bloqueando, tenta fechá-lo e clicar novamente
                            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "jqmOverlay")))
                            driver.find_element(By.CLASS_NAME, "jqmOverlay").click()
                            wait.until(EC.element_to_be_clickable((By.ID, "_id351")))
                            driver.find_element(By.ID, "_id351").click()
                        except:
                            pass
                return

            print("Não tem necessidade de mudar a empresa.")
        except Exception as e:
            print(f"ERRO -> Algo deu errado ao mudar a empresa -> {e}")

    def navigate(self, driver: webdriver.Chrome):
        """
        Navega para a aba específica dentro do sistema Bradesco.

        Parâmetros:
        - driver (webdriver.Chrome): Instância do navegador controlada pelo Selenium.
        - texto_aba (str): Nome da aba para onde deseja navegar (padrão: 'Cadastros e débitos').
        """
        wait = WebDriverWait(driver, 15)  # Define um tempo de espera explícito de 15 segundos

        try:
            try:
                # Fecha qualquer modal de overlay que possa estar bloqueando a tela
                wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'jqmOverlay')))
                driver.find_element(By.CLASS_NAME, 'jqmOverlay').click()
            except:
                wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body[1]/div')))
                driver.find_element(By.XPATH, '/html/body[1]/div').click()
        except:
            pass   # Se não houver modal, continua normalmente

        try:
            # Aguarda a visibilidade do elemento de navegação principal
            wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="_id69_0:_id71"]')))
            driver.find_element(By.XPATH, '//*[@id="_id69_0:_id71"]').click()

            # Aguarda a visibilidade do iframe que contém o conteúdo principal
            wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="paginaCentral"]')))

            # Alterna para o iframe correto
            driver.switch_to.frame(
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="paginaCentral"]')))
            )

            # Aguarda a visibilidade do link da aba desejada e clica nele
            wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="conteudo"]/div[2]/div[2]/div[1]/ul[1]/li[1]/a')
            )
    )
            driver.find_element(By.XPATH, f'//*[@id="conteudo"]/div[2]/div[2]/div[1]/ul[1]/li[1]/a' ).click()
        except Exception as e:
            print(f"ERRO -> Algo deu errado ao navegar para a página -> {e}")
            raise ValueError("Erro ao acessar a Página.")

    def mudar_contas_pelo_select(self, driver: webdriver.Chrome, max_qtd:int = 300)->List[Dict[str, float]]:
        """
        Change account selection and get balance for each selected account

        Args:
            driver: Selenium WebDriver instance
            qtd: Maximum number of accounts to process

        Returns:
            List of dictionaries containing account and balance information
        """
        select_xpath = "//*[@id='formFiltroSaldos:filtroContaCorrente:comboContas']"

        conta_list = []
        saldo_list = []

        try:
            # Encontrar o elemento select
            WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, select_xpath))
            )
            select_elem = driver.find_element(By.XPATH, select_xpath)
            select = Select(select_elem)
            print("Iniciando Loop")
            options = select.options

            i = 0
            # Iterar sobre as opções
            for option in options[1:]:
                option_text = option.text
                option_value = option.get_attribute("value")

                # Verifica se qualquer filtro está contido no texto da opção
                try:
                    # log.info(f"Selecionando a opção: {option.text}")
                    select.select_by_visible_text(option.text)
                    conta_list.append(option.text)

                    # Obter saldo após selecionar a opção
                    # Wait for loading image to disappear
                    try:
                        WebDriverWait(driver, 60).until(
                            EC.invisibility_of_element_located((By.XPATH, '//*[@id="divLoading"]/img'))
                        )
                    except TimeoutException:
                        print("Loading image did not disappear")
                        pass

                    saldo_list = self.pegar_saldo(driver, saldo_list)
                    i += 1
                except Exception as e:
                    print(f"Erro ao selecionar a opção {option.text}: {e}")

                if i >= max_qtd:
                    break

            # Ajustar o formato das contas
            new_conta = [self.trim_string(conta) for conta in conta_list]

            result_list = [
                {"conta": conta, "saldo": saldo}
                for conta, saldo in zip(new_conta, saldo_list)
            ]
        except Exception as e:
            print(f"Erro ao acessar o elemento select: {e}")
            result_list = []

        print("Fim do loop")
        return result_list

    def trim_string(self, text):
        """
        Transform account numbers from format '03396 | 0000098-1' to '0098-1'
        or from '03396 | 0001934-8' to '1934-8'
        Always maintains 4 digits before the hyphen.

        Args:
            text (str): Account number string to transform

        Returns:
            str: Transformed account number with exactly 4 digits before the hyphen
        """
        try:
            # Split by '|' and take the second part
            account = text.split('|')[1].strip()

            # Split by '-' to separate the main number and check digit
            main_num, check_digit = account.split('-')

            # Remove leading zeros and get the clean number
            clean_num = str(int(main_num))

            # Ensure 4 digits by padding with zeros if needed
            clean_num = clean_num.zfill(4)

            # Combine with check digit
            result = f"{clean_num}-{check_digit}"

            return result
        except Exception as e:
            print(f"Error processing account string '{text}': {e}")
            return text  # Return original string if processing fails

    def pegar_saldo(self, driver, saldo=None, max_tries=5):
        """
        Get balance from selected account using multiple possible XPaths

        Args:
            driver: Selenium WebDriver instance
            saldo: List to store balance values (default: None)
            max_tries: Maximum number of attempts to find balance (default: 5)

        Returns:
            List with updated balance values
        """

        def _formata_saldo_para_valor_programacao(text):
            """
            Convert string to money format

            Args:
                text: String to convert
            """
            if not text:
                return "0.00"

            # Remove any non-numeric characters except decimal point and minus sign
            cleaned = re.sub(r'[^\d.,-]', '', text)
            new_number = cleaned.replace('.', '').replace(',', '.')

            try:
                # Convert to float and format to 2 decimal places
                value = float(new_number)
                return f"{value:.2f}"
            except:
                return "0.00"

        attempt = 0
        while attempt < max_tries:
            try:
                wait = WebDriverWait(driver, 5)

                # Tentar encontrar o saldo com múltiplos XPaths em uma única chamada de espera
                xpath_list = [
                    "//*[@id='divTransacaoSaldo']/div[2]/div/div/table/tbody/tr/td/div/div[1]/div[1]/table/tbody/tr/td[2]",
                    "//*[@id='divTransacaoSaldo']/div[2]/div[1]/div/table/tbody/tr/td/div/div[1]/div[1]/table/tbody/tr/td[2]",
                    "//*[@id='divTransacaoSaldo']/div[2]/div[2]/div/table/tbody/tr/td/div/div[1]/div[1]/table/tbody/tr/td[2]",
                ]

                # Verifique a visibilidade de qualquer um dos elementos
                for xpath in xpath_list:
                    try:
                        element = wait.until(
                            EC.visibility_of_element_located((By.XPATH, xpath))
                        )
                        saldo_ = _formata_saldo_para_valor_programacao(element.text)
                        print(f"Valor da conta: {saldo_}")
                        saldo.append(saldo_)
                        return saldo
                    except Exception:
                        print(f"Não foi possível achar o saldo usando o XPath: {xpath}.")

                # Se todas as tentativas falharem, aguarde e tente novamente
                attempt += 1

            except Exception as e:
                print(f"Erro ao tentar encontrar o saldo: {e}")
                saldo.append("")
                return saldo

        # Caso não encontre o saldo após todas as tentativas
        saldo.append("")
        return saldo
