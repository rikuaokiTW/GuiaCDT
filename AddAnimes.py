import tkinter as Tk
from tkinter import filedialog
import os, asyncio, threading

class Title():
    def __init__(self, master, name, row, column, pady=5, columnspan=1):
        self.label = Tk.Label(master, text=name, font=("Arial", 10), pady=pady, padx=5)
        self.label.grid(row=row, column=column, columnspan=columnspan, sticky=Tk.W)

    def getValue(self):
        return self.label.cget("text")

class Input():
    def __init__(self, master, row, column):
        self.input = Tk.Entry(master, width=50, font=("Arial", 10))
        self.input.grid(row=row, column=column, sticky=Tk.EW)

    def getValue(self):
        return self.input.get()

    def setText(self, text):
        self.clearText()
        self.input.insert(0, text)

    def clearText(self):
        self.input.delete(0, Tk.END)

class ButtonItem():
    def __init__(self, master, text, padx, pady, action, row, column, width=20, inputItem='', bgColor='lightgray', bgActive='gray', fontColor='black', pathFile=''):
        self.action = action
        self.inputItem = inputItem
        self.pathFile = pathFile

        self.buttonItem = Tk.Button(master, text=text, width=width, padx=padx, pady=pady, fg=fontColor, bg=bgColor, activebackground=bgActive)
        self.setAction()
        self.buttonItem.grid(row=row, column=column, sticky=Tk.EW)

    def setAction(self):
        if self.action == 'search':
            self.buttonItem.configure(command=lambda: self.inputItem.setText(self.getDirectoryName()))
        elif self.action == 'add':
            self.buttonItem.configure(command=lambda: self.addAnime())
        elif self.action == 'removeLast':
            self.buttonItem.configure(command=lambda: self.removeLastAnime())
        elif self.action == 'removeAll':
            self.buttonItem.configure(command=lambda: self.removeAllAnimes())

    def setPath(self, newPath):
        self.pathFile = newPath

    def getDirectoryName(self):
        firstPath = os.path.split(os.getcwd())
        firstPath = os.path.split(firstPath[0])[0]
        filename = filedialog.askdirectory(initialdir=firstPath)

        return filename

    def addAnime(self):
        if os.path.isfile(self.pathFile):
            with open(self.pathFile) as fileObj:
                fileIsEmpty = len(fileObj.readlines()) == 0
        else:
            fileIsEmpty = True

        with open(self.pathFile, 'a') as file:
            for item in self.inputItem:
                if item['input'].getValue() == '':
                    item['input'].setText('==')
            if fileIsEmpty:
                for item in self.inputItem:
                    if 'Data' in item['fieldName'].getValue():
                        file.write(item['input'].getValue())
                    else:
                        file.write(f'{item["input"].getValue()}\n')
            else:
                for item in self.inputItem:
                    if 'Título Original' in item['fieldName'].getValue():
                        file.write(f'\n\n{item["input"].getValue()}\n')
                    elif 'Data' in item['fieldName'].getValue():
                        file.write(item["input"].getValue())
                    else:
                        file.write(f'{item["input"].getValue()}\n')

        for item in self.inputItem:
            item['input'].clearText()

    def removeLastAnime(self):
        if os.path.isfile(self.pathFile):
            fileIsEmpty = False
            with open(self.pathFile) as fileObj:
                fileLength = len(fileObj.readlines())
        else:
            fileIsEmpty = True

        if fileIsEmpty:
            open(self.pathFile, 'w').close()
        else:
            if fileLength <= 12:
                open(self.pathFile, 'w').close()
            else:
                fileLength -= 1
                with open(self.pathFile) as fileObj:
                    infoList = fileObj.readlines()
                    for i in range(13):
                        infoList.pop()
                with open(self.pathFile, 'w') as file:
                    infoList[-1] = infoList[-1].rstrip()
                    for info in infoList:
                        file.write(info)

    def removeAllAnimes(self):
        if os.path.isfile(self.pathFile):
            open(self.pathFile, 'w').close()
                      

async def verifyInput():
    while True:
        try:
            global pathFile
            pathFile = os.path.join(pathInput.getValue(), fileNameInput.getValue() + '.txt')

            addButton.setPath(pathFile)
            removeLast.setPath(pathFile)
            removeAll.setPath(pathFile)
            await asyncio.sleep(1)
        except asyncio.CancelledError:
            break

def onClosing():
    async_loop.stop()
    root.destroy()

def _asyncio_thread():
    async_loop.create_task(verifyInput())
    async_loop.run_forever()

if __name__ == '__main__':
    root = Tk.Tk()
    root.title("Adicionador de Animes")

    windowRes = (500, 550)
    monitorRes = (root.winfo_screenwidth(), root.winfo_screenheight())
    windowPos = (monitorRes[0]/2 - windowRes[0]/2, (monitorRes[1]/2 - windowRes[1]/2) - 30)
    root.geometry(f"{windowRes[0]}x{windowRes[1]}+{int(windowPos[0])}+{int(windowPos[1])}")

    pathTitle = Title(root, 'Pasta do Arquivo:', 0, 0)
    pathInput = Input(root, 0, 1)
    pathLocator = ButtonItem(root, '...', 0, 0, 'search', 0, 3, 2, pathInput)

    fileNameTitle = Title(root, 'Nome do Arquivo:', 1, 0)
    fileNameInput = Input(root, 1, 1)

    spacing1 = Title(root, '', 2, 0, pady=10, columnspan=3)

    fields = [
        {
            "fieldName": Title(root, '1. Título Original:', 3, 0),
            "input": Input(root, 3, 1),
        },
        {
            "fieldName": Title(root, '2. Título em Inglês:', 4, 0),
            "input": Input(root, 4, 1),
        },
        {
            "fieldName": Title(root, '3. TEMA/GEN/DEMOG:', 5, 0),
            "input": Input(root, 5, 1),
        },
        {
            "fieldName": Title(root, '4. Nome do Estúdio:', 6, 0),
            "input": Input(root, 6, 1),
        },
        {
            "fieldName": Title(root, '5. Animes do Estúdio:', 7, 0),
            "input": Input(root, 7, 1),
        },
        {
            "fieldName": Title(root, '6. Nome do Diretor:', 8, 0),
            "input": Input(root, 8, 1),
        },
        {
            "fieldName": Title(root, '7. Animes do Diretor:', 9, 0),
            "input": Input(root, 9, 1),
        },
        {
            "fieldName": Title(root, '8. Nome do Compositor:', 10, 0),
            "input": Input(root, 10, 1),
        },
        {
            "fieldName": Title(root, '9. Animes do Compositor:', 11, 0),
            "input": Input(root, 11, 1),
        },
        {
            "fieldName": Title(root, '10. Origem:', 12, 0),
            "input": Input(root, 12, 1),
        },
        {
            "fieldName": Title(root, '11. Plataforma:', 13, 0),
            "input": Input(root, 13, 1),
        },
        {
            "fieldName": Title(root, '12. Data de Estréia:', 14, 0),
            "input": Input(root, 14, 1),
        },
    ]

    spacing2 = Title(root, '', 15, 0, pady=10, columnspan=3)

    buttonFrame = Tk.Frame(root)

    addButton = ButtonItem(buttonFrame, 'Adicionar', 4, 2, 'add', 0, 0, inputItem=fields, bgColor='#7BFF78', fontColor='#0d650b')
    removeLast = ButtonItem(buttonFrame, 'Remover Último', 4, 2, 'removeLast', 0, 1, bgColor='lightyellow', fontColor='black')
    removeAll = ButtonItem(buttonFrame, 'Apagar Tudo', 4, 2, 'removeAll', 0, 2, bgColor='#FF7878', fontColor='#650B0B')

    buttonFrame.grid(row=16, column=0, columnspan=4, sticky=Tk.EW)


    root.grid_columnconfigure([1], weight=1)
    root.grid_rowconfigure([2, 15], weight=1)
    buttonFrame.grid_columnconfigure([0, 1, 2], weight=1)

    async_loop = asyncio.get_event_loop()
    thread = threading.Thread(target=_asyncio_thread)
    thread.start()

    root.protocol("WM_DELETE_WINDOW", onClosing)

    root.mainloop()
