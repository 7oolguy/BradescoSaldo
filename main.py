from pegar_saldos_bradesco import BradescoBot, salvar_como_excel

if __name__ == "__main__":
    bot = BradescoBot(headless=False)  # Defina como True para rodar em modo headless
    driver = bot._driver()

    try:
        bot.login(driver)
        bot.navigate(driver)
        saldo = bot.mudar_contas_pelo_select(driver, max_qtd=300) # Mude a quantidade maxima para a quantidade de conta que você tem
        salvar_como_excel(saldo)
        print("Login realizado com sucesso!")
    except Exception as e:
        print(f"Erro durante o login: {e}")
    finally:
        driver.quit()
