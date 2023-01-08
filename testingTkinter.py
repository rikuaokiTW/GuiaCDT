from tkinter import *

dado1 = 2
dado2 = 3
# Funções
def altDados(new_dado1, new_dado2):
    global dado1, dado2
    dado1 = new_dado1
    dado2 = new_dado2
    print(dado1, dado2)

def showDado():
    print(dado1, dado2)
    
# Referente a metadata
interface = Tk()
interface.title("Automatizador do Trovão")

# Dimensao da janela do aplicativo
dj = (500, 300)
# Resolucao do Monitor
rm = (interface.winfo_screenwidth(), interface.winfo_screenheight())
# Posicao da Janela do Aplicativo
pj = (rm[0]/2 - dj[0]/2, rm[1]/2 - dj[1]/2)

interface.geometry("{}x{}+{}+{}".format(dj[0], dj[1], int(pj[0]), int(pj[1])))

"""
Label(root,
    fg = cor da fonte, bg = cor do fundo, font = fonte/tamanho/weight/style
    width=20 (tamanho como tamanho de fonte, em função do caractere, com borda corta)
    height=2 (número de linhas) anchor=NW/N/NE/E/SE/S/SW/W/CENTER
    padx=20, pady=20 (Padding esquerda/direita e superior/inferior, é em pixel)
    justify=CENTER/LEFT/RIGHT (possível misturar justify e anchor)
    textvariable = var (pega o valor de uma variável, o valor de StringVar())
    qualquer.grid(row = 0, column = 0, sticky=W) - alternativa a .pack()
    sticky=NW/N/NE/E/SE/S/SW/W/CENTER 'we'(alinhamento perante a row/col do grid)
    columnspan=2 (do grid, define quantas colunas elemento ocupa)
    Possível 1: label['propriedade'] = "novo_valor"
    Possível 2: alterar texto dps de já usado o comando ".pack" usando o possível 1
    borderwidth/bd=1    relief = "solid/groove/flat/raised/sunken/ridge"
    NameVarImg = PhotoImage(file="path") image=NameVarImg (adicionar imagem 1)
    ex: img = PhotoImage(file="Images/imagem.png") // la_I=Label(root, image=img).pack()

Entry(root,
    Permite input do usuário
    .grid()
    .focus()

Button(root,
    botão
    .grid
    command=lambda name_function/comando (executa uma função ou comando)

Criar Frame:
    1. O frame é definido através de "nameFrame = Frame(root)"
    2. Os demais itens que serão pertencentes a esse frame deixam de serem
        iniciados através de "widget(root)" e passam a ter o nome do frame
        no lugar do "root"
    Ex: nameFrame = Frame(root) \n nameWidget = Widget(nameFrame)

CheckButton:
    valor_check = IntVar()
    check = CheckButton(root, text="Está é checkbox").pack()

    ## Possibilidade pro teste
    def apresentar():
        print(valor_check.get())
    valor_check = IntVar()
    check = CheckButton(root, text="Teste", variable=valor_check,
        command=apresentar).pack()

    ## Isso faz apresentar 0 e 1 alternadamente, logo dá pra fzr
    
"""

# Referente ao que aparece dentro
btn = Button(interface, text = "Aplicar", command=lambda: altDados("sim", "sim"))
btn.pack()

btn2 = Button(interface, text = "Show Original", command=lambda: showDado())
btn2.pack()
# Execução
interface.mainloop()
