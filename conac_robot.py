import os
import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        # Lança o navegador com configurações para parecer um humano
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 720})
        page = context.new_page()
        
        try:
            print("Acessando o site (modo rápido)...")
            # O segredo é o wait_until="domcontentloaded", que é muito mais rápido
            page.goto("https://conac.com.br/2-via-de-boleto/", wait_until="domcontentloaded", timeout=90000)
            
            print("Procurando botão 'Acesso Condomínio'...")
            # Espera o botão estar visível antes de clicar
            page.wait_for_selector("text=Acesso Condomínio", state="visible", timeout=30000)
            page.click("text=Acesso Condomínio")
            
            print("Aguardando carregamento da tela de e-mail...")
            page.wait_for_load_state("domcontentloaded")
            
            # Localiza o campo de e-mail e digita
            # Tentando seletores comuns em portais de condomínio
            page.wait_for_selector("input", timeout=20000)
            page.fill("input", os.environ['CONAC_EMAIL'])
            
            print("Navegando pelos menus...")
            page.get_by_text("Continuar").click()
            page.wait_for_timeout(2000)
            
            page.get_by_text("Avançar").click()
            page.wait_for_timeout(2000)
            
            page.get_by_text("Boleto Eletrônico").click()
            page.wait_for_timeout(2000)
            
            print("Finalizando: Solicitando envio por e-mail...")
            page.get_by_text("Receber por e-mail").click()
            
            # Aguarda confirmação visual na tela (opcional)
            time.sleep(5)
            print("Missão cumprida! O e-mail foi solicitado.")

        except Exception as e:
            print(f"Ocorreu um erro técnico: {e}")
            raise e
        finally:
            browser.close()

if __name__ == "__main__":
    run()
