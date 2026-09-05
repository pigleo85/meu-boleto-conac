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
            print("🚀 Acessando a página de 2ª via...")
            page.goto("https://conac.com.br/2-via-de-boleto/", wait_until="networkidle", timeout=120000)
            
            # Aguarda a renderização de frames dinâmicos do portal
            time.sleep(5)
            
            print("📧 Inserindo e-mail no formulário...")
            
            # Varre a página e eventuais iframes internos em busca do campo de entrada
            email_field = None
            for frame in page.frames:
                locator = frame.locator("input[name*='email' i], input[type='email'], input[placeholder*='email' i], input:visible").first
                if locator.count() > 0:
                    email_field = locator
                    break

            if not email_field:
                # Fallback: tenta localização direta na janela principal
                email_field = page.locator("input:visible").first

            email_field.wait_for(state="visible", timeout=45000)
            email_field.fill(os.environ['CONAC_EMAIL'])
            
            steps = ["Continuar", "Avançar", "Boleto Eletrônico", "Receber por e-mail"]
            
            for step in steps:
                print(f"👉 Clicando em: {step}")
                
                # Procura o botão em todos os frames ativos
                target = None
                for frame in page.frames:
                    loc = frame.locator(f"text={step}").first
                    if loc.count() > 0:
                        target = loc
                        break
                
                if not target:
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
