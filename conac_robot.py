import os
import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        # Lança o navegador
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
        page = context.new_page()
        
        try:
            print("Acessando o site...")
            page.goto("https://conac.com.br/2-via-de-boleto/", wait_until="load", timeout=60000)
            
            # Espera o botão aparecer antes de clicar
            print("Procurando botão 'Acesso Condomínio'...")
            page.wait_for_selector("text=Acesso Condomínio", timeout=30000)
            page.click("text=Acesso Condomínio")
            
            # Espera a página de login carregar
            print("Digitando e-mail...")
            page.wait_for_selector("input", timeout=30000)
            # Tenta encontrar o campo de e-mail de forma mais genérica
            page.keyboard.type(os.environ['CONAC_EMAIL'])
            
            print("Clicando em Continuar...")
            page.get_by_text("Continuar").click()
            
            print("Clicando em Avançar...")
            page.wait_for_timeout(3000) # Pausa de segurança
            page.get_by_text("Avançar").click()
            
            print("Clicando em Boleto Eletrônico...")
            page.wait_for_timeout(3000)
            page.get_by_text("Boleto Eletrônico").click()
            
            print("Solicitando envio por e-mail...")
            page.get_by_text("Receber por e-mail").click()
            
            time.sleep(10) # Tempo para o site processar o envio
            print("Finalizado com sucesso!")

        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            # Tira um print do erro para a gente ver o que o robô estava vendo
            page.screenshot(path="erro_print.png")
            raise e
        finally:
            browser.close()

if __name__ == "__main__":
    run()
