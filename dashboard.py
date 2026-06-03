"""
dashboard.py
------------
Dashboard gráfico para gerir despesas mensais.
Guarda as despesas num ficheiro Excel.
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from excel_manager import (
    guardar_despesas,
    obter_total_mes,
    DESPESAS_FIXAS,
    DESPESAS_VARIAVEIS
)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# meses em português
MESES_PT = {
    "January": "Janeiro", "February": "Fevereiro", "March": "Março",
    "April": "Abril", "May": "Maio", "June": "Junho",
    "July": "Julho", "August": "Agosto", "September": "Setembro",
    "October": "Outubro", "November": "Novembro", "December": "Dezembro"
}

app = ctk.CTk()
app.title("💰 Gestor de Despesas")
app.geometry("600x750")

# --- TÍTULO ---
titulo = ctk.CTkLabel(app, text="💰 GESTOR DE DESPESAS", font=("Arial", 20, "bold"))
titulo.pack(pady=10)

# --- MÊS ATUAL ---
mes_en = datetime.now().strftime("%B")
mes_atual = f"{MESES_PT[mes_en]} {datetime.now().year}"
label_mes = ctk.CTkLabel(app, text=f"📅 {mes_atual}", font=("Arial", 14), text_color="gray")
label_mes.pack(pady=2)

# --- FRAME COM SCROLL ---
frame_scroll = ctk.CTkScrollableFrame(app, width=560, height=520)
frame_scroll.pack(pady=10, padx=10)

# dicionário para guardar os campos de input
campos = {}

# --- DESPESAS FIXAS ---
label_fixas = ctk.CTkLabel(frame_scroll, text="📌 DESPESAS FIXAS", font=("Arial", 14, "bold"))
label_fixas.pack(pady=(10, 5), anchor="w", padx=10)

for despesa in DESPESAS_FIXAS:
    frame_linha = ctk.CTkFrame(frame_scroll, fg_color="transparent")
    frame_linha.pack(fill="x", padx=10, pady=3)

    ctk.CTkLabel(frame_linha, text=despesa, width=220, anchor="w").pack(side="left", padx=5)

    campo = ctk.CTkEntry(frame_linha, width=150, placeholder_text="")
    campo.pack(side="left", padx=5)
    campos[despesa] = campo

# --- DESPESAS VARIÁVEIS ---
label_variaveis = ctk.CTkLabel(frame_scroll, text="🔄 DESPESAS VARIÁVEIS", font=("Arial", 14, "bold"))
label_variaveis.pack(pady=(20, 5), anchor="w", padx=10)

for despesa in DESPESAS_VARIAVEIS:
    frame_linha = ctk.CTkFrame(frame_scroll, fg_color="transparent")
    frame_linha.pack(fill="x", padx=10, pady=3)

    ctk.CTkLabel(frame_linha, text=despesa, width=220, anchor="w").pack(side="left", padx=5)

    campo = ctk.CTkEntry(frame_linha, width=150, placeholder_text="")
    campo.pack(side="left", padx=5)
    campos[despesa] = campo

# --- TOTAL E BOTÕES ---
frame_bottom = ctk.CTkFrame(app, fg_color="transparent")
frame_bottom.pack(pady=5, fill="x", padx=20)

label_total = ctk.CTkLabel(frame_bottom, text="Total: 0.00 €", font=("Arial", 16, "bold"), text_color="green")
label_total.pack(side="left", padx=10)


def calcular_total():
    """Calcula o total dos campos preenchidos."""
    total = 0.0
    for despesa, campo in campos.items():
        valor_str = campo.get().replace("€", "").replace(",", ".").strip()
        try:
            total += float(valor_str)
        except:
            pass
    label_total.configure(text=f"Total: {total:.2f} €")
    return total


def limpar_campos():
    """Limpa todos os campos."""
    for campo in campos.values():
        campo.delete(0, "end")
    label_total.configure(text="Total: 0.00 €")


def guardar():
    """Recolhe os valores e guarda no Excel."""
    despesas = {}
    tem_valores = False

    for despesa, campo in campos.items():
        valor_str = campo.get().replace("€", "").replace(",", ".").strip()
        try:
            valor = float(valor_str)
            if valor > 0:
                despesas[despesa] = valor
                tem_valores = True
        except:
            pass

    if not tem_valores:
        messagebox.showwarning("Aviso", "Introduz pelo menos um valor antes de guardar!")
        return

    sucesso = guardar_despesas(despesas)

    if sucesso:
        total = calcular_total()
        messagebox.showinfo("Guardado!", f"✅ Despesas guardadas com sucesso!\nTotal: {total:.2f} €")
        limpar_campos()
    else:
        messagebox.showerror("Erro", "❌ Erro ao guardar as despesas.")


# botões
ctk.CTkButton(
    frame_bottom,
    text="🧮 Calcular",
    font=("Arial", 13),
    width=120,
    command=calcular_total
).pack(side="left", padx=5)

ctk.CTkButton(
    frame_bottom,
    text="💾 Guardar",
    font=("Arial", 13),
    width=120,
    fg_color="#27AE60",
    command=guardar
).pack(side="left", padx=5)

ctk.CTkButton(
    frame_bottom,
    text="🗑️ Limpar",
    font=("Arial", 13),
    width=120,
    fg_color="#E74C3C",
    command=limpar_campos
).pack(side="left", padx=5)

if __name__ == "__main__":
    app.mainloop()
