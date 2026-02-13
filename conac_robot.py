import os
import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print("Iniciando acesso ao site da Conac...")
        page.goto("https://conac.com.br/2-via-de-boleto/", wait_until="networkidle")

        # Passo 1: Clicar em Acesso Condomínio
        page.click("text=Acesso Condomínio")
        page.wait_for_load_state("networkidle")

        # Passo 2: Digitar o E-mail (usando o Segredo que você criou)
        email_input = "input[type='email'], input[name='email'], .form-control"
        # Aqui ele busca o nome exato que você salvou: CONAC_EMAIL
        page.fill(email_input, os.environ['CONAC_EMAIL'])
        
        # Passo 3: Cliques de navegação
        page.click("text=Continuar")
        page.wait_for_load_state("networkidle")

        page.click("text=Avançar")
        page.wait_for_load_state("networkidle")

        page.click("text=Boleto Eletrônico")
        
        # Passo 4: Finalização
        print("Finalizando: Clicando em Receber por e-mail...")
        page.click("text=Receber por e-mail")
        
        time.sleep(5)
        print("Sucesso! O comando foi enviado.")
        browser.close()

if __name__ == "__main__":
    run()
