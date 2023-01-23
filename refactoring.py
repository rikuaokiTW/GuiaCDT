from tkinter import *
from tkinter import filedialog
from tkinter.tix import *
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
        filename = filedialog.askopenfilename(initialdir=os.getcwd(),filetypes = (("*ttf, *otf, *png files",".png .otf .ttf"),("all files","*.*")))

        return filename

class ActionButton(Button):
    def __init__(self, master, text, bgColor, fontColor, action, row, column, sticky=EW, span=1, listInputs=[]):
        self.__master = master
        self._action = action
        self.listInputs = listInputs

        self.actionButton = Button(self.__master, text=text, background=bgColor, fg=fontColor, font=("Consolas"), bd=2)
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
# Frame de Entrada de Dados
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
    }
]

# Botões
button1 = ActionButton(input_frame, 'VALIDAR', '#7BFF78', '#0D650B', 'validar', 4, 0, span=2, listInputs=inputs)
button2 = ActionButton(input_frame, 'APAGAR', '#FF7878', '#650B0B', 'limpar', 4, 2, span=2, listInputs=inputs)

input_frame.grid(row=0, column=0, sticky=EW)

#---------------------------------------------------------------------------
# Frame de Preview da Imagem

# Responsividade
input_frame.grid_columnconfigure([0,3], weight=0)
input_frame.grid_columnconfigure(1, weight=1)
input_frame.grid_columnconfigure(2, weight=3)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

root.mainloop()
