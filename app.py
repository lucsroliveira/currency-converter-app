import tkinter as tk
from tkinter import ttk, messagebox
import requests

MOEDAS_DISPONIVEIS = {
    "Dólar (USD)": "USD",
    "Euro (EUR)": "EUR",
    "Bitcoin (BTC)": "BTC",
    "Ethereum (ETH)": "ETH",
    "Peso Argentino (ARS)": "ARS",
    "Iene Japonês (JPY)": "JPY"
}


def obter_cotacao(moeda_base, moeda_destino):
    par = f"{moeda_base}-{moeda_destino}"
    url = f"https://economia.awesomeapi.com.br/json/last/{par}"

    try:
        resposta = requests.get(url)
        dados = resposta.json()
        par = moeda_base + moeda_destino
        return float(dados[par.replace("-","")]['bid'])
    except Exception as e:
        messagebox.showerror("Erro",  f"Nao foi possível obter a cotação.\n{e}")
        return None

def converter():
    moeda_destino = moeda_var.get()
    simbolo = MOEDAS_DISPONIVEIS[moeda_destino]

    try:
        valor_brl = float(entrada_valor.get())
    except ValueError:
        messagebox.showwarning("Entrada inválida", "Digite um valor numérico válido")
        return

    if simbolo in ["BTC","ETH"]:
        taxa = obter_cotacao(simbolo,"BRL")
        if taxa:
            valor_convertido = valor_brl / taxa
            resultado_texto.set(
                f"R$ {valor_brl:.2f} equivale a:\n"
                f"{valor_convertido:.8f} {simbolo} (Cotação: R$ {taxa:.2f})"
            )
    else:
        taxa = obter_cotacao("BRL", simbolo)
        if taxa:
            valor_convertido = valor_brl * taxa
            resultado_texto.set(
                f"R$ {valor_brl:.2f} equivale a:\n"
                f"{valor_convertido:.2f} {simbolo} (Cotação: {taxa:.3f})"
            )

#Interface
janela = tk.Tk()
janela.title("Conversor de Moeda")
janela.geometry("430x330")
janela.resizable(False, False)

tk.Label(janela,text="Digite o valor em Reais (BRL): ", font=("Arial", 12)).pack(pady=10)
entrada_valor = tk.Entry(janela,font=("Arial", 14), justify="center")
entrada_valor.pack(pady=5)

tk.Label(janela,text="Escolha a moeda de destino: ",  font=("Arial", 12)).pack(pady=5)
moeda_var = tk.StringVar(value=list(MOEDAS_DISPONIVEIS.keys())[0])
dropdown = ttk.Combobox(janela, textvariable=moeda_var, values=list(MOEDAS_DISPONIVEIS.keys()), state="readonly", font=("Arial", 12), justify="center")
dropdown.pack(pady=5)

tk.Button(janela, text="Converter", font=("Arial", 12), command=converter).pack(pady=10)

resultado_texto = tk.StringVar()
tk.Label(janela, textvariable=resultado_texto, font=("Arial", 12), justify="center", wraplength=380).pack(pady=10)

janela.mainloop()