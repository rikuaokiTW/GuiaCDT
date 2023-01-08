from tkinter import *
from tkinter.tix import *

class FramePath(Frame):
    def __init__(self, master, label_name, row_number, column_number):
        super().__init__()
        self.master = master
        self.label_name = label_name
        self.row_number = row_number
        self.column_number = column_number

        image = PhotoImage(file=r"C:/Users/Riku Aoki/Documents/Programas/GuiaCDT/src/icons/cancel.png")
        self.image_item = Label(self.master)
        self.image_item.configure(image=image)
        self.image_item.image = image
        self.image_item.grid(row=self.row_number, column=self.column_number)
        
        self.label_item = Label(self.master, text=self.label_name, width="10", anchor=W)
        self.label_item.grid(row=self.row_number, column=self.column_number + 1, sticky=W)
        
        self.path_item = Entry(self.master, width="50")
        self.path_item.grid(row=self.row_number, column=self.column_number + 2, sticky="EW")
        
        self.tip_item = Balloon(self.master)
        self.tip_item.bind_widget(self.image_item, balloonmsg="Path não identificado")

    def returnText(self):
        return self.path_item.get()

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
path_frame = Frame(root, width=dj[0], padx=5, pady=5, bd=5, relief="groove")

frame01 = FramePath(path_frame, "Sim", 0, 0)

frame02 = FramePath(path_frame, "Não", 1, 0)

frame03 = FramePath(path_frame, "Tlvz", 2, 0)

frame04 = FramePath(path_frame, "Vai saber", 3, 0)


def showDado():
    print(frame01.returnText())

btn2 = Button(root, text = "Show Original", command=lambda: showDado())
btn2.grid(row=2, column=0)

path_frame.grid(row=0, column=0, sticky="NSWE")

# Responsividade
path_frame.grid_rowconfigure((0, 1, 2, 3), weight=1, uniform=0)
path_frame.grid_columnconfigure((0,1,2,3), weight=1, minsize=2)
root.grid_rowconfigure(0, weight=2)
root.grid_columnconfigure(0, weight=2)


root.mainloop()
