"""
sheets_manager.py
-----------------
Gere o Google Sheets onde são guardadas as despesas.
Usa OAuth2 para autenticar com o Google.

Bibliotecas usadas:
- gspread          : para ler e escrever no Google Sheets
- google-auth      : para autenticar com OAuth2
"""

import gspread
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import pickle
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta

# ID da Google Sheet
SHEET_ID = "1JjMagLTvc1A8GZ4buwokXjlkCqiOoC4_MXdPnb49uoQ"

# ficheiro de token
TOKEN_FILE = "token.pickle"

# meses em português
MESES_PT = {
    "January": "Janeiro", "February": "Fevereiro", "March": "Março",
    "April": "Abril", "May": "Maio", "June": "Junho",
    "July": "Julho", "August": "Agosto", "September": "Setembro",
    "October": "Outubro", "November": "Novembro", "December": "Dezembro"
}


def mes_pt(data: datetime) -> str:
    """Devolve o nome do mês em português. Ex: 'Junho 2026'"""
    mes_en = data.strftime("%B")
    return f"{MESES_PT[mes_en]} {data.year}"


def obter_cliente() -> gspread.Client:
    """
    Autentica com o Google e devolve o cliente gspread.
    """
    creds = None

    # carrega o token guardado
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)

    # renova o token se necessário
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)

    return gspread.authorize(creds)


def obter_ou_criar_folha(spreadsheet, mes_ano: str):
    """
    Obtém ou cria uma folha para o mês indicado.
    """
    try:
        return spreadsheet.worksheet(mes_ano)
    except gspread.WorksheetNotFound:
        # cria folha nova
        ws = spreadsheet.add_worksheet(title=mes_ano, rows=100, cols=4)

        # cabeçalhos
        ws.update(values=[["Categoria", "Valor (€)", "Data", "Tipo"]], range_name="A1:D1")

        # formata cabeçalho
        ws.format("A1:D1", {
            "backgroundColor": {"red": 0.18, "green": 0.52, "blue": 0.67},
            "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
            "horizontalAlignment": "CENTER"
        })

        return ws


def guardar_despesas_sheets(despesas: dict) -> bool:
    """
    Guarda as despesas no Google Sheets.
    """
    try:
        cliente = obter_cliente()
        spreadsheet = cliente.open_by_key(SHEET_ID)

        agora = datetime.now()
        mes_ano = mes_pt(agora)
        data_hoje = agora.strftime("%d/%m/%Y")

        ws = obter_ou_criar_folha(spreadsheet, mes_ano)

        # encontra próxima linha vazia
        valores = ws.get_all_values()
        proxima_linha = len(valores) + 1

        # despesas fixas
        FIXAS = [
            "Renda", "Prestação do Carro", "Luz", "Água", "Gás",
            "Seguro de Saúde", "Seguro do Carro", "Telemóvel/Internet",
            "Escola/Creche", "Subscrições"
        ]

        linhas = []
        for categoria, valor in despesas.items():
            if valor and valor > 0:
                tipo = "Fixa" if categoria in FIXAS else "Variável"
                linhas.append([categoria, valor, data_hoje, tipo])

        print(f"DEBUG: {len(linhas)} linhas a guardar: {linhas}")

        if linhas:
            ws.update(values=linhas, range_name=f"A{proxima_linha}")

        print(f"✅ Despesas guardadas no Google Sheets!")
        return True

    except Exception as erro:
        print(f"❌ Erro ao guardar no Sheets: {erro}")
        return False


def obter_resumo_mes_anterior() -> dict:
    """
    Lê o Google Sheets e devolve o resumo do mês anterior.
    """
    try:
        cliente = obter_cliente()
        spreadsheet = cliente.open_by_key(SHEET_ID)

        # calcula o mês anterior
        mes_anterior = datetime.now() - relativedelta(months=1)
        nome_mes = mes_pt(mes_anterior)

        try:
            ws = spreadsheet.worksheet(nome_mes)
        except gspread.WorksheetNotFound:
            return {"mes": nome_mes, "despesas": {}, "total": 0.0}

        registos = ws.get_all_records()
        despesas = {}
        total = 0.0

        for registo in registos:
            categoria = registo.get("Categoria", "")
            valor = registo.get("Valor (€)", 0)

            if categoria and valor:
                try:
                    valor = float(str(valor).replace(",", ".").replace("€", "").strip())
                    if categoria in despesas:
                        despesas[categoria] += valor
                    else:
                        despesas[categoria] = valor
                    total += valor
                except:
                    pass

        return {
            "mes": nome_mes,
            "despesas": despesas,
            "total": total
        }

    except Exception as erro:
        print(f"❌ Erro ao ler resumo: {erro}")
        return {}


if __name__ == "__main__":
    despesas_teste = {
        "Renda": 500.0,
        "Luz": 45.0,
        "Compras": 120.0
    }
    guardar_despesas_sheets(despesas_teste)
