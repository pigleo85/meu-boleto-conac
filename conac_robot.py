import os
import time
import re
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
            page.goto("https://conac.com.br/2-via-de-boleto/", wait_until="domcontentloaded", timeout=120000)
            
            print("🔘 Clicando em Acesso Condomínio...")
            # Busca flexível por qualquer elemento que contenha 'Acesso' e 'Condomínio'
            btn_acesso = page.locator("a, button, div").filter(has_text=re.compile(r"Acesso.*Condom[íi]nio", re.IGNORECASE)).first
            
            try:
                btn_acesso.wait_for(state="attached", timeout=15000)
                btn_acesso.click(force=True)
            except Exception:
                print("⚠️ Botão principal não respondeu. Redirecionando direto para a área do cliente...")
                page.goto("https://areadocliente.conac.com.br/", wait_until="domcontentloaded", timeout=60000)

            print("📧 Inserindo e-mail...")
            # Aguarda e preenche qualquer campo de entrada de texto visível
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
