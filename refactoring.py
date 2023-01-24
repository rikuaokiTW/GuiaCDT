from tkinter import *
from tkinter import filedialog
from tkinter.tix import *
from PIL import Image, ImageDraw, ImageFont
import re, os

class FileVerification():
    def __init__(self):
        self.extensionRegex = re.compile(r'[^.]+$')

    def isImage(self, pathImage):
        if os.path.isfile(pathImage):
            extension = self.extensionRegex.search(pathImage).group()
            if extension == 'png':
                return True
            else:
                return False

    def isText(self, pathText):
        if os.path.isfile(pathText):
            extension = self.extensionRegex.search(pathText).group()
            if extension == 'txt':
                return True
            else:
                return False

    def isFont(self, pathFont):
        if os.path.isfile(pathFont):
            extension = self.extensionRegex.search(pathFont).group()
            if extension == 'otf' or extension == 'ttf':
                return True
            else:
                return False
    
    def isDirectory(self, pathDirectory):
        if os.path.isdir(pathDirectory):
            return True
        else:
            return False

class VisualWarning(Label, Balloon):
    def __init__(self, master, pathImage, row, column):
        super().__init__()
        self.__master = master
        self.__image = PhotoImage(file=pathImage)
        self._row = row
        self._column = column

        self.__warning = Label(self.__master, image=self.__image)
        self.__warning.grid(row=self._row, column=self._column)
        #self.__warning.columnconfigure(self._column, weight=0)
        
        self.__balloonWarning = Balloon(self.__master)
        self.__balloonWarning.bind_widget(self.__warning, balloonmsg="Path não identificado")

    def setImage(self, newImage):
        self.__image = PhotoImage(file=newImage)
        self.__warning.configure(image=self.__image)
        self.__warning.image = self.__image

    def setMessage(self, newMessage):
        self.__balloonWarning.bind_widget(self.__warning, balloonmsg=newMessage)

class Title(Label):
    def __init__(self, master, name, row, column, columnspan = 1, sticky = 'W'):
        super().__init__()
        self.__master = master
        self.name = name
        self._row = row
        self._column = column
        self._columnspan = columnspan
        self.sticky = sticky

        self.label = Label(self.__master, text=self.name)
        self.label.grid(row=self._row, column=self._column, columnspan=self._columnspan, sticky=EW)
        self.label.bind("<Configure>", self.setSize)
        #self.label.columnconfigure(self._column, weight=2)
    
    def setSize(self, event):
        if event.width < 70:
            font_size = int(event.width/7)
            #print("caso 1: ", font_size, event.width, self.label.cget("text"))
        elif event.width >= 70 and event.width < 80:
            font_size = int(event.width/8)
            #print("caso 2: ", font_size, event.width, self.label.cget("text"))
        elif event.width >= 80 and event.width < 90:
            font_size = int(event.width/9)
            #print("caso 3: ", font_size, event.width, self.label.cget("text"))
        elif event.width >= 90 and event.width < 110:
            font_size = int(event.width/10)
            #print("caso 4: ", font_size, event.width, self.label.cget("text"))
        elif event.width >= 110 and event.width < 150:
            font_size = int(event.width/11)
            #print("caso 5: ", font_size, event.width, self.label.cget("text"))
        elif event.width >= 150:
            font_size = 14
            #print("caso 6: ", font_size, event.width, self.label.cget("text"))
        self.label.configure(font=("Arial", font_size))


class Input(Entry):
    def __init__(self, master, width, row, column, textDefault = ''):
        super().__init__()
        self.__master = master
        self._width = width
        self._row = row
        self._column = column
        self.verification = FileVerification()
        
        self.input = Entry(self.__master, width=self._width)
        self.input.grid(row=self._row, column=self._column, sticky=EW)
        #self.input.columnconfigure(self._column, weight=3)
        self.setText(textDefault)

    def getValue(self):
        return self.input.get()

    def setText(self, text):
        self.clearText()
        self.input.insert(0, text)
    
    def clearText(self):
        self.input.delete(0, END)

class SearchButton(Button):
    def __init__(self, master, text, padx, pady, inputIndex, row, column,bgColor='lightgray', bgActive="gray"):
        super().__init__()
        self.__master = master
        self.row = row
        self.column = column
        self.text = text
        self.padx = padx
        self.pady = pady

        self.searchButton = Button(self.__master, text=self.text, bg=bgColor, activebackground=bgActive, padx=self.padx, pady=self.pady, command=lambda: inputs[inputIndex]['input'].setText(self.getFileName()))
        self.searchButton.grid(row=self.row, column=self.column)
        #self.searchButton.columnconfigure(self.column, weight=1)
    
    def getFileName(self):
        filename = filedialog.askopenfilename(initialdir=os.getcwd(),filetypes = (("*ttf, *otf, *txt, *png files",".txt .png .otf .ttf"),("all files","*.*")))

        return filename

class ActionButton(Button):
    def __init__(self, master, text, bgColor, fontColor, action, row, column, sticky=N, span=1, listInputs=[]):
        self.__master = master
        self._action = action
        self.listInputs = listInputs

        self.actionButton = Button(self.__master, text=text, background=bgColor, fg=fontColor, width="40", font=("Consolas"), bd=2)
        self.setAction()
        self.actionButton.grid(row=row, column=column, columnspan=span, sticky=sticky)
        self.actionButton.grid_columnconfigure(column, weight=0)

    def setAction(self):
        if self._action == 'validar':
            self.actionButton.configure(command=lambda: self.verifyInputs())
        elif self._action == 'limpar':
            self.actionButton.configure(command=lambda: self.clearInputs())

    def verifyInputs(self):
        if self.listInputs:
            for item in self.listInputs:
                if item['type'] == 'image':
                    if item["input"].getValue():
                        if item["input"].verification.isImage(item["input"].getValue()):
                            item["warning"].setImage(r'{}'.format(os.path.join(os.getcwd(), r"src\icons\accept.png")))
                            item["warning"].setMessage("Imagem encontrada!")
                        elif item["input"].verification.isImage(item["input"].getValue()) == None:
                            item["warning"].setImage(r'{}'.format(os.path.join(os.getcwd(), r"src\icons\cancel.png")))
                            item["warning"].setMessage("Esperava algo como C:/path/image.png")
                        elif not item["input"].verification.isImage(item["input"].getValue()):
                            item["warning"].setImage(r'{}'.format(os.path.join(os.getcwd(), r"src\icons\cancel.png")))
                            item["warning"].setMessage("A imagem deve ser .png")
                    else:
                        item["warning"].setImage(r'{}'.format(os.path.join(os.getcwd(), r"src\icons\cancel.png")))
                        item["warning"].setMessage("Path não identificado")

                elif item['type'] == 'font':
                    if item["input"].getValue():
                        if item["input"].verification.isFont(item["input"].getValue()):
                            item["warning"].setImage(r'{}'.format(os.path.join(os.getcwd(), r"src\icons\accept.png")))
                            item["warning"].setMessage("Fonte encontrada!")
                        elif item["input"].verification.isFont(item["input"].getValue()) == None:
                            item["warning"].setImage(r'{}'.format(os.path.join(os.getcwd(), r"src\icons\cancel.png")))
                            item["warning"].setMessage("Esperava algo como C:/path/fonte.ttf")
                        elif not item["input"].verification.isFont(item["input"].getValue()):
                            item["warning"].setImage(r'{}'.format(os.path.join(os.getcwd(), r"src\icons\cancel.png")))
                            item["warning"].setMessage("A fonte deve ser .ttf ou .otf")
                    else:
                        item["warning"].setImage(r'{}'.format(os.path.join(os.getcwd(), r"src\icons\cancel.png")))
                        item["warning"].setMessage("Path não identificado")

                elif item['type'] == 'directory':
                    if item["input"].getValue():
                        if item["input"].verification.isDirectory(item["input"].getValue()):
                            item["warning"].setImage(r'{}'.format(os.path.join(os.getcwd(), r"src\icons\accept.png")))
                            item["warning"].setMessage("Pasta encontrada!")
                        elif item["input"].verification.isDirectory(item["input"].getValue()) == None:
                            item["warning"].setImage(r'{}'.format(os.path.join(os.getcwd(), r"src\icons\cancel.png")))
                            item["warning"].setMessage("Esperava algo como C:/path/pasta/")
                        elif not item["input"].verification.isDirectory(item["input"].getValue()):
                            item["warning"].setImage(r'{}'.format(os.path.join(os.getcwd(), r"src\icons\cancel.png")))
                            item["warning"].setMessage("Não é uma pasta")

                elif item['type'] == 'text':
                    if item["input"].getValue():
                        if item["input"].verification.isText(item["input"].getValue()):
                            item["warning"].setImage(r'{}'.format(os.path.join(os.getcwd(), r"src\icons\accept.png")))
                            item["warning"].setMessage("Texto encontrado!")
                        elif item["input"].verification.isText(item["input"].getValue()) == None:
                            item["warning"].setImage(r'{}'.format(os.path.join(os.getcwd(), r"src\icons\cancel.png")))
                            item["warning"].setMessage("Esperava algo como C:/path/texto.txt")
                        elif not item["input"].verification.isText(item["input"].getValue()):
                            item["warning"].setImage(r'{}'.format(os.path.join(os.getcwd(), r"src\icons\cancel.png")))
                            item["warning"].setMessage("Deve ser um arquivo .txt")
                            
                    else:
                        item["warning"].setImage(r'{}'.format(os.path.join(os.getcwd(), r"src\icons\cancel.png")))
                        item["warning"].setMessage("Path não identificado")
        else:
            pass
    
    def clearInputs(self):
        for item in self.listInputs:
            item['input'].clearText()

#--------------------------------------------------------------------------
# Início
root = Tk()
root.title("Automatizando o Guia")

#--------------------------------------------------------------------------
# Dimensao da janela do aplicativo
dj = (500, 300)
# Resolucao do Monitor
rm = (root.winfo_screenwidth(), root.winfo_screenheight())
# Posicao da Janela do Aplicativo
pj = (rm[0]/2 - dj[0]/2, rm[1]/2 - dj[1]/2)
# Centralizando a Janela com relação ao monitor
root.geometry("{}x{}+{}+{}".format(dj[0], dj[1], int(pj[0]), int(pj[1])))
#---------------------------------------------------------------------------
# Definindo Frame de Entrada de Dados
input_frame = Frame(root, width=dj[0], padx=5, pady=5, bd=3, relief="groove")

# Colocando Entrada de Paths de Arquivos
inputs = [
    {
        "type": 'image', 
        "label":Title(input_frame, "Imagem Base:", 0, 1),
        "input":Input(input_frame, "50", 0, 2, r'{}'.format(os.path.join(os.getcwd(), r"src\images\test-cdt.png"))),
        "warning":VisualWarning(input_frame, r'{}'.format(os.path.join(os.getcwd(), r"src\icons\cancel.png")), 0, 0),
        "button":SearchButton(input_frame, "...", 4, 2, 0, 0, 3),
    },
    {
        "type": 'font',
        "label":Title(input_frame, "Fonte Principal:", 1, 1),
        "input":Input(input_frame, "50", 1, 2),
        "warning":VisualWarning(input_frame, r'{}'.format(os.path.join(os.getcwd(), r"src\icons\cancel.png")), 1, 0),
        "button":SearchButton(input_frame, "...", 4, 2, 1, 1, 3),
    },
    {
        "type": 'font',
        "label":Title(input_frame, "Fonte com Itálico:", 2, 1),
        "input":Input(input_frame, "50", 2, 2),
        "warning":VisualWarning(input_frame, r'{}'.format(os.path.join(os.getcwd(), r"src\icons\cancel.png")), 2, 0),
        "button":SearchButton(input_frame, "...", 4, 2, 2, 2, 3),
    },
    {
        "type": 'directory',
        "label":Title(input_frame, "Local de Destino:", 3, 1),
        "input":Input(input_frame, "50", 3, 2),
        "warning":VisualWarning(input_frame, r'{}'.format(os.path.join(os.getcwd(), r"src\icons\cancel.png")), 3, 0),
        "button":SearchButton(input_frame, "...", 4, 2, 3, 3, 3),
    },
    {
        "type": 'text',
        "label":Title(input_frame, "Info Animes:", 4, 1),
        "input":Input(input_frame, "50", 4, 2),
        "warning":VisualWarning(input_frame, r'{}'.format(os.path.join(os.getcwd(), r"src\icons\cancel.png")), 4, 0),
        "button":SearchButton(input_frame, "...", 4, 2, 4, 4, 3),
    },
]

# Botões
button1 = ActionButton(input_frame, 'VALIDAR', '#7BFF78', '#0D650B', 'validar', 5, 0, span=2, listInputs=inputs)
button2 = ActionButton(input_frame, 'APAGAR', '#FF7878', '#650B0B', 'limpar', 5, 2, span=2, listInputs=inputs)

# Inserindo Frame de Entrada de Dados
input_frame.grid(row=0, column=0, sticky=EW)

#---------------------------------------------------------------------------
# Definindo Frame de Preview da Imagem
preview_frame = Frame(root, width=dj[0], padx=5, pady=5, bd=3, relief="groove")

# Imagem
base_image = PhotoImage(file=os.path.join(os.getcwd(), r'src/images/preview.png'))
image_preview = Label(preview_frame, image=base_image)
image_preview.grid(row=0, column=0)

preview_frame.grid(row=1, column=0, sticky=EW)

#---------------------------------------------------------------------------
# Definindo Frame de Textos de Teste da Imagem
preview_texts = Frame(root, width=dj[0], padx=5, pady=5, bd=3, relief="groove")

# Texto de Teste
# Labels
title_label = Label(preview_texts, text="1. Título:", padx=5)
title_label.grid(row=0, column=0)

# Inputs
title_input = Entry(preview_texts, width="40")
title_input.grid(row=0, column=1, sticky=EW, pady=10)

preview_texts.grid(row=2, column=0, sticky=EW)

#---------------------------------------------------------------------------
# Layout de Ajuste finos
adjust_canvas = Canvas(root, width=dj[0])
adjust_frame = Frame(adjust_canvas)

# Criando Labels
title_label = Label(adjust_frame, text="Título")
title_label.grid(row=0, column=0)

# Frame dos inputs
titles_frame = Frame(adjust_frame, bg="gray", padx=10, pady=10, bd=3)


# Criando label das coordenadas
font_height_label = Label(titles_frame, text="font size")
font_height_label.grid(row=0, column=0)
coordx_label = Label(titles_frame, text="coordx")
coordx_label.grid(row=1, column=0)
coordy_label = Label(titles_frame, text="coordy")
coordy_label.grid(row=2, column=0)

# Criando inputs dos titulos
font_height_input = Entry(titles_frame)
font_height_input.grid(row=0, column=1)
coordx_input = Entry(titles_frame)
coordx_input.grid(row=1, column=1)
coordy_input = Entry(titles_frame)
coordy_input.grid(row=2, column=1)

# Fechando Frame dos Inputs
titles_frame.grid(row=1, column=0)

# Barra de Scroll
scrollbar = Scrollbar(root, orient='vertical')
scrollbar.grid(row=0, column=1, sticky=NS)

# Configurando o comando da scrollbar para controlar o scroll do canva
scrollbar.config(command = adjust_canvas.yview)

# Configurando scroll pra controlar a área vertical
#root.config(yscrollcommand=scrollbar.set)
adjust_canvas['yscrollcommand'] = scrollbar.set

# Conectar a barra de rolagem ao evento/área que você quer rolar
adjust_canvas.bind('<Configure>', lambda event: adjust_canvas.configure(scrollregion = adjust_canvas.bbox("all")))

# Adicionando o adjust_frame ao canva para habilitar o scroll
adjust_canvas.create_window((0,0), window=adjust_frame, anchor=NE)

adjust_canvas.grid(row=3, column=0, sticky=EW)

#---------------------------------------------------------------------------
# Acionar Preview
def add_it():
    # Abrindo a imagem
    preview_image = Image.open(os.path.join(os.getcwd(), r'src/images/preview.png'))
    
    # Pegando o texto pra adicionar
    text_to_add = title_input.get()

    # Coordenadas adaptadas pra preview
    preview_font_height = round((int(font_height_input.get()) / 1080) * 300)
    preview_coordx = (int(coordx_input.get()) / 1920) * 523
    preview_coordy = (int(coordy_input.get()) / 1080) * 300

    # Definindo a fonte
    text_font = ImageFont.truetype(os.path.join(os.getcwd(), r'src/fonts/coolvetica rg.otf'), preview_font_height)

    # Editando a imagem
    preview_image_edit = ImageDraw.Draw(preview_image)
    preview_image_edit.text((preview_coordx, preview_coordy), text_to_add, anchor="mm", font=text_font)

    # Salvando a imagem
    preview_image.save(os.path.join(os.getcwd(), r'src/images/new_preview.png'))

    # Limpe a entry box
    title_input.delete(0, END)
    title_input.insert(0, "Saving File...")

    # Espere alguns segundos e mostre a imagem
    image_preview.after(2000, show_pic(os.path.join(os.getcwd(), r'src/images/new_preview.png')))

def show_pic(pathNewPic):
    global new_preview
    new_preview = PhotoImage(file=pathNewPic)
    image_preview.config(image=new_preview)
    title_input.delete(0, END)

buttonDemo = Button(root, text="Demonstração", command=lambda: add_it())
buttonDemo.grid(row=4, column=0, sticky=EW)



""" # Barra de Scroll
scrollbar = Scrollbar(root, orient='vertical')
scrollbar.grid(row=0, column=1, sticky=NS)

# Configurando o comando da scrollbar para controlar o scroll do canva
scrollbar.config(command = parent_canvas.yview)

# Configurando scroll pra controlar a área vertical
#root.config(yscrollcommand=scrollbar.set)
parent_canvas['yscrollcommand'] = scrollbar.set

# Conectar a barra de rolagem ao evento/área que você quer rolar
parent_canvas.bind('<Configure>', lambda event: parent_canvas.configure(scrollregion = parent_canvas.bbox("all")))

# Adicionando o parent_frame ao canva para habilitar o scroll
parent_canvas.create_window((0,0), window=parent_frame, anchor=NE)


parent_canvas.grid(row=0, column=0, sticky=NSEW) 
parent_canvas.bind("<Configure>", on_resize) """
adjust_canvas.grid_columnconfigure(0, weight=1)
# Responsividade
input_frame.grid_columnconfigure([0,3], weight=0)
input_frame.grid_columnconfigure(1, weight=1)
input_frame.grid_columnconfigure(2, weight=3)
input_frame.grid_rowconfigure([0,1,2,3,4], pad=10)
preview_frame.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

root.mainloop()