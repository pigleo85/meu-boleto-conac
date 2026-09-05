import os
import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            print("🚀 Acessando portal do condomínio direto...")
            # Acessa diretamente a URL final onde o e-mail é digitado
            page.goto("https://conac.superlogica.net/clients/arena", wait_until="domcontentloaded", timeout=90000)
            
            print("📧 Inserindo e-mail...")
            # Localiza o campo de entrada e preenche com o segredo configurado
            input_email = page.locator("input[type='email'], input[type='text'], input:visible").first
            input_email.wait_for(state="visible", timeout=45000)
            input_email.fill(os.environ['CONAC_EMAIL'])
            
            steps = ["Continuar", "Avançar", "Boleto Eletrônico", "Receber por e-mail"]
            
            for step in steps:
                print(f"👉 Clicando em: {step}")
                target = page.locator(f"text={step}").first
                target.wait_for(state="visible", timeout=30000)
                target.click()
                time.sleep(4)
            
            print("✅ Sucesso! O boleto foi solicitado para o e-mail.")

        except Exception as e:
            print(f"❌ Erro detectado durante a execução: {e}")
            page.screenshot(path="erro_execucao.png")
            raise e
        finally:
            browser.close()

if __name__ == "__main__":
    run()
