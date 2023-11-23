import tkinter as tk

def mostrar_selecoes():
    resultado = [var.get() for var in variaveis]
    print("Opções selecionadas:", resultado)
    janela.destroy()

# Criar a janela principal
janela = tk.Tk()
janela.title("Selecione as opções")

# Criar variáveis para armazenar o estado das checkboxes
variaveis = [tk.StringVar(value=False) for _ in range(3)]

# Criar checkboxes
for i, texto_opcao in enumerate(["Opção 1", "Opção 2", "Opção 3"]):
    checkbox = tk.Checkbutton(janela, text=texto_opcao, variable=variaveis[i])
    checkbox.pack(anchor='w')

# Botão para mostrar seleções
botao_mostrar = tk.Button(janela, text="Mostrar Seleções", command=mostrar_selecoes)
botao_mostrar.pack()

# Iniciar o loop da interface gráfica
janela.mainloop()
