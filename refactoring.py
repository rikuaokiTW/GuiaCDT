from tkinter import *
from tkinter import filedialog
from tkinter.tix import *
from PIL import Image, ImageDraw, ImageFont
import re, os, logging, asyncio, threading

logging.basicConfig(filename="log.txt", filemode="w", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s", datefmt='%d/%m/%Y %I:%M:%S %p')
logging.debug('=================================')
logging.debug('Início do Programa')

#--------------------------------------------------------------------------
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
        logging.debug('*** Criando Instância de VisualWarning ***')
        logging.debug(f'Instância gerada no frame {master}, linha {row} e coluna {column}')
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
        logging.debug('*** Fim de Criação de Instância ***')

    def setImage(self, newImage):
        self.__image = PhotoImage(file=newImage)
        self.__warning.configure(image=self.__image)
        self.__warning.image = self.__image

    def setMessage(self, newMessage):
        self.__balloonWarning.bind_widget(self.__warning, balloonmsg=newMessage)

class Title(Label):
    def __init__(self, master, name, row, column, padx=0, pady=0, bgColor='', fgColor='', columnspan = 1, sticky = 'W', listInputs=[]):
        logging.debug('*** Criando Instância de Title ***')
        logging.debug(f'Instância gerada no frame {master}, linha {row} e coluna {column}')
        super().__init__()
        self.__master = master
        self._row = row
        self._column = column
        self._columnspan = columnspan
        self._listInputs = listInputs
        self.sticky = sticky
        self.name = name if name else "T: 0"
        self.bgColor = bgColor if bgColor else self.__master.cget("bg")
        self.fgColor = fgColor if fgColor else "black"

        self.label = Label(self.__master, text=self.name, padx=padx, pady=pady, bg=self.bgColor, fg=self.fgColor)
        self.label.grid(row=self._row, column=self._column, columnspan=self._columnspan, sticky=EW)
        self.label.bind("<Configure>", self.setSize)
        #self.label.columnconfigure(self._column, weight=2)
        logging.debug('*** Fim de Criação de Instância ***')

    def setName(self, newName):
        self.label.config(text = newName)
    
    def setSize(self, event):
        if event.width < 10:
            font_size = int(event.width/1)
            logging.info(f"Redimensionando {self.label.cget('text')} no caso 1: de {event.width} para {font_size}")
        elif event.width >= 10 and event.width < 20:
            font_size = int(event.width/2)
            logging.info(f"Redimensionando {self.label.cget('text')} no caso 2: de {event.width} para {font_size}")
        elif event.width >= 20 and event.width < 30:
            font_size = int(event.width/3)
            logging.info(f"Redimensionando {self.label.cget('text')} no caso 3: de {event.width} para {font_size}")
        elif event.width >= 30 and event.width < 40:
            font_size = int(event.width/4)
            logging.info(f"Redimensionando {self.label.cget('text')} no caso 4: de {event.width} para {font_size}")
        elif event.width >= 40 and event.width < 50:
            font_size = int(event.width/5)
            logging.info(f"Redimensionando {self.label.cget('text')} no caso 5: de {event.width} para {font_size}")
        elif event.width >= 50 and event.width < 60:
            font_size = int(event.width/6)
            logging.info(f"Redimensionando {self.label.cget('text')} no caso 6: de {event.width} para {font_size}")
        elif event.width >= 60 and event.width < 70:
            font_size = int(event.width/7)
            logging.info(f"Redimensionando {self.label.cget('text')} no caso 7: de {event.width} para {font_size}")
        elif event.width >= 70 and event.width < 80:
            font_size = int(event.width/8)
            logging.info(f"Redimensionando {self.label.cget('text')} no caso 8: de {event.width} para {font_size}")
        elif event.width >= 80 and event.width < 90:
            font_size = int(event.width/9)
            logging.info(f"Redimensionando {self.label.cget('text')} no caso 9: de {event.width} para {font_size}")
        elif event.width >= 90 and event.width < 110:
            font_size = int(event.width/10)
            logging.info(f"Redimensionando {self.label.cget('text')} no caso 10: de {event.width} para {font_size}")
        elif event.width >= 110 and event.width < 150:
            font_size = int(event.width/11)
            logging.info(f"Redimensionando {self.label.cget('text')} no caso 11: de {event.width} para {font_size}")
        elif event.width >= 150:
            font_size = 14
            logging.info(f"Redimensionando {self.label.cget('text')} no caso 12: de {event.width} para {font_size}")
        #self.label.configure(font=("Arial", font_size))


class Input(Entry):
    def __init__(self, master, width, row, column, textDefault = ''):
        logging.debug('*** Criando Instância de Input ***')
        logging.debug(f'Instância gerada no frame {master}, linha {row} e coluna {column}')
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
        logging.debug('*** Fim de Criação de Instância ***')

    def getValue(self):
        return self.input.get()

    def setText(self, text):
        self.clearText()
        self.input.insert(0, text)
    
    def clearText(self):
        self.input.delete(0, END)

class AreaFrame(Frame):
    def __init__(self, master, frameTitle, campo, numFrames, nameFrames, row, column, bgColor="gray", padx=10, pady=10, bd=3):
        logging.debug('*** Criando Instância de AreaFrame ***')
        logging.debug(f'Instância gerada no frame {master}, linha {row} e coluna {column}')
        super().__init__()
        self.__master = master
        self._row = row
        self._column = column
        self._nameFrames = nameFrames
        self._frameTitle = frameTitle
        self._campo = campo
        
        self.areaFrame = Frame(self.__master, bg=bgColor, padx=padx, pady=pady, bd=bd)
        self.subFrames = []
        logging.debug('*** Fim de Criação de Instância ***')

        for i in range(numFrames):
            columnLabel = i + i
            columnInput = (i + 1) + i
            newFrame = {
                "fieldName": self._nameFrames[i],
                "labelTitle": Title(self.areaFrame, self._nameFrames[i], 1, columnLabel, pady=2, columnspan=2, sticky=EW, fgColor="white"),
                "labelFont": Title(self.areaFrame, "font size:", 2, columnLabel, padx=2, bgColor="gray", fgColor="white"),
                "labelCoordx": Title(self.areaFrame, "coordx:", 3, columnLabel, padx=2, bgColor="gray", fgColor="white"),
                "labelCoordy": Title(self.areaFrame, "coordy:", 4, columnLabel, padx=2, bgColor="gray", fgColor="white"),
                "inputCampo": self._campo,
                "inputFont": Input(self.areaFrame, "10", 2, columnInput),
                "inputCoordx": Input(self.areaFrame, "10", 3, columnInput),
                "inputCoordy": Input(self.areaFrame, "10", 4, columnInput),
            }
            self.subFrames.append(newFrame)
        
        self.title = Title(self.areaFrame, self._frameTitle, 0, 0, pady=2, fgColor="white", columnspan=self.areaFrame.grid_size()[1] + 1, sticky=EW)
        self.areaFrame.grid(row=self._row, column=self._column)

    def getSubFrames(self):
        return self.subFrames

    def getFontSize(self, field):
        #print(field)
        for item in self.subFrames:
            #print(item['fieldName'])
            if item['fieldName'] == field:
                print('Aqui', item['inputFont'].getValue())
                return item["inputFont"].getValue()

    def getValueX(self, field):
        for item in self.subFrames:
            if item["fieldName"] == field:
                return int(item["inputCoordx"].getValue())
    
    def getValueY(self, field):
        for item in self.subFrames:
            if item["fieldName"] == field:
                return int(item["inputCoordy"].getValue())

class SearchButton(Button):
    def __init__(self, master, text, padx, pady, inputIndex, row, column,bgColor='lightgray', bgActive="gray"):
        logging.debug('*** Criando Instância de SearchButton ***')
        logging.debug(f'Instância gerada no frame {master}, linha {row} e coluna {column}')
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
        logging.debug('*** Fim de Criação de Instância ***')
    
    def getFileName(self):
        filename = filedialog.askopenfilename(initialdir=os.getcwd(),filetypes = (("*ttf, *otf, *txt, *png files",".txt .png .otf .ttf"),("all files","*.*")))

        return filename

#--------------------------------------------------------------------------

class ActionButton(Button):
    def __init__(self, master, text, bgColor, fontColor, action, row, column, sticky=N, span=1, listInputs=[]):
        logging.debug('*** Criando Instância de ActionButton ***')
        logging.debug(f'Instância gerada no frame {master}, linha {row} e coluna {column}')
        super().__init__()
        self.__master = master
        self._action = action
        self.listInputs = listInputs

        self.actionButton = Button(self.__master, text=text, background=bgColor, fg=fontColor, width="40", font=("Consolas"), bd=2)
        self.setAction()
        self.actionButton.grid(row=row, column=column, columnspan=span, sticky=sticky)
        self.actionButton.grid_columnconfigure(column, weight=0)
        logging.debug('*** Fim de Criação de Instância ***')

    def setAction(self):
        if self._action == 'limpar':
            self.actionButton.configure(command=lambda: self.clearInputs())
        elif self._action == 'preview':
            self.actionButton.configure(command=lambda: self.setPreview())
    
    def clearInputs(self):
        for item in self.listInputs:
            item['input'].clearText()
    
    def setPreview(self):
        # Abrindo a imagem
        for item in self.listInputs:
            if item['fieldName'] == '1 linha':
                preview_image = Image.open(os.path.join(os.getcwd(), r'src/images/preview.png'))
                
                # Pegando o texto pra adicionar
                text_to_add = item['inputCampo'].getValue()

                # Coordenadas adaptadas pra preview
                preview_font_height = round((int(item['inputFont'].getValue()) / 1080) * 300)
                preview_coordx = int(item['inputCoordx'].getValue()) / 1920 * 523
                preview_coordy = int(item['inputCoordy'].getValue()) / 1080 * 300

                # Definindo a fonte
                text_font = ImageFont.truetype(os.path.join(os.getcwd(), r'src/fonts/coolvetica rg.otf'), preview_font_height)

                # Editando a imagem
                preview_image_edit = ImageDraw.Draw(preview_image)
                preview_image_edit.text((preview_coordx, preview_coordy), text_to_add, anchor="mm", font=text_font)

                # Salvando a imagem
                preview_image.save(os.path.join(os.getcwd(), r'src/images/new_preview.png'))

                # Limpe a entry box
                item['inputCampo'].delete(0, END)
                item['inputCampo'].insert(0, "Saving File...")

                # Espere alguns segundos e mostre a imagem
                image_preview.after(2000, self.show_pic(os.path.join(os.getcwd(), r'src/images/new_preview.png')))

    def show_pic(self, pathNewPic):
        global new_preview
        new_preview = PhotoImage(file=pathNewPic)
        image_preview.config(image=new_preview)

# Async
async def verifyInputs():
    while True:
        try:
            for item in inputs:
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
            await asyncio.sleep(1)
        except asyncio.CancelledError:
            break

async def showLength():
    while True:
        try:
            for item in preview_inputs:
                if item['input'].getValue():
                    item['size'].setName(f"T: {len(item['input'].getValue())}")
            await asyncio.sleep(1)
        except asyncio.CancelledError:
            break

def onClosing():
    async_loop.stop()
    root.destroy()

def _asyncio_thread():
    async_loop.create_task(verifyInputs())
    async_loop.create_task(showLength())
    async_loop.run_forever()

#--------------------------------------------------------------------------
# Início
if __name__ == '__main__':
    # Asyncio
    async_loop = asyncio.get_event_loop()
    #queue = asyncio.Queue()

    root = Tk()
    root.title("Automatizando o Guia")

    #--------------------------------------------------------------------------
    # Dimensao da janela do aplicativo
    dj = (1000, 500)
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
    #button1 = ActionButton(input_frame, 'VALIDAR', '#7BFF78', '#0D650B', 'validar', 5, 0, span=2, listInputs=inputs)
    button1 = ActionButton(input_frame, 'APAGAR', '#FF7878', '#650B0B', 'limpar', 5, 0, span=4, listInputs=inputs)

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

    preview_inputs = [
        {
            "field": "title",
            "title":Title(preview_texts, "1. Título:", 0, 0, padx=5),
            "input":Input(preview_texts, "40", 0, 1),
            "size":Title(preview_texts, "", 0, 2),
        }
    ]
    # Texto de Teste
    """ # Labels
    title_label = Label(preview_texts, text="1. Título:", padx=5)
    title_label.grid(row=0, column=0)

    # Inputs
    title_input = Input(preview_texts, "40", 0, 1)
    #title_input.grid(row=0, column=1, sticky=EW, pady=10)

    # Tamanho do valor do Input
    text_size = title_input.get()
    size_label = Label(preview_texts, text=f"T: {text_size}")
    size_label.grid(row=0, column=2) """

    preview_texts.grid(row=2, column=0, sticky=EW)

    #---------------------------------------------------------------------------
    # Layout de Ajuste finos
    adjust_canvas = Canvas(root, width=dj[0])
    adjust_frame = Frame(adjust_canvas)

    # Criando Labels
    #title_label = Title(adjust_frame, "Título:", 0, 0)
    #title_label.grid(row=0, column=0)


    # Frames onde serão ajustadas as coordenadas e tamanho de fonte
    titles_frame = AreaFrame(adjust_frame, "Título:", preview_inputs[0]['input'], 3, ("1 linha", "2 linhas", "3 linhas"), 0, 0) 

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

    buttonDemo = ActionButton(root, "Demonstração", bgColor="lightyellow", fontColor="black", action="preview", row=4, column=0, sticky=EW, listInputs=titles_frame.getSubFrames())
    """ buttonDemo = Button(root, text="Demonstração", command=lambda: add_it())
    buttonDemo.grid(row=4, column=0, sticky=EW) """



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


    # Thread de verificações assíncronas
    thread = threading.Thread(target=_asyncio_thread)
    thread.start()

    root.protocol("WM_DELETE_WINDOW", onClosing)
    # Loop do tkinter
    root.mainloop()