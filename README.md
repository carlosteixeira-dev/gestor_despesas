# 💰 Gestor de Despesas

Dashboard para registar e monitorizar despesas mensais, com sincronização automática para Excel e Google Sheets, e resumo mensal enviado para o Telegram.

---

## 📁 Estrutura do projeto
gestor_despesas/
├── main.py              # Ponto de entrada
├── dashboard.py         # Interface gráfica (CustomTkinter)
├── excel_manager.py     # Guarda despesas no Excel local
├── sheets_manager.py    # Sincroniza com Google Sheets
├── telegram_bot.py      # Envia resumo para o Telegram
├── config.py            # Configurações (não vai para o GitHub)
├── requirements.txt     # Dependências
└── .github/
└── workflows/
└── resumo_mensal.yml  # Envia resumo no dia 1 de cada mês

---

## ⚙️ Como configurar

### 1. Clonar o repositório
```bash
git clone https://github.com/carlosteixeira-dev/gestor_despesas.git
cd gestor_despesas
```

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Configurar o ficheiro config.py
Cria um ficheiro `config.py` (não commites este ficheiro!):
```python
SHEET_ID = "o-teu-google-sheets-id"
TELEGRAM_TOKEN = "o-teu-token"
TELEGRAM_CHAT_ID = "o-teu-chat-id"
```

### 4. Configurar Google Sheets
- Cria um projeto na [Google Cloud Console](https://console.cloud.google.com/)
- Ativa a API do Google Sheets
- Gera um token com `python gerar_token.py`

### 5. Testar localmente
```bash
python main.py
```

---

## 🤖 GitHub Actions

Adiciona os seguintes secrets no repositório (Settings → Secrets → Actions):

| Secret | Descrição |
|--------|-----------|
| `TELEGRAM_TOKEN` | Token do bot do Telegram |
| `TELEGRAM_CHAT_ID` | O teu chat ID |
| `GOOGLE_TOKEN` | Token OAuth do Google |
| `SHEET_ID` | ID do Google Sheets |

O resumo é enviado automaticamente no **dia 1 de cada mês às 8h**.

---

## 🛠️ Stack

- Python 3.11
- CustomTkinter — interface gráfica
- openpyxl — Excel local
- gspread — Google Sheets
- requests — Telegram API
- GitHub Actions — automação gratuita
