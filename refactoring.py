from tkinter import *
from tkinter.tix import *
import re, os

class FileVerification():
    def __init__(self):
        self.extensionRegex = re.compile(r'[^.]+$')

    def isImage(self, pathImage):
        if os.path.isfile(pathImage):
            print(pathImage)
            print(os.path.isfile(pathImage))
            extension = self.extensionRegex.search(pathImage).group()
            if extension == 'png':
                print("Passou aqui")
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

        self.Label = Label(self.__master, text=self.name)
        self.Label.grid(row=self._row, column=self._column, columnspan=self._columnspan, sticky=self.sticky)
        

class Input(Entry):
    def __init__(self, master, width, row, column):
        super().__init__()
        self.__master = master
        self.width = width
        self._row = row
        self._column = column
        self.verification = FileVerification()
        
        self.input = Entry(self.__master, width=self.width)
        self.input.grid(row=self._row, column=self._column)

    def getValue(self):
        return self.input.get()

root = Tk()
root.title("Testando")

#--------------------------------------------------------------------------
# Dimensao da janela do aplicativo
dj = (500, 300)
# Resolucao do Monitor
rm = (root.winfo_screenwidth(), root.winfo_screenheight())
# Posicao da Janela do Aplicativo
pj = (rm[0]/2 - dj[0]/2, rm[1]/2 - dj[1]/2)

root.geometry("{}x{}+{}+{}".format(dj[0], dj[1], int(pj[0]), int(pj[1])))
#---------------------------------------------------------------------------
path_frame = Frame(root, width=dj[0], padx=5, pady=5, bd=3, relief="groove")

# Definindo Rótulos
inputs = [
    {
        "label":Title(path_frame, "Imagem Base:", 0, 1),
        "input":Input(path_frame, "50", 0, 2),
        "warning":VisualWarning(path_frame, r'C:/Users/Riku Aoki/Documents/Programas/GuiaCDT/src/icons/cancel.png', 0, 0),
    },
    {
        "label":Title(path_frame, "Fonte Principal:", 1, 1),
        "input":Input(path_frame, "50", 1, 2),
        "warning":VisualWarning(path_frame, r'C:/Users/Riku Aoki/Documents/Programas/GuiaCDT/src/icons/cancel.png', 1, 0),
    },
    {
        "label":Title(path_frame, "Fonte com Itálico:", 2, 1),
        "input":Input(path_frame, "50", 2, 2),
        "warning":VisualWarning(path_frame, r'C:/Users/Riku Aoki/Documents/Programas/GuiaCDT/src/icons/cancel.png', 2, 0),
    },
    {
        "label":Title(path_frame, "Local de Destino:", 3, 1),
        "input":Input(path_frame, "50", 3, 2),
        "warning":VisualWarning(path_frame, r'C:/Users/Riku Aoki/Documents/Programas/GuiaCDT/src/icons/cancel.png', 3, 0),
    }
]
#label_base_image = Title(path_frame, "Imagem Base:", 0, 1)
label_principal_font = Title(path_frame, "Fonte Principal:", 1, 1)
label_italic_font = Title(path_frame, "Fonte com Itálico:", 2, 1)
label_destiny_path = Title(path_frame, "Local de Destino:", 3, 1)

# Definindo Entradas
#input_base_image = Input(path_frame, "50", 0, 2)
input_principal_font = Input(path_frame, "50", 1, 2)
input_italic_font = Input(path_frame, "50", 2, 2)
input_destiny_path = Input(path_frame, "50", 3, 2)

# Imagens Verificadoras
#warning_base_image = VisualWarning(path_frame, r'C:/Users/Riku Aoki/Documents/Programas/GuiaCDT/src/icons/cancel.png', 0, 0)
warning_principal_font = VisualWarning(path_frame, r'C:/Users/Riku Aoki/Documents/Programas/GuiaCDT/src/icons/cancel.png', 1, 0)
warning_italic_font = VisualWarning(path_frame, r'C:/Users/Riku Aoki/Documents/Programas/GuiaCDT/src/icons/cancel.png', 2, 0)
warning_destiny_path = VisualWarning(path_frame, r'C:/Users/Riku Aoki/Documents/Programas/GuiaCDT/src/icons/cancel.png', 3, 0)

#warning_base_image.setImage(r'C:/Users/Riku Aoki/Documents/Programas/GuiaCDT/src/icons/add.png')



def testeDado():
    for item in inputs:
        if item["input"].getValue():
            if item["input"].verification.isImage(item["input"].getValue()):
                item["warning"].setImage(r'C:/Users/Riku Aoki/Documents/Programas/GuiaCDT/src/icons/accept.png')
                item["warning"].setMessage("Imagem Encontrada!")
            elif item["input"].verification.isImage(item["input"].getValue()) == None:
                item["warning"].setImage(r'C:/Users/Riku Aoki/Documents/Programas/GuiaCDT/src/icons/cancel.png')
                item["warning"].setMessage("Esperava algo como C:/path/image.png")
            elif not item["input"].verification.isImage(item["input"].getValue()):
                item["warning"].setImage(r'C:/Users/Riku Aoki/Documents/Programas/GuiaCDT/src/icons/cancel.png')
                item["warning"].setMessage("A imagem deve ser .png")
        else:
            item["warning"].setImage(r'C:/Users/Riku Aoki/Documents/Programas/GuiaCDT/src/icons/cancel.png')
            item["warning"].setMessage("Path não identificado")
            
    """ for x in range(5):
        if inputs[x].getValue():
            if inputs[x].verification.isImage(inputs[x].getValue()):
                warnings[x].setImage(r'C:/Users/Riku Aoki/Documents/Programas/GuiaCDT/src/icons/accept.png')
                warnings[x].setMessage("Imagem Encontrada!")
            elif inputs[x].verification.isImage(inputs[x].getValue()) == None:
                warnings[x].setImage(r'C:/Users/Riku Aoki/Documents/Programas/GuiaCDT/src/icons/cancel.png')
                warnings[x].setMessage("Esperava algo como C:/path/image.png")
            elif not inputs[x].verification.isImage(inputs[x].getValue()):
                warnings[x].setImage(r'C:/Users/Riku Aoki/Documents/Programas/GuiaCDT/src/icons/cancel.png')
                warnings[x].setMessage("A imagem deve ser .png")
        else:
            warnings[x].setImage(r'C:/Users/Riku Aoki/Documents/Programas/GuiaCDT/src/icons/cancel.png')
            warnings[x].setMessage("Path não identificado") """
            

    """ if input_base_image.getValue():
        if input_base_image.verification.isImage(input_base_image.getValue()):
            warning_base_image.setImage(r'C:/Users/Riku Aoki/Documents/Programas/GuiaCDT/src/icons/accept.png')
            warning_base_image.setMessage("Imagem Encontrada!")
        elif input_base_image.verification.isImage(input_base_image.getValue()) == None:
            warning_base_image.setImage(r'C:/Users/Riku Aoki/Documents/Programas/GuiaCDT/src/icons/cancel.png')
            warning_base_image.setMessage("Esperava algo como C:/path/image.png")
        elif not input_base_image.verification.isImage(input_base_image.getValue()):
            warning_base_image.setImage(r'C:/Users/Riku Aoki/Documents/Programas/GuiaCDT/src/icons/cancel.png')
            warning_base_image.setMessage("A imagem deve ser .png")
    else:
        warning_base_image.setImage(r'C:/Users/Riku Aoki/Documents/Programas/GuiaCDT/src/icons/cancel.png')
        warning_base_image.setMessage("Path não identificado") """

    #print(frame01.returnText())

btn2 = Button(root, text = "Show Original", command=lambda: testeDado())
btn2.grid(row=2, column=0)

path_frame.grid(row=0, column=0)

# Responsividade
path_frame.grid_rowconfigure(0, weight=1)
path_frame.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

root.mainloop()
