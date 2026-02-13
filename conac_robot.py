import os
import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        # Abre o navegador (modo headless = sem janela, para rodar na nuvem)
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print("Iniciando acesso ao site da Conac...")
        page.goto("https://conac.com.br/2-via-de-boleto/", wait_until="networkidle")

        # Passo 1: Clicar em Acesso Condomínio
        # Usamos o texto do botão para garantir o clique
        page.click("text=Acesso Condomínio")
        page.wait_for_load_state("networkidle")

        # Passo 2: Digitar o E-mail
        # O seletor 'input[type="email"]' ou 'input[name="email"]' costuma ser padrão
        # Se falhar, usaremos o seletor de posição
        email_input = "input[type='email'], input[name='email'], .form-control"
        page.fill(email_input, os.environ['USER_EMAIL'])
        
        # Passo 3: Clicar em Continuar
        page.click("text=Continuar")
        page.wait_for_load_state("networkidle")

        # Passo 4: Clicar em Avançar
        page.click("text=Avançar")
        page.wait_for_load_state("networkidle")

        # Passo 5: Clicar em Boleto Eletrônico
        page.click("text=Boleto Eletrônico")
        
        # Passo 6: Clicar em Receber por e-mail
        print("Finalizando: Clicando em Receber por e-mail...")
        page.click("text=Receber por e-mail")
        
        # Espera um pouco para garantir que o comando foi enviado
        time.sleep(5)
        print("Sucesso! O comando foi enviado.")
        
        browser.close()

if __name__ == "__main__":
    run()
