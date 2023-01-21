from tkinter import *
from tkinter.tix import *

class VisualWarning(Label, Balloon):
    def __init__(self, master, pathImage, row, column):
        super().__init__()
        self.master = master
        self.image = PhotoImage(file=pathImage)
        self.row = row
        self.column = column

        self.warning = Label(self.master, image=self.image)
        self.warning.grid(row=self.row, column=self.column)
        
        self.balloonWarning = Balloon(master)
        self.balloonWarning.bind_widget(self.warning, balloonmsg="Path não identificado")

    def setImage(self, newImage):
        self.image = PhotoImage(file=newImage)
        self.warning.configure(image=self.image)
        self.warning.image = self.image

    def setMessage(self, newMessage):
        self.balloonWarning.bind_widget(self.warning, balloonmsg=newMessage)

class Title(Label):
    def __init__(self, master, name, row, column, columnspan = 1, sticky = 'W'):
        super().__init__()
        self.master = master
        self.name = name
        self.row = row
        self.column = column
        self.columnspan = columnspan
        self.sticky = sticky

        self.Label = Label(self.master, text=self.name)
        self.Label.grid(row=self.row, column=self.column, columnspan=self.columnspan, sticky=self.sticky)
        

class Input(Entry):
    def __init__(self, master, width, row, column):
        super().__init__()
        self.master = master
        self.width = width
        self.row = row
        self.column = column
        
        self.input = Entry(self.master, width=self.width)
        self.input.grid(row=self.row, column=self.column)

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


label_bimage = Title(path_frame, "Imagem Base:", 0, 1)
label_principal_font = Title(path_frame, "Fonte Principal:", 1, 1)

base_image_path = Input(path_frame, "50", 0, 2)
principal_font = Input(path_frame, "50", 1, 2)

image_01 = VisualWarning(path_frame, r'C:/Users/Riku Aoki/Documents/Programas/GuiaCDT/src/icons/cancel.png', 0, 0)
image_02 = VisualWarning(path_frame, r'C:/Users/Riku Aoki/Documents/Programas/GuiaCDT/src/icons/cancel.png', 1, 0)

image_01.setImage(r'C:/Users/Riku Aoki/Documents/Programas/GuiaCDT/src/icons/add.png')

def showDado():
    print(base_image_path.getValue())
    image_01.setMessage("Sim")
    #print(frame01.returnText())

btn2 = Button(root, text = "Show Original", command=lambda: showDado())
btn2.grid(row=2, column=0)

path_frame.grid(row=0, column=0)

# Responsividade
path_frame.grid_rowconfigure(0, weight=1)
path_frame.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

root.mainloop()
