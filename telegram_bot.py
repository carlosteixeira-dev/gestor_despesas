import os
import requests
from sheets_manager import obter_resumo_mes_anterior

try:
    from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
    os.environ["TELEGRAM_TOKEN"] = TELEGRAM_TOKEN
    os.environ["TELEGRAM_CHAT_ID"] = TELEGRAM_CHAT_ID
except ImportError:
    pass

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

def enviar_mensagem(texto: str) -> bool:
    """
    Envia uma mensagem para o Telegram.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": texto,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }

    try:
        resposta = requests.post(url, data=payload, timeout=10)
        if resposta.status_code == 200:
            print("✅ Resumo enviado para o Telegram!")
            return True
        else:
            print(f"❌ Erro: {resposta.status_code} - {resposta.text}")
            return False
    except Exception as erro:
        print(f"❌ Erro de ligação: {erro}")
        return False


def formatar_resumo(resumo: dict) -> str:
    """
    Formata o resumo mensal para o Telegram.
    """
    if not resumo or not resumo.get("despesas"):
        return "📊 Sem despesas registadas no mês anterior."

    mes = resumo["mes"]
    despesas = resumo["despesas"]
    total = resumo["total"]

    linhas = [
        f"💰 <b>RESUMO DE DESPESAS — {mes}</b>",
        "━━━━━━━━━━━━━━━━━━━━━━",
        ""
    ]

    for categoria, valor in despesas.items():
        linhas.append(f"• {categoria}: <b>{valor:.2f} €</b>")

    linhas.append("")
    linhas.append("━━━━━━━━━━━━━━━━━━━━━━")
    linhas.append(f"💳 <b>TOTAL: {total:.2f} €</b>")

    return "\n".join(linhas)


def enviar_resumo_mensal() -> None:
    """
    Obtém o resumo do mês anterior e envia para o Telegram.
    """
    print("💰 A enviar resumo mensal de despesas...\n")

    resumo = obter_resumo_mes_anterior()
    mensagem = formatar_resumo(resumo)

    print(mensagem)
    enviar_mensagem(mensagem)

    print("\n🏁 Concluído!")


if __name__ == "__main__":
    enviar_resumo_mensal()