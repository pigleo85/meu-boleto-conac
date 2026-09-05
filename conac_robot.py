import os
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
            page.goto("https://conac.com.br/login-area-do-cliente/", wait_until="domcontentloaded", timeout=90000)
            
            print("🔢 Digitando CPF...")
            input_cpf = page.locator("input[type='text'], input:visible").first
            input_cpf.wait_for(state="visible", timeout=30000)
            input_cpf.fill(os.environ['CONAC_CPF'])
            
            print("🔘 Clicando em Entrar...")
            btn_entrar = page.locator("text=Entrar").first
            btn_entrar.click()
            
            print("📋 Clicando em Abrir boleto...")
            btn_abrir_boleto = page.locator("text=Abrir boleto").first
            btn_abrir_boleto.wait_for(state="visible", timeout=30000)
            btn_abrir_boleto.click()
            
            print("📥 Aguardando download do PDF...")
            with page.expect_download() as download_info:
                btn_abrir_pdf = page.locator("text=Abrir PDF").first
                btn_abrir_pdf.wait_for(state="visible", timeout=30000)
                btn_abrir_pdf.click()
                
            download = download_info.value
            caminho_pdf = "boleto_conac.pdf"
            download.save_as(caminho_pdf)
            print(f"✅ Download concluído: {caminho_pdf}")
            
            # Envia o arquivo diretamente para o Telegram
            enviar_telegram(caminho_pdf)

        except Exception as e:
            print(f"❌ Erro durante o processo: {e}")
            raise e
        finally:
            browser.close()

if __name__ == "__main__":
    run()
