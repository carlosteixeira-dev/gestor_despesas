"""
main.py
-------
Ponto de entrada para o envio automático do resumo mensal.
Corre no dia 1 de cada mês via GitHub Actions.
"""

from telegram_bot import enviar_resumo_mensal

if __name__ == "__main__":
    enviar_resumo_mensal()