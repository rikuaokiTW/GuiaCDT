from tkinter import *
from tkinter.tix import *
import os, re

# -------------------------------------------------------------
# Classes
class FramePath(Frame):
    def __init__(self, master, label_name, row_number, column_number):
        super().__init__()
        self.label_name = label_name
        self.row_number = row_number
        self.column_number = column_number

        image = PhotoImage(file=r"C:/Users/Riku Aoki/Documents/Programas/CDT/Image/cancel.png")
        image_item = Label(self)
        image_item.configure(image=image)
        image_item.image = image
        image_item.grid(row=self.row_number, column=self.column_number)
        
        label_item = Label(self, text=self.label_name)
        label_item.grid(row=self.row_number, column=self.column_number + 1, sticky=W)
        
        path_item = Entry(self, width="50")
        path_item.grid(row=self.row_number, column=self.column_number + 2)
        
        tip_item = Balloon(self)
        tip_item.bind_widget(image_item, balloonmsg="Path não identificado")
        

# Funções
def VerificarArquivo(path):
    """
        Verifica se o caminho para cada arquivo está funcional e correto, retornando o necessário
    """
    # Lista com formatos para verificação
    fontes = ['otf', 'ttf']
    # Regex pra testar extensões de arquivo
    extensionRegex = re.compile(r'[^.]+$')

     # Fluxo para verifiicação
    if os.path.isfile(path):
        return True
    else:
        return False

def Atualizar():
    # Imagem Base
    if VerificarArquivo(base_image_path.get()):
        # Imagem
        new_image = PhotoImage(file=r"C:/Users/Riku Aoki/Documents/Programas/CDT/Image/accept.png")
        image_01.configure(image=new_image)
        image_01.image = new_image
        # Balão
        tip_base_image.bind_widget(image_01, balloonmsg = "Arquivo Identificado")
    else:
        # Imagem
        image = PhotoImage(file=r"C:/Users/Riku Aoki/Documents/Programas/CDT/Image/cancel.png")
        image_01.configure(image=image)
        image_01.image = image
        # Balão
        tip_base_image.bind_widget(image_01, balloonmsg = "Não encontro o arquivo '.png'")

    # Fonte Principal
    if VerificarArquivo(principal_font.get()):
        # Imagem
        new_image = PhotoImage(file=r"C:/Users/Riku Aoki/Documents/Programas/CDT/Image/accept.png")
        image_02.configure(image=new_image)
        image_02.image = new_image
        # Balão
        tip_principal_font.bind_widget(image_02, balloonmsg="Arquivo Identificado")
    else:
        # Imagem
        image = PhotoImage(file=r"C:/Users/Riku Aoki/Documents/Programas/CDT/Image/cancel.png")
        image_02.configure(image=image)
        image_02.image = image
        # Balão
        tip_principal_font.bind_widget(image_02, balloonmsg="Não encontro o arquivo '.otf' ou '.ttf'")

    # Fonte Itálico
    if VerificarArquivo(italic_font.get()):
        # Imagem
        new_image = PhotoImage(file=r"C:/Users/Riku Aoki/Documents/Programas/CDT/Image/accept.png")
        image_03.configure(image=new_image)
        image_03.image = new_image
        # Balão
        tip_italic_font.bind_widget(image_03, balloonmsg="Arquivo Identificado")
    else:
        # Imagem
        image = PhotoImage(file=r"C:/Users/Riku Aoki/Documents/Programas/CDT/Image/cancel.png")
        image_03.configure(image=image)
        image_03.image = image
        # Balão
        tip_italic_font.bind_widget(image_03, balloonmsg="Não encontro o arquivo '.otf' ou '.ttf'")
        
    # Pasta de Destino
    if VerificarArquivo(destiny_path.get()):
        # Imagem
        new_image = PhotoImage(file=r"C:/Users/Riku Aoki/Documents/Programas/CDT/Image/accept.png")
        image_04.configure(image=new_image)
        image_04.image = new_image
        # Balão
        tip_destiny_path.bind_widget(image_04, balloonmsg="Arquivo Identificado")
    else:
        # Imagem
        image = PhotoImage(file=r"C:/Users/Riku Aoki/Documents/Programas/CDT/Image/cancel.png")
        image_04.configure(image=image)
        image_04.image = image
        # Balão
        tip_destiny_path.bind_widget(image_04, balloonmsg="Não encontro a pasta")

    # Fonte Negrito
    if VerificarArquivo(bold_font.get()):
        # Imagem
        new_image = PhotoImage(file=r"C:/Users/Riku Aoki/Documents/Programas/CDT/Image/accept.png")
        image_04.configure(image=new_image)
        image_04.image = new_image
        # Balão
        tip_bold_font.bind_widget(image_04, balloonmsg="Arquivo Identificado")
    elif destiny_path.get() == None or destiny_path.get() == '':
        pass
    else:
        # Imagem
        image = PhotoImage(file=r"C:/Users/Riku Aoki/Documents/Programas/CDT/Image/cancel.png")
        image_04.configure(image=image)
        image_04.image = image
        # Balão
        tip_bold_font.bind_widget(image_04, balloonmsg="Não encontro a pasta")

def Negrito():
    if valor_check1.get() == 1:
        pass
    else:
        pass
    if valor_check2.get() == 1:
        pass
    else:
        pass
    if valor_check3.get() == 1:
        pass
    else:
        pass
    

# -------------------------------------------------------------
# Código

def show():
    print(texto.get())

# -------------------------------------------------------------
# GUI
root = Tk()
root.title("Automatizador do Trovão")

# Dimensao da janela do aplicativo
dj = (500, 300)
# Resolucao do Monitor
rm = (root.winfo_screenwidth(), root.winfo_screenheight())
# Posicao da Janela do Aplicativo
pj = (rm[0]/2 - dj[0]/2, rm[1]/2 - dj[1]/2)

root.geometry("{}x{}+{}+{}".format(dj[0], dj[1], int(pj[0]), int(pj[1])))



# -------------------------------------------------------------
# Widgets

path_frame = Frame(root, width=dj[0], padx=5, pady=5, bd=3, relief="groove")

# Definindo Rótulos
label_bimage = Label(path_frame, text="Imagem Base:").grid(row=0, column=1, sticky=W)
label_principal_font = Label(path_frame, text="Fonte Principal:").grid(row=1, column=1, sticky=W)
label_italic_font = Label(path_frame, text="Fonte com Itálico:").grid(row=2, column=1, sticky=W)
label_destiny = Label(path_frame, text="Local de Destino:").grid(row=3, column=1, sticky=W)
label_option = Label(path_frame, text="Opcional:", pady=5).grid(row=4, columnspan=3)
label_bold_font = Label(path_frame, text="Local de Destino:").grid(row=5, column=1, sticky=W)

# Definindo Entradas
base_image_path = Entry(path_frame, width="50")
principal_font = Entry(path_frame, width="50")
italic_font = Entry(path_frame, width="50")
destiny_path = Entry(path_frame, width="50")
bold_font = Entry(path_frame, width="50")

# Organizando Entradas
base_image_path.grid(row=0, column=2)
principal_font.grid(row=1, column=2)
italic_font.grid(row=2, column=2)
destiny_path.grid(row=3, column=2)
bold_font.grid(row=5, column=2)

# Imagens Verificadoras
image = PhotoImage(file=r"C:/Users/Riku Aoki/Documents/Programas/CDT/Image/cancel.png")
optional_image = PhotoImage(file=r"C:/Users/Riku Aoki/Documents/Programas/CDT/Image/add.png")
image_01 = Label(path_frame, image=image)
image_02 = Label(path_frame, image=image)
image_03 = Label(path_frame, image=image)
image_04 = Label(path_frame, image=image)
image_05 = Label(path_frame, image=optional_image)
image_01.grid(row=0, column=0)
image_02.grid(row=1, column=0)
image_03.grid(row=2, column=0)
image_04.grid(row=3, column=0)
image_05.grid(row=5, column=0)

# Balões de Dica
tip_base_image = Balloon(path_frame)
tip_principal_font = Balloon(path_frame)
tip_italic_font = Balloon(path_frame)
tip_destiny_path = Balloon(path_frame)
tip_bold_font = Balloon(path_frame)

# Associando Balões
tip_base_image.bind_widget(image_01, balloonmsg="Path não identificado")
tip_principal_font.bind_widget(image_02, balloonmsg="Path não identificado")
tip_italic_font.bind_widget(image_03, balloonmsg="Path não identificado")
tip_destiny_path.bind_widget(image_04, balloonmsg="Path não identificado")
tip_bold_font.bind_widget(image_05, balloonmsg="Path Opcional")

# CheckButtons
valor_check1 = IntVar()
valor_check2 = IntVar()
valor_check3 = IntVar()
check1 = Checkbutton(path_frame, text="Título", variable=valor_check1)
check2 = Checkbutton(path_frame, text="Nomes Principais", variable=valor_check2, pady=5)
check3 = Checkbutton(path_frame, text="Data de Estreia", variable=valor_check3)

# Colocando os Checkbuttons
check1.grid(row=6, columnspan=3, sticky="we")
check2.grid(row=6, columnspan=3, sticky="w")
check3.grid(row=6, columnspan=3, sticky="e")


path_frame.grid(row=0, column=0)

# Responsividade
path_frame.grid_rowconfigure(0, weight=1)
path_frame.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

base_image_path
principal_font
italic_font
destiny_path
bold_font

texto = Entry(root)
texto.insert(270, '270')
texto.grid(row=1, column=0)
                
Btn = Button(root, text="aperta!" , command=lambda: show())
Btn.grid(row=2, column=0)
Btn = Button(path_frame, text="atualizar" , command=lambda: Atualizar())
Btn.grid(row=7, columnspan=3)

# -------------------------------------------------------------
# Layout



# -------------------------------------------------------------
root.mainloop()

"""
1º Frame - Paths:
    Path de Imagem-Base
    Path de Fontes (normal, negrito e itálico)
    Path de Destino

2º Frame - Preview:
    Label
    Imagem para testes

3º Frame - Ajustes Finos:
    fileira 1:
        title = 2
        genders = 2
    fileira 2:
        studio = 1
        studio_animes = 4
    fileira 3:
        director = 1
        director_animes = 4
    fileira 4:
        composer = 1
        composer_animes = 4
    fileira 5:
        original_source = 1
        platform = 1
        premiere = 1

4º Frame (possivelmente root) - Botão de teste e botão de fazer tudo
"""
