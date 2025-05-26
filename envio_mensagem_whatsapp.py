import pywhatkit
import time

def enviar_mensagem_whatsapp():
    """Envia mensagem instantânea via WhatsApp Web usando PyWhatKit"""

    try:
        numero_destino = '+5562984099756'
        mensagem = '🚀 Mensagem enviada por Python usando PyWhatKit!'

        if not numero_destino.startswith('+'):
            raise ValueError("Número deve começar com '+' e código do país!")
        
        print("⚠️ ATENÇÃO: Mantenha o WhatsApp Web aberto no navegador!")
  
        pywhatkit.send_message(numero_destino, mensagem)
        print("✅ Mensagem enviada com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao enviar mensagem: {str(e)}")
        print("Verifique:")
        print("- Conexão com internet")
        print("- Número no formato internacional (+5511123456789)")
        print("- WhatsApp Web aberto e logado")

if __name__ == "__main__":
    enviar_mensagem_whatsapp()