import os
import time
import requests
from playwright.sync_api import sync_playwright

def enviar_telegram(caminho_pdf):
    token = os.environ['TELEGRAM_TOKEN']
    chat_id = os.environ['TELEGRAM_CHAT_ID']
    
    url = f"https://api.telegram.org/bot{token}/sendDocument"
    caption = "📄 *Seu Boleto Conac do Mês Chegou!*"
    
    print("📤 Enviando boleto para o Telegram...")
    with open(caminho_pdf, "rb") as file:
        payload = {"chat_id": chat_id, "caption": caption, "parse_mode": "Markdown"}
        files = {"document": file}
        response = requests.post(url, data=payload, files=files)
        
    if response.status_code == 200:
        print("✨ Boleto enviado com sucesso no Telegram!")
    else:
        print(f"❌ Falha ao enviar no Telegram: {response.text}")
        raise Exception("Erro no envio do Telegram")

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()
        
        try:
            print("🚀 Acessando portal de login da Conac...")
            page.goto("https://conac.com.br/login-area-do-cliente/", wait_until="domcontentloaded", timeout=120000)
            
            # Aguarda renderização dos componentes/iframes dinâmicos
            time.sleep(5)
            
            print("🔢 Procurando campo de CPF nos frames...")
            input_cpf = None
            
            # Procura em todos os frames/iframes carregados na página
            for frame in page.frames:
                loc = frame.locator("input[type='text'], input[placeholder*='CPF' i], input[name*='cpf' i], input:visible").first
                if loc.count() > 0:
                    input_cpf = loc
                    break
            
            if not input_cpf:
                input_cpf = page.locator("input[type='text'], input:visible").first

            input_cpf.wait_for(state="visible", timeout=45000)
            input_cpf.fill(os.environ['CONAC_CPF'])
            
            print("🔘 Clicando em Entrar...")
            btn_entrar = None
            for frame in page.frames:
                loc = frame.locator("text=Entrar").first
                if loc.count() > 0:
                    btn_entrar = loc
                    break
            
            if not btn_entrar:
                btn_entrar = page.locator("text=Entrar").first
                
            btn_entrar.click()
            
            print("📋 Clicando em Abrir boleto...")
            btn_abrir_boleto = None
            for frame in page.frames:
                loc = frame.locator("text=Abrir boleto").first
                if loc.count() > 0:
                    btn_abrir_boleto = loc
                    break
                    
            if not btn_abrir_boleto:
                btn_abrir_boleto = page.locator("text=Abrir boleto").first

            btn_abrir_boleto.wait_for(state="visible", timeout=60000)
            btn_abrir_boleto.click()
            
            print("📥 Aguardando download do PDF...")
            with page.expect_download(timeout=90000) as download_info:
                btn_abrir_pdf = None
                for frame in page.frames:
                    loc = frame.locator("text=Abrir PDF").first
                    if loc.count() > 0:
                        btn_abrir_pdf = loc
                        break
                        
                if not btn_abrir_pdf:
                    btn_abrir_pdf = page.locator("text=Abrir PDF").first

                btn_abrir_pdf.wait_for(state="visible", timeout=60000)
                btn_abrir_pdf.click()
                
            download = download_info.value
            caminho_pdf = "boleto_conac.pdf"
            download.save_as(caminho_pdf)
            print(f"✅ Download concluído: {caminho_pdf}")
            
            enviar_telegram(caminho_pdf)

        except Exception as e:
            print(f"❌ Erro durante o processo: {e}")
            page.screenshot(path="erro_execucao.png")
            raise e
        finally:
            browser.close()

if __name__ == "__main__":
    run()
