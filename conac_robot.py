import os
import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        # Lança o navegador com um perfil de usuário real para evitar bloqueios
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            print("🚀 Acessando a página de 2ª via...")
            # Usamos 'commit' para não esperar o lixo do site carregar 100%
            page.goto("https://conac.com.br/2-via-de-boleto/", wait_until="commit", timeout=60000)
            
            # 1. Clique em Acesso Condomínio
            print("🔘 Clicando em Acesso Condomínio...")
            btn_acesso = page.locator("text=Acesso Condomínio").first
            btn_acesso.wait_for(state="visible", timeout=30000)
            btn_acesso.click()
            
            # 2. Digitar o E-mail
            # O log mostrou que existem 3 campos 'input'. Vamos focar no visível.
            print("📧 Inserindo e-mail...")
            # Este seletor busca apenas o campo que o usuário realmente consegue ver
            input_email = page.locator("input:visible").first
            input_email.wait_for(state="visible", timeout=30000)
            input_email.fill(os.environ['CONAC_EMAIL'])
            
            # 3. Fluxo de Cliques (Navegação interna)
            # Usamos esperas forçadas curtas para o site processar as trocas de tela
            print("⏭️ Avançando no menu...")
            steps = ["Continuar", "Avançar", "Boleto Eletrônico", "Receber por e-mail"]
            
            for step in steps:
                print(f"👉 Clicando em: {step}")
                target = page.locator(f"text={step}").first
                target.wait_for(state="visible", timeout=20000)
                target.click()
                time.sleep(3) # Pausa técnica necessária para o backend da Conac
            
            print("✅ Sucesso! O boleto foi solicitado para o e-mail.")

        except Exception as e:
            print(f"❌ Erro detectado: {e}")
            # Tira um print do erro para o log do GitHub se falhar novamente
            page.screenshot(path="debug_screenshot.png")
            raise e
        finally:
            browser.close()

if __name__ == "__main__":
    run()
