from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont
import re, os, logging, asyncio, threading

logging.basicConfig(filename="log.txt", filemode="w", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", datefmt='%d/%m/%Y %I:%M:%S %p')
logging.info('=================================')
logging.info('Início do Programa')

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

class SliceText():
    def __init__(self):
        pass
    
    def twoSlice(self, text, length, maxFont, maxLine1=0):
        maxLine1 = maxLine1 if maxLine1 else maxFont
        if length <= maxFont or length <= maxLine1:
            return text
        elif length > maxLine1:
            newText = list(text)
            characPosi = maxLine1
            for x in range(maxLine1):
                if newText[characPosi] == ' ':
                    newText[characPosi] = '\n'
                    break
                else:
                    characPosi -= 1
            return ''.join(newText)
    
    def threeSlice(self, text, length, maxLine1, maxLine2=0, maxLine3=0):
        maxLine2 = maxLine2 if maxLine2 else maxLine1
        maxLine3 = maxLine3 if maxLine3 else maxLine2
        if length <= maxLine1:
            return text
        elif length > maxLine1 and length <= maxLine2:
            newText = list(text)
            characPosi = maxLine1
            # Quebra pra Segunda Linha
            for x in range(maxLine1):
                if newText[characPosi] == ' ':
                    newText[characPosi] = '\n'
                    break
                else:
                    characPosi -= 1
        elif length > maxLine2 and length <= maxLine3:
            newText = list(text)
            # Quebra pra Segunda Linha
            characPosi1 = maxLine1
            for x in range(maxLine1):
                if newText[characPosi1] == ' ':
                    newText[characPosi1] = '\n'
                    break
                else:
                    characPosi1 -= 1
            # Quebra pra Terceira Linha
            characPosi2 = maxLine2
            for x in range(maxLine1):
                if newText[characPosi2] == ' ':
                    newText[characPosi2] = '\n'
                    break
                else:
                    characPosi2 -= 1
        elif length > maxLine3:
            newText = list(text)
            # Quebra pra Segunda Linha
            characPosi1 = maxLine1
            for x in range(maxLine1):
                if newText[characPosi1] == ' ':
                    newText[characPosi1] = '\n'
                    break
                else:
                    characPosi1 -= 1
            # Quebra pra Terceira Linha
            characPosi2 = maxLine2
            for x in range(maxLine1):
                if newText[characPosi2] == ' ':
                    newText[characPosi2] = '\n'
                    break
                else:
                    characPosi2 -= 1
            # Quebra pra Quarta Linha
            characPosi3 = maxLine3
            for x in range(maxLine1):
                if newText[characPosi3] == ' ':
                    newText[characPosi3] = '\n'
                    break
                else:
                    characPosi3 -= 1
        else:
            newText = list(text)
            characPosi = maxLine1
            for x in range(maxLine1):
                if newText[characPosi] == ' ':
                    newText[characPosi] = '\n'
                    break
                else:
                    characPosi -= 1
        return ''.join(newText)

class ImageText():
    def __init__(self):
        self.oneLine = ImageDraw.Draw
        self.multiLine = ImageDraw.Draw
        self.font = ImageFont.truetype
    
    def fontText(self, path, size, tipo = 'normal'):
        if tipo == 'normal':
            fontText = self.font(path, size)
        elif tipo == 'italic':
            fontText = self.font(path, size)
        elif tipo == 'bold':
            fontText = self.font(path, size)
        return fontText
    
    def writeImage(self, image, text, textFont, coordx, coordy, anchor='ma', spacing=0, color=(255, 255, 255)):
        if '\n' in text:
            #print('Entrou no multiline')
            self.multiLine(image).multiline_text((coordx, coordy), text, anchor=anchor, font=textFont, fill=color, align="center", spacing=spacing)
        else:
            self.oneLine(image).text((coordx, coordy), text, anchor=anchor,
               font=textFont, fill=color)

class BalloonTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.balloonTip = None

        self.widget.bind("<Enter>", lambda _: self.showBalloon())
        self.widget.bind("<Leave>", lambda _: self.hideBalloon())
    
    def setMessage(self, newMessage):
        self.text = newMessage

    def showBalloon(self):
        x, y, _cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 5
        y = y + cy + self.widget.winfo_rooty() + 25
        self.balloonTip = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = Label(tw, text=self.text, justify='left',
                      background="#ffffe0", relief='solid', borderwidth=1,
                      font=("Arial Black", "8", "normal"))
        label.pack(ipadx=1)

    def hideBalloon(self):
        tw = self.balloonTip
        self.balloonTip = None
        if tw:
            tw.destroy()

class VisualWarning(Label):
    """
        RF002 - Configura os alertas visuais e possibilita alteração
    """
    def __init__(self, master, pathImage, row, column):
        super().__init__()
        self.__master = master
        self.__image = PhotoImage(file=pathImage)
        self._row = row
        self._column = column

        self.__warning = Label(self.__master, image=self.__image)
        self.__warning.grid(row=self._row, column=self._column)
        #self.__warning.columnconfigure(self._column, weight=0)
        
        self.__balloonWarning = BalloonTip(self.__warning, 'Path não identificado')
        #self.__balloonWarning.bind_widget(self.__warning, balloonmsg="Path não identificado")
        logging.info(f'*** Instância de VisualWarning - linha: {self._row}, coluna: {self._column} ***')

    def setImage(self, newImage):
        self.__image = PhotoImage(file=newImage)
        self.__warning.configure(image=self.__image)
        self.__warning.image = self.__image

    def setMessage(self, newMessage):
        self.__balloonWarning.setMessage(newMessage)
        #self.__balloonWarning.bind_widget(self.__warning, balloonmsg=newMessage)

class Title(Label):
    def __init__(self, master, name, row, column, padx=0, pady=0, bgColor='', fgColor='', columnspan = 1, sticky = EW, listInputs=[]):
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

        self.label = Label(self.__master, text=self.name, padx=padx, pady=pady, bg=self.bgColor, fg=self.fgColor, font=("Arial", 9))
        self.label.grid(row=self._row, column=self._column, columnspan=self._columnspan, sticky=self.sticky)
        #self.label.bind("<Configure>", self.setSize)
        logging.info(f'*** Instância de Title - linha: {self._row}, coluna: {self._column}***')

    def getValue(self):
        return self.label.cget("text")
    
    def setName(self, newName):
        self.label.config(text = newName)
    
    # Responsividade no Tamanho de Labels
    """ def setSize(self, event):
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
        #self.label.configure(font=("Arial", font_size)) """
    
    def removeWidget(self):
        self.label.grid_remove()


class Input(Entry):
    def __init__(self, master, width, row, column, textDefault = '', columnspan=1):
        super().__init__()
        self.__master = master
        self._width = width
        self._row = row
        self._column = column
        self.verification = FileVerification()
        
        self.input = Entry(self.__master, width=self._width)
        self.input.grid(row=self._row, column=self._column, columnspan=columnspan, sticky=EW)
        self.setText(textDefault)
        logging.info(f'*** Instância de Input - linha: {self._row}, coluna {self._column}***')

    def getValue(self):
        return self.input.get()

    def setText(self, text):
        self.clearText()
        self.input.insert(0, text)
    
    def clearText(self):
        self.input.delete(0, END)
    
    def removeWidget(self):
        self.input.grid_remove()

class AreaFrame(Frame):
    def __init__(self, master, frameTitle, campo, nameFrames, row, column, bgColor="gray", padx=10, pady=10, bd=3):
        super().__init__()
        self.__master = master
        self._row = row
        self._column = column
        self._nameFrames = nameFrames
        self._numFrames = len(nameFrames)
        self._frameTitle = frameTitle
        self._campo = campo
        
        self.areaFrame = Frame(self.__master, bg=bgColor, padx=padx, pady=pady, bd=bd)
        self.subFrames = []
        logging.info(f'*** Instância de AreaFrame - linha: {self._row}, coluna: {self._column} ***')

        for i in range(self._numFrames):
            # RF008 - Exceções de 1 linha para otimização de áreas
            specificFields = ['Título:', 'Gêneros:', 'Origem:', 'Plataforma:', 'Data de Estréia:']
            # Adicionamento dinâmico de colunas
            columnLabel = i * 4
            columnInput = (i * 4) + 2
            # Especificação de colunas dinâmicas para os caracteres
            columnCharac2 = (i * 4) + 2
            columnICharac1 = (i * 4) + 1
            columnICharac2 = (i * 4) + 3

            if self._frameTitle in specificFields or 'Nome' in self._frameTitle:
                newFrame = {
                    "subField": self._nameFrames[i],
                    "labelTitle": Title(self.areaFrame, self._nameFrames[i], 3, columnLabel, pady=5, columnspan=4, sticky=EW, fgColor="white"),
                    "labelCharacter1": Title(self.areaFrame, 'até:', 4, columnLabel, padx=2, bgColor="gray", fgColor="white", sticky=W),
                    "labelCharacter2": Title(self.areaFrame, 'máx:', 4, columnCharac2, padx=2, bgColor="gray", fgColor="white", sticky=W),
                    "labelFont": Title(self.areaFrame, "font size 1:", 5, columnLabel, padx=2, bgColor="gray", fgColor="white", columnspan=2, sticky=W),
                    "labelFont2": Title(self.areaFrame, "font size 2:", 6, columnLabel, padx=2, bgColor="gray", fgColor="white", columnspan=2, sticky=W),
                    "inputCampo": self._campo,
                    "inputCharacter1": Input(self.areaFrame, "5", 4, columnICharac1),
                    "inputCharacter2": Input(self.areaFrame, "5", 4, columnICharac2),
                    "inputFont": Input(self.areaFrame, "6", 5, columnInput, columnspan=2),
                    "inputFont2": Input(self.areaFrame, "6", 6, columnInput, columnspan=2),
                }
                if 'Nome' in self._frameTitle or 'Estréia' in self._frameTitle or self._frameTitle == 'Plataforma:' or self._frameTitle == 'Origem:':
                    newFrame['inputCharacter2'].removeWidget()
                    newFrame.update({'inputCharacter2':Title(self.areaFrame, "-", 4, columnICharac2, padx=2, bgColor="gray", fgColor="white", sticky=EW)})
                if self._nameFrames[i] == '2 linhas':
                    newFrame['inputCharacter1'].removeWidget()
                    newFrame['inputCharacter2'].removeWidget()
                    newFrame["labelSpacing"] = newFrame.pop("labelFont2")
                    newFrame['inputSpacing'] = newFrame.pop("inputFont2")
                    newFrame["labelFont"].setName("font size:")
                    newFrame["labelCharacter1"].setName("min:")
                    newFrame["labelSpacing"].setName("spacing:")
                    newFrame.update({"labelCharacter2":Title(self.areaFrame, "-", 4, columnICharac2, padx=2, bgColor="gray", fgColor="white", columnspan=2, sticky=W), "inputCharacter1":Title(self.areaFrame, "0", 4, columnICharac1, padx=2, bgColor="gray", fgColor="white", sticky=W)})
            else:
                newFrame = {
                    "subField": self._nameFrames[i],
                    "labelTitle": Title(self.areaFrame, self._nameFrames[i], 3, columnLabel, pady=5, columnspan=4, sticky=EW, fgColor="white"),
                    "labelCharacter1": Title(self.areaFrame, 'min:', 4, columnLabel, padx=2, bgColor="gray", fgColor="white", sticky=W),
                    "labelCharacter2": Title(self.areaFrame, 'máx:', 4, columnCharac2, padx=2, bgColor="gray", fgColor="white", sticky=W),
                    "labelFont": Title(self.areaFrame, "font size:", 5, columnLabel, padx=2, bgColor="gray", fgColor="white", columnspan=2, sticky=W),
                    "labelSpacing": Title(self.areaFrame, "spacing:", 6, columnLabel, padx=2, bgColor="gray", fgColor="white", columnspan=2, sticky=W),
                    "inputCampo": self._campo,
                    "inputCharacter1": Title(self.areaFrame, "0", 4, columnICharac1, padx=2, bgColor="gray", fgColor="white", sticky=W),
                    "inputCharacter2": Input(self.areaFrame, "5", 4, columnICharac2),
                    "inputFont": Input(self.areaFrame, "6", 5, columnInput, columnspan=2),
                    "inputSpacing": Input(self.areaFrame, "6", 6, columnInput, columnspan=2),
                }
                if self._nameFrames[i] == '1 linha':
                    newFrame['inputSpacing'].removeWidget()
                    newFrame.update({"inputSpacing":Title(self.areaFrame, "-", 6, columnInput, padx=2, bgColor="gray", fgColor="white", sticky=EW)})
                if self._nameFrames[i] == '4 linhas':
                    newFrame['inputCharacter2'].removeWidget()
                    newFrame.update({"inputCharacter2":Title(self.areaFrame, "-", 4, columnICharac2, padx=2, bgColor="gray", fgColor="white", columnspan=2, sticky=W)})
            newFrame["fieldName"] = self._frameTitle
            self.subFrames.append(newFrame)
        
        frameColumnspan = len(self.subFrames * 4)
        self.title = Title(self.areaFrame, self._frameTitle, 0, 0, pady=2, fgColor="white", columnspan=frameColumnspan, sticky=EW)
        # Coordenadas
        self.labelCoordx = Title(self.areaFrame, "coordx:", 1, 0, bgColor="gray", fgColor="white", columnspan=round(frameColumnspan/2), sticky=EW)
        self.labelCoordy = Title(self.areaFrame, "coordy:", 1, round(frameColumnspan/2), bgColor="gray", fgColor="white", columnspan=round(frameColumnspan/2))
        self.inputCoordx = Input(self.areaFrame, "15", 2, 0, columnspan=round(frameColumnspan/2))
        self.inputCoordy = Input(self.areaFrame, "15", 2, round(frameColumnspan/2), columnspan=round(frameColumnspan/2))
        
        self.areaFrame.grid(row=self._row, column=self._column, sticky=W)

    def getSubFrames(self):
        return self.subFrames

    def getCoordx(self):
        return int(self.inputCoordx.getValue())
    
    def setCoordx(self, newCoordx):
        self.inputCoordx.setText(newCoordx)
    
    def getCoordy(self):
        return int(self.inputCoordy.getValue())
    
    def setCoordy(self, newCoordy):
        self.inputCoordy.setText(newCoordy)

    def getText(self):
        return self._campo.getValue()
    
    def getTitle(self):
        return self.title.getValue()
    
class SearchButton(Button):
    """
        RF004 - Configura botões de pesquisa via explorador de arquivo
    """
    def __init__(self, master, text, padx, pady, inputIndex, row, column, action='file',bgColor='lightgray', bgActive="gray"):
        super().__init__()
        self.__master = master
        self.row = row
        self.column = column
        self.text = text
        self.padx = padx
        self.pady = pady
        self.inputIndex = inputIndex
        self.action = action

        self.searchButton = Button(self.__master, text=self.text, bg=bgColor, activebackground=bgActive, padx=self.padx, pady=self.pady)
        self.setAction()
        self.searchButton.grid(row=self.row, column=self.column)
        logging.info(f'*** Instância de SearchButton - linha: {self.row}, coluna {self.column}***')
    
    def setAction(self):
        if self.action == 'file':
            self.searchButton.configure(command=lambda: inputs[self.inputIndex]['input'].setText(self.getFileName()))
        elif self.action == 'directory':
            self.searchButton.configure(command=lambda: inputs[self.inputIndex]['input'].setText(self.getDirectoryName()))
    
    def getFileName(self):
        filename = filedialog.askopenfilename(initialdir=locationPath,filetypes = (("*ttf, *otf, *txt, *png files",".txt .png .otf .ttf"),("all files","*.*")))

        return filename
    
    def getDirectoryName(self):
        filename = filedialog.askdirectory(initialdir=locationPath)

        return filename

#--------------------------------------------------------------------------

class ActionButton(Button):
    def __init__(self, master, text, bgColor, fontColor, action, row, column, width='40', sticky=N, span=1, listInputs=[], paths=''):
        super().__init__()
        self.__master = master
        self._action = action
        self.listInputs = listInputs
        self.pathBaseImage = paths[0] if paths else ''
        self.pathMainFont = paths[1] if paths else ''
        self.pathItalicFont = paths[2] if paths else ''
        self.pathDirectory = paths[3] if paths else ''
        self.pathDataText = paths[4] if paths else ''
        self.slice = SliceText()
        self.draw = ImageText()

        self.actionButton = Button(self.__master, text=text, background=bgColor, fg=fontColor, width=width, font=("Consolas"), bd=2)
        self.setAction()
        self.actionButton.grid(row=row, column=column, columnspan=span, sticky=sticky)
        self.actionButton.grid_columnconfigure(column, weight=0)
        logging.info(f'*** Instância de ActionButton - linha: {row}, coluna {column}***')

    def setAction(self):
        if self._action == 'limpar':
            self.actionButton.configure(command=lambda: self.clearInputs())
        elif self._action == 'preview':
            self.actionButton.configure(command=lambda: self.setPreview())
        elif self._action == 'salvar config':
            self.actionButton.configure(command=lambda: self.saveConfigs())
        elif self._action == 'salvar paths':
            self.actionButton.configure(command=lambda: self.savePaths())
        elif self._action == 'gerar':
            self.actionButton.configure(command=lambda: self.orderInfo())
        elif self._action == 'confirmar':
            self.actionButton.configure(command=lambda: self.confirmationWindow())
    
    def clearInputs(self):
        for item in self.listInputs:
            item['input'].clearText()
    
    def setPreview(self):
        # RF005 - Gera prévia com a imagem indicada redimensionando-a
        logging.info('*** Início de execução de preview')
        previewImage = Image.open(self.pathBaseImage)
        previewImage = previewImage.resize((533,300))
        for item in self.listInputs:
            field = item['field']
            coordx = item['frame'].getCoordx()
            coordy = item['frame'].getCoordy()
            text = item['frame'].getText()
            logging.info(f'Configurações do Campo {field}')
            logging.info(f'Coordenadas(x, y): ({coordx}, {coordy})')
            logging.info(f'Texto: {text}')
            logging.info(f'Tamanho de Texto: {len(text)}')
            for frames in item['frame'].getSubFrames():
                if frames['subField'] == '1 linha':
                    maxFont = int(frames['inputCharacter1'].getValue())
                    fontHeight1 = int(frames['inputFont'].getValue())
                    try:
                        maxLine1 = int(frames['inputCharacter2'].getValue())
                    except:
                        maxLine1 = 500
                    try:
                        fontHeight2 = int(frames['inputFont2'].getValue())
                    except:
                        fontHeight2 = 0
                        fontHeight3 = 500
                elif frames['subField'] == '2 linhas':
                    if field == 'title' or field == 'genders':
                        maxLine2 = 500
                    fontHeight3 = int(frames['inputFont'].getValue())
                    textSpacing1 = int(frames['inputSpacing'].getValue())
                elif frames['subField'] == '3 linhas':
                    maxLine2 = int(frames['inputCharacter1'].getValue())
                    maxLine3 = int(frames['inputCharacter2'].getValue())
                    fontHeight4 = int(frames['inputFont'].getValue())
                    textSpacing2 = int(frames['inputSpacing'].getValue())
                elif frames['subField'] == '4 linhas':
                    fontHeight5 = int(frames['inputFont'].getValue())
                    textSpacing3 = int(frames['inputSpacing'].getValue())

            if 'Animes' in field:
                if fontHeight1 > fontHeight3 and len(text) > maxLine1 and len(text) < maxLine2:
                    for x in range(0, fontHeight1 - fontHeight3, 2):
                        maxLine1 += 3
                elif fontHeight3 > fontHeight4 and len(text) > maxLine2 and len(text) < maxLine3:
                    for x in range(0, fontHeight3 - fontHeight4, 2):
                        maxLine1 += 3
                    for x in range(fontHeight3 - fontHeight4):
                        maxLine2 += 5
                elif fontHeight4 > fontHeight5 and len(text) > maxLine3:
                    for x in range(0, fontHeight4 - fontHeight5, 2):
                        if len(text) > 125 and len(text) <= 150:
                            maxLine1 += 6
                        elif len(text) > 150 and len(text) <= 160:
                            maxLine1 += 8
                        elif len(text) > 160:
                            maxLine1 += 13
                        else:
                            maxLine1 += 5
                    for x in range(fontHeight4 - fontHeight5):
                        if len(text) > 125 and len(text) <= 150:
                            maxLine2 += 7
                        elif len(text) > 150 and len(text) <= 160:
                            maxLine2 += 9
                        elif len(text) > 160:
                            maxLine2 += 13
                        else:
                            maxLine2 += 4
                    for x in range(fontHeight4 - fontHeight5):
                        if len(text) > 125 and len(text) <= 150:
                            maxLine3 += 5
                        elif len(text) > 150 and len(text) <= 160:
                            maxLine3 += 6
                        elif len(text) > 160:
                            maxLine3 += 11
                textToAdd = self.slice.threeSlice(text, len(text), maxLine1, maxLine2, maxLine3)
                logging.info('Parâmetros de Caracteres')
                logging.info(f'Limites:')
                logging.info(f'Linha 1: {maxLine1}')
                logging.info(f'Linha 2: {maxLine2}')
                logging.info(f'Linha 3: {maxLine3}')
                logging.info(f'Texto Final: {textToAdd}')

            else:
                textToAdd = self.slice.twoSlice(text, len(text), maxFont, maxLine1=maxLine1)
                logging.info('Parâmetros de Caracteres')
                logging.info(f'Limites:')
                logging.info(f'Limite pra Fonte 1: {maxFont}')
                logging.info(f'Limite Linha 1: {maxLine1}')
                logging.info(f'Texto Final: {textToAdd}')

            if len(text) <= maxFont:
                previewFontHeight = round((fontHeight1 / 1080) * 300)
                textSpacing = 0
            elif len(text) > maxFont and len(text) <= maxLine1:
                if 'Animes' in item['field']:
                    previewFontHeight = round((fontHeight1 / 1080) * 300)
                else:
                    previewFontHeight = round((fontHeight2 / 1080) * 300)
                textSpacing = 0
            elif len(text) > maxLine1 and len(text) <= maxLine2 if maxLine2 else maxLine1:
                previewFontHeight = round((fontHeight3 / 1080) * 300)
                textSpacing = textSpacing1
            elif len(text) > maxLine2 and len(text) <= maxLine3 if maxLine3 else maxLine2:
                previewFontHeight = round((fontHeight4 / 1080) * 300)
                textSpacing = textSpacing2
            elif len(text) > maxLine3 if maxLine3 else maxLine2:
                previewFontHeight = round((fontHeight5 / 1080) * 300)
                textSpacing = textSpacing3
            
            logging.info(f'Tamanho de Fonte do Preview: {previewFontHeight}')
            logging.info(f'Spacing Definido: {textSpacing}')
            
            if field == 'title':
                previewCoordx = (int(coordx) / 1920 * 523) + 5
            else:
                previewCoordx = (int(coordx) / 1920 * 523) + 2
            previewCoordy = int(coordy) / 1080 * 300

            # Definindo a fonte
            if 'Animes' in field:
                textFont = self.draw.fontText(self.pathItalicFont, previewFontHeight, 'italic')
                # Editando a imagem
                self.draw.writeImage(previewImage, textToAdd, textFont, previewCoordx, previewCoordy, anchor='ma', spacing=textSpacing if textSpacing else 0, color=(245, 245, 245))
            else:
                textFont = self.draw.fontText(self.pathMainFont, previewFontHeight)
                # Editando a imagem
                self.draw.writeImage(previewImage, textToAdd, textFont, previewCoordx, previewCoordy, anchor='mm' if item['field'] == 'title' or item['field'] == 'premiere' else 'ma', spacing=textSpacing if textSpacing else 0)
        # Salvando a imagem
        previewImage.save(os.path.join(locationPath, r'src/images/new_preview.png'))
        # Espere alguns segundos e mostre a imagem
        imagePreview.after(2000, self.show_pic(os.path.join(locationPath, r'src/images/new_preview.png')))

    def show_pic(self, pathNewPic):
        global newPreview
        newPreview = PhotoImage(file=pathNewPic)
        imagePreview.config(image=newPreview)
    
    def setPaths(self, newPaths=''):
        self.pathBaseImage = newPaths[0] if newPaths else ''
        self.pathMainFont = newPaths[1] if newPaths else ''
        self.pathItalicFont = newPaths[2] if newPaths else ''
        self.pathDirectory = newPaths[3] if newPaths else ''
        self.pathDataText = newPaths[4] if newPaths else ''
    
    def confirmationWindow(self):
        window = Toplevel()
        window.title('Confirmação de Salvamento')
        
        message = Title(window, 'Você deseja realmente salvar essas configurações?', 0, 0, 5, 20, columnspan=2, sticky=EW)
        buttonY = ActionButton(window, "Sim", '#7BFF78', '#0D650B', 'salvar config', 1, 0, width='10', sticky=EW, listInputs= self.listInputs)
        buttonN = Button(window, text='Não', background='#FF7878', fg='#650B0B', width="10", font=("Consolas"), bd=2, command=lambda: window.destroy())
        buttonN.grid(row=1, column=1, sticky=EW)
        # Dimensao da janela do aplicativo
        dj = (300, 100)
        # Resolucao do Monitor
        rm = (window.winfo_screenwidth(), window.winfo_screenheight())
        # Posicao da Janela do Aplicativo
        pj = (rm[0]/2 - dj[0]/2, (rm[1]/2 - dj[1]/2) - 30)
        # Centralizando a Janela com relação ao monitor
        window.geometry("{}x{}+{}+{}".format(dj[0], dj[1], int(pj[0]), int(pj[1])))
        # Responsividade
        window.grid_rowconfigure([0, 1], weight=1)
        window.grid_columnconfigure([0, 1], weight=1)
    
    def savePaths(self):
        # RF009 -  Salvamento de 'paths' em texto simples
        fileLocation = re.compile(r'GuiaCDT.+')
        barLocation = re.compile(r'[/]+')
        with open(os.path.join(locationPath, r'src\data\paths.txt'), 'w') as paths:
            for item in self.listInputs:
                if 'GuiaCDT' in item['input'].getValue():
                    path = barLocation.sub('\\\\', item['input'].getValue())
                    paths.write(fileLocation.search(path).group()[8:] + '\n')
                else:
                    paths.write('==\n')
    
    def saveConfigs(self):
        # RF009 - Salvamento de configurações de ajuste em texto simples
        with open(os.path.join(locationPath, r'src\data\configs.txt'), 'w') as configs:
            for item in self.listInputs:
                field = item['frame'].getTitle()
                #print(field)
                configs.write(f"campo: {item['frame'].getTitle()}\n")
                configs.write(f"coordx: {item['frame'].getCoordx()}\n")
                configs.write(f"coordy: {item['frame'].getCoordy()}\n")
                for frames in item['frame'].getSubFrames():
                    if frames['subField'] == '1 linha':
                        if 'Animes' not in field:
                            configs.write(f"1inputCharacter1: {frames['inputCharacter1'].getValue()}\n")
                        if 'Título' in field or 'Gêneros' in field or 'Animes' in field:
                            configs.write(f"1inputCharacter2: {frames['inputCharacter2'].getValue()}\n")
                        configs.write(f"1inputFont: {frames['inputFont'].getValue()}\n")
                        if 'Animes' not in field:
                            if 'Data' in field:
                                configs.write(f"1inputFont2: {frames['inputFont2'].getValue()}")
                            else:
                                configs.write(f"1inputFont2: {frames['inputFont2'].getValue()}\n")
                    elif frames['subField'] == '2 linhas':
                        if 'Animes' in field:
                            configs.write(f"2inputCharacter2: {frames['inputCharacter2'].getValue()}\n")
                        configs.write(f"2inputFont: {frames['inputFont'].getValue()}\n")
                        configs.write(f"2inputSpacing: {frames['inputSpacing'].getValue()}\n")
                    elif frames['subField'] == '3 linhas':
                        configs.write(f"3inputCharacter2: {frames['inputCharacter2'].getValue()}\n")
                        configs.write(f"3inputFont: {frames['inputFont'].getValue()}\n")
                        configs.write(f"3inputSpacing: {frames['inputSpacing'].getValue()}\n")
                    elif frames['subField'] == '4 linhas':
                        configs.write(f"4inputFont: {frames['inputFont'].getValue()}\n")
                        configs.write(f"4inputSpacing: {frames['inputSpacing'].getValue()}\n")
                if 'Data' not in field:
                    configs.write('\n')
        logging.info('*** Configurações Salvas ***')
        self.__master.destroy()
    
    def orderInfo(self):
        # Lista que conterá as informações de cada anime
        animesList = []
        # Informações a serem coletadas de cada anime
        animesInfo = {
            'title': '',
            'genders': '',
            'studioName': '',
            'studioAnimes': '',
            'directorName': '',
            'directorAnimes': '',
            'composerName': '',
            'composerAnimes': '',
            'originalSource': '',
            'platform': '',
            'premiere': '',
        }

        with open(self.pathDataText) as fileObj:
            infoAnimes = fileObj.readlines()
            infoAnimes = [line.rstrip() for line in infoAnimes]
            while '' in infoAnimes:
                infoAnimes.remove('')
            if infoAnimes.count('=='):
                for item in infoAnimes:
                    if item == '==':
                        infoAnimes[infoAnimes.index('==')] = ''
        
        for x in range(round(len(infoAnimes)/11)):
            animesItems = infoAnimes[x*11:]
            item = 0
            for key in animesInfo.keys():
                animesInfo[key] = animesItems[item]
                item += 1
            animesList.append(animesInfo)
            animesInfo = {
                        'title': '',
                        'genders': '',
                        'studioName': '',
                        'studioAnimes': '',
                        'directorName': '',
                        'directorAnimes': '',
                        'composerName': '',
                        'composerAnimes': '',
                        'originalSource': '',
                        'platform': '',
                        'premiere': '',
                    }
        self.createImage(animesList)

    def createImage(self, animesList):
        logging.info('Gerando Imagens Finais')
        for anime in animesList:
            # Definindo nome da Imagem
            imageName = anime['title']
            # Removendo caracteres proibidos em nome de arquivo
            forbidden = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
            imageName = list(imageName)
            for symbol in forbidden:
                if symbol in imageName:
                    while symbol in imageName:
                        imageName.remove(symbol)
            imageName = ''.join(imageName) + '.png'

            finalImage = Image.open(self.pathBaseImage)
            for key, value in anime.items():
                for item in self.listInputs:
                    if key == item['field']:
                        field = item['field']
                        coordx = item['frame'].getCoordx()
                        coordy = item['frame'].getCoordy()
                        text = value
                        for frames in item['frame'].getSubFrames():
                            if frames['subField'] == '1 linha':
                                maxFont = int(frames['inputCharacter1'].getValue())
                                fontHeight1 = int(frames['inputFont'].getValue())
                                try:
                                    maxLine1 = int(frames['inputCharacter2'].getValue())
                                except:
                                    maxLine1 = 500
                                try:
                                    fontHeight2 = int(frames['inputFont2'].getValue())
                                except:
                                    fontHeight2 = 0
                                    fontHeight3 = 500
                            elif frames['subField'] == '2 linhas':
                                if field == 'title' or field == 'genders':
                                    maxLine2 = 500
                                fontHeight3 = int(frames['inputFont'].getValue())
                                textSpacing1 = int(frames['inputSpacing'].getValue())
                            elif frames['subField'] == '3 linhas':
                                maxLine2 = int(frames['inputCharacter1'].getValue())
                                maxLine3 = int(frames['inputCharacter2'].getValue())
                                fontHeight4 = int(frames['inputFont'].getValue())
                                textSpacing2 = int(frames['inputSpacing'].getValue())
                            elif frames['subField'] == '4 linhas':
                                fontHeight5 = int(frames['inputFont'].getValue())
                                textSpacing3 = int(frames['inputSpacing'].getValue())

                        if 'Animes' in field:
                            if fontHeight1 > fontHeight3 and len(text) > maxLine1 and len(text) < maxLine2:
                                for x in range(0, fontHeight1 - fontHeight3, 2):
                                    maxLine1 += 3
                            elif fontHeight3 > fontHeight4 and len(text) > maxLine2 and len(text) < maxLine3:
                                for x in range(0, fontHeight3 - fontHeight4, 2):
                                    maxLine1 += 3
                                for x in range(fontHeight3 - fontHeight4):
                                    maxLine2 += 5
                            elif fontHeight4 > fontHeight5 and len(text) > maxLine3:
                                for x in range(0, fontHeight4 - fontHeight5, 2):
                                    if len(text) > 125:
                                        maxLine1 += 6
                                    if len(text) > 125 and len(text) <= 150:
                                        maxLine1 += 6
                                    elif len(text) > 150 and len(text) <= 160:
                                        maxLine1 += 8
                                    elif len(text) > 160:
                                        maxLine1 += 13
                                    else:
                                        maxLine1 += 5
                                for x in range(fontHeight4 - fontHeight5):
                                    if len(text) > 125 and len(text) <= 150:
                                        maxLine2 += 7
                                    elif len(text) > 150 and len(text) <= 160:
                                        maxLine2 += 9
                                    elif len(text) > 160:
                                        maxLine2 += 13
                                    else:
                                        maxLine2 += 4
                                for x in range(fontHeight4 - fontHeight5):
                                    if len(text) > 125 and len(text) <= 150:
                                        maxLine3 += 4
                                    elif len(text) > 150 and len(text) <= 160:
                                        maxLine3 += 6
                                    elif len(text) > 160:
                                        maxLine3 += 11
                            textToAdd = self.slice.threeSlice(text, len(text), maxLine1, maxLine2, maxLine3)

                        else:
                            textToAdd = self.slice.twoSlice(text, len(text), maxFont, maxLine1=maxLine1)

                        if len(text) <= maxFont:
                            finalFontHeight = fontHeight1
                            textSpacing = 0
                        elif len(text) > maxFont and len(text) <= maxLine1:
                            if 'Animes' in item['field']:
                                finalFontHeight = fontHeight1
                            else:
                                finalFontHeight = fontHeight2
                            textSpacing = 0
                        elif len(text) > maxLine1 and len(text) <= maxLine2:
                            finalFontHeight = fontHeight3
                            textSpacing = textSpacing1
                        elif len(text) > maxLine2 and len(text) <= maxLine3:
                            finalFontHeight = fontHeight4
                            textSpacing = textSpacing2
                        elif len(text) > maxLine3:
                            finalFontHeight = fontHeight5
                            textSpacing = textSpacing3
                        
                        finalCoordx = int(coordx)
                        finalCoordy = int(coordy)

                        # Definindo a fonte
                        if 'Animes' in field:
                            textFont = self.draw.fontText(self.pathItalicFont, finalFontHeight, 'italic')
                            # Editando a imagem
                            self.draw.writeImage(finalImage, textToAdd, textFont, finalCoordx, finalCoordy, anchor='ma', spacing=textSpacing if textSpacing else 0, color=(245, 245, 245))
                        else:
                            textFont = self.draw.fontText(self.pathMainFont, finalFontHeight)
                            # Editando a imagem
                            self.draw.writeImage(finalImage, textToAdd, textFont, finalCoordx, finalCoordy, anchor='mm' if item['field'] == 'title' or item['field'] == 'premiere' else 'ma', spacing=textSpacing if textSpacing else 0)
            # Salvando a imagem
            logging.info(f'Gerada imagem "{imageName}"')
            finalImage.save(os.path.join(self.pathDirectory, imageName))

        


# RF003 - Funções Assíncronas de Check-up
async def verifyInputs():
    while True:
        try:
            for item in inputs:
                # Passando os paths para o escopo global do programa
                global pathBaseImage, pathMainFont, pathItalicFont, pathDirectory, pathDataText
                if item['type'] == 'image':
                    pathBaseImage = item['input'].getValue()
                elif item['type'] == 'font1':
                    pathMainFont = item['input'].getValue()
                elif item['type'] == 'font2':
                    pathItalicFont = item['input'].getValue()
                elif item['type'] == 'directory':
                    pathDirectory = item['input'].getValue()
                elif item['type'] == 'text':
                    pathDataText = item['input'].getValue()
                demoButton.setPaths((pathBaseImage, pathMainFont, pathItalicFont, '', ''))
                runButton.setPaths((pathBaseImage, pathMainFont, pathItalicFont, pathDirectory, pathDataText))
                # Verificação de validade
                if item['type'] == 'image':
                    if item["input"].getValue():
                        if item["input"].verification.isImage(item["input"].getValue()):
                            item["warning"].setImage(r'{}'.format(os.path.join(locationPath, r"src\icons\accept.png")))
                            item["warning"].setMessage("Imagem encontrada!")
                        elif item["input"].verification.isImage(item["input"].getValue()) == None:
                            item["warning"].setImage(r'{}'.format(os.path.join(locationPath, r"src\icons\cancel.png")))
                            item["warning"].setMessage("Esperava algo como C:/path/image.png")
                        elif not item["input"].verification.isImage(item["input"].getValue()):
                            item["warning"].setImage(r'{}'.format(os.path.join(locationPath, r"src\icons\cancel.png")))
                            item["warning"].setMessage("A imagem deve ser .png")
                    else:
                        item["warning"].setImage(r'{}'.format(os.path.join(locationPath, r"src\icons\cancel.png")))
                        item["warning"].setMessage("Path não identificado")

                elif 'font' in item['type']:
                    if item["input"].getValue():
                        if item["input"].verification.isFont(item["input"].getValue()):
                            item["warning"].setImage(r'{}'.format(os.path.join(locationPath, r"src\icons\accept.png")))
                            item["warning"].setMessage("Fonte encontrada!")
                        elif item["input"].verification.isFont(item["input"].getValue()) == None:
                            item["warning"].setImage(r'{}'.format(os.path.join(locationPath, r"src\icons\cancel.png")))
                            item["warning"].setMessage("Esperava algo como C:/path/fonte.ttf")
                        elif not item["input"].verification.isFont(item["input"].getValue()):
                            item["warning"].setImage(r'{}'.format(os.path.join(locationPath, r"src\icons\cancel.png")))
                            item["warning"].setMessage("A fonte deve ser .ttf ou .otf")
                    else:
                        item["warning"].setImage(r'{}'.format(os.path.join(locationPath, r"src\icons\cancel.png")))
                        item["warning"].setMessage("Path não identificado")

                elif item['type'] == 'directory':
                    if item["input"].getValue():
                        if item["input"].verification.isDirectory(item["input"].getValue()):
                            item["warning"].setImage(r'{}'.format(os.path.join(locationPath, r"src\icons\accept.png")))
                            item["warning"].setMessage("Pasta encontrada!")
                        elif item["input"].verification.isDirectory(item["input"].getValue()) == None:
                            item["warning"].setImage(r'{}'.format(os.path.join(locationPath, r"src\icons\cancel.png")))
                            item["warning"].setMessage("Esperava algo como C:/path/pasta/")
                        elif not item["input"].verification.isDirectory(item["input"].getValue()):
                            item["warning"].setImage(r'{}'.format(os.path.join(locationPath, r"src\icons\cancel.png")))
                            item["warning"].setMessage("Deve ser uma pasta")
                    else:
                        item['warning'].setImage(r'{}'.format(os.path.join(locationPath, r"src\icons\cancel.png")))
                        item['warning'].setMessage("Pasta não identificada")

                elif item['type'] == 'text':
                    if item["input"].getValue():
                        if item["input"].verification.isText(item["input"].getValue()):
                            item["warning"].setImage(r'{}'.format(os.path.join(locationPath, r"src\icons\accept.png")))
                            item["warning"].setMessage("Informação encontrada!")
                        elif item["input"].verification.isText(item["input"].getValue()) == None:
                            item["warning"].setImage(r'{}'.format(os.path.join(locationPath, r"src\icons\cancel.png")))
                            item["warning"].setMessage("Esperava algo como C:/path/texto.txt")
                        elif not item["input"].verification.isText(item["input"].getValue()):
                            item["warning"].setImage(r'{}'.format(os.path.join(locationPath, r"src\icons\cancel.png")))
                            item["warning"].setMessage("Deve ser um arquivo .txt")
                    else:
                        item["warning"].setImage(r'{}'.format(os.path.join(locationPath, r"src\icons\cancel.png")))
                        item["warning"].setMessage("Path não identificado")
            await asyncio.sleep(1)
        except asyncio.CancelledError:
            break

# RF006 - Função assíncrona para contagem de caracteres
async def showLength():
    while True:
        try:
            for item in previewInputs:
                if item['input'].getValue():
                    item['size'].setName(f"T: {len(item['input'].getValue())}")
            for item in previewFrames:
                for frame in item['frame'].getSubFrames():
                    if frame["subField"] == "1 linha":
                        if frame["inputCharacter2"].getValue():
                            for secondFrame in item['frame'].getSubFrames():
                                if secondFrame["subField"] == "2 linhas":
                                    secondFrame["inputCharacter1"].setName(frame["inputCharacter2"].getValue())
                        else:
                            for secondFrame in item['frame'].getSubFrames():
                                if secondFrame["subField"] == "2 linhas":
                                    secondFrame["inputCharacter1"].setName("0")
                    elif frame["subField"] == "2 linhas":
                        if frame["inputCharacter2"].getValue():
                            for secondFrame in item['frame'].getSubFrames():
                                if secondFrame["subField"] == "3 linhas":
                                    secondFrame["inputCharacter1"].setName(frame["inputCharacter2"].getValue())
                        else:
                            for secondFrame in item['frame'].getSubFrames():
                                if secondFrame["subField"] == "3 linhas":
                                    secondFrame["inputCharacter1"].setName("0")
                    elif frame["subField"] == "3 linhas":
                        if frame["inputCharacter2"].getValue():
                            for secondFrame in item['frame'].getSubFrames():
                                if secondFrame["subField"] == "4 linhas":
                                    secondFrame["inputCharacter1"].setName(frame["inputCharacter2"].getValue())
                        else:
                            for secondFrame in item['frame'].getSubFrames():
                                if secondFrame["subField"] == "4 linhas":
                                    secondFrame["inputCharacter1"].setName("0")
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
    # Paths de localização
    developmentPath = os.getcwd()
    productionPath = os.path.split(os.path.split(os.getcwd())[0])[0]
    locationPath = developmentPath
    # Asyncio
    async_loop = asyncio.get_event_loop()
    #queue = asyncio.Queue()

    root = Tk()
    root.title("Automatizando o Guia")

    #--------------------------------------------------------------------------
    # Dimensao da janela do aplicativo
    dj = (1000, 1000)
    # Resolucao do Monitor
    rm = (root.winfo_screenwidth(), root.winfo_screenheight())
    # Posicao da Janela do Aplicativo
    pj = (rm[0]/2 - dj[0]/2, (rm[1]/2 - dj[1]/2) - 30)
    # Centralizando a Janela com relação ao monitor
    root.geometry("{}x{}+{}+{}".format(dj[0], dj[1], int(pj[0]), int(pj[1])))
    #---------------------------------------------------------------------------
    # Definindo Frame de Entrada de Dados
    inputFrame = Frame(root, width=dj[0], padx=5, pady=5, bd=3, relief="groove")

    # RF001 - Colocando Entrada de Paths de Arquivos
    inputs = [
        {
            "type": 'image', 
            "label":Title(inputFrame, "Imagem Base:", 0, 1),
            "input":Input(inputFrame, "50", 0, 2),
            "warning":VisualWarning(inputFrame, r'{}'.format(os.path.join(locationPath, r"src\icons\cancel.png")), 0, 0),
            "button":SearchButton(inputFrame, "...", 4, 2, 0, 0, 3),
        },
        {
            "type": 'font1',
            "label":Title(inputFrame, "Fonte Principal:", 1, 1),
            "input":Input(inputFrame, "50", 1, 2),
            "warning":VisualWarning(inputFrame, r'{}'.format(os.path.join(locationPath, r"src\icons\cancel.png")), 1, 0),
            "button":SearchButton(inputFrame, "...", 4, 2, 1, 1, 3),
        },
        {
            "type": 'font2',
            "label":Title(inputFrame, "Fonte com Itálico:", 2, 1),
            "input":Input(inputFrame, "50", 2, 2),
            "warning":VisualWarning(inputFrame, r'{}'.format(os.path.join(locationPath, r"src\icons\cancel.png")), 2, 0),
            "button":SearchButton(inputFrame, "...", 4, 2, 2, 2, 3),
        },
        {
            "type": 'directory',
            "label":Title(inputFrame, "Local de Destino:", 3, 1),
            "input":Input(inputFrame, "50", 3, 2),
            "warning":VisualWarning(inputFrame, r'{}'.format(os.path.join(locationPath, r"src\icons\cancel.png")), 3, 0),
            "button":SearchButton(inputFrame, "...", 4, 2, 3, 3, 3, 'directory'),
        },
        {
            "type": 'text',
            "label":Title(inputFrame, "Info Animes:", 4, 1),
            "input":Input(inputFrame, "50", 4, 2),
            "warning":VisualWarning(inputFrame, r'{}'.format(os.path.join(locationPath, r"src\icons\cancel.png")), 4, 0),
            "button":SearchButton(inputFrame, "...", 4, 2, 4, 4, 3),
        },
    ]

    # Botões
    saveButton = ActionButton(inputFrame, 'SALVAR PATHS', 'lightblue', 'blue', 'salvar paths', 5, 0, span=2, listInputs=inputs, sticky=E)
    deleteButton = ActionButton(inputFrame, 'APAGAR', '#FF7878', '#650B0B', 'limpar', 5, 2, span=2, listInputs=inputs, sticky=W)
    
    # RF010 - Busca de paths salvos anteriormente
    if os.path.isfile(os.path.join(locationPath, r'src\data\paths.txt')):
        with open(os.path.join(locationPath, r'src\data\paths.txt')) as fileObject:
            defaultPaths = fileObject.readlines()
            defaultPaths = [line.rstrip() for line in defaultPaths]
            i = 0
            for item in inputs:
                if defaultPaths[i] == '==':
                    item["input"].setText('')
                else:
                    item["input"].setText(os.path.join(locationPath, defaultPaths[i]))
                i += 1

    # Inserindo Frame de Entrada de Dados
    inputFrame.grid(row=0, column=0, sticky=EW)

    #---------------------------------------------------------------------------
    # Definindo Frame de Preview da Imagem
    previewFrame = Frame(root, width=dj[0], padx=5, pady=5, bd=3, relief="groove")

    # RF005 - Procura pela imagem 'preview' para exibir primeiro como padrão
    if '.png' in inputs[0]["input"].getValue():
        preview = Image.open(inputs[0]["input"].getValue())
        preview = preview.resize((533, 300))
        preview.save(os.path.join(locationPath, r'src/images/preview.png'))
        baseImage = PhotoImage(file=os.path.join(locationPath, r'src/images/preview.png'))
    else:
        baseImage = PhotoImage(file=os.path.join(locationPath, r'src/images/preview.png'))
    imagePreview = Label(previewFrame, image=baseImage)
    imagePreview.grid(row=0, column=0)

    previewFrame.grid(row=1, column=0, sticky=EW)

    #---------------------------------------------------------------------------
    # Definindo Frame de Textos de Teste da Imagem
    previewTexts = Frame(root, width=dj[0], padx=5, pady=5, bd=3, relief="groove")

    # RF006 - Campos de inserção de texto-modelo
    previewInputs = [
        {
            "field": "title",
            "title":Title(previewTexts, "1. Título:", 0, 1, padx=5, sticky=W),
            "input":Input(previewTexts, "40", 0, 2),
            "size":Title(previewTexts, "", 0, 3),
        },
        {
            "field": "genders",
            "title":Title(previewTexts, "2. Gêneros:", 1, 1, padx=5, sticky=W),
            "input":Input(previewTexts, "40", 1, 2),
            "size":Title(previewTexts, "", 1, 3),
        },
        {
            "field": "studioName",
            "title":Title(previewTexts, "3. Nome do Estúdio:", 2, 1, padx=5, sticky=W),
            "input":Input(previewTexts, "40", 2, 2),
            "size":Title(previewTexts, "", 2, 3),
        },
        {
            "field": "studioAnimes",
            "title":Title(previewTexts, "4. Animes do Estúdio:", 3, 1, padx=5, sticky=W),
            "input":Input(previewTexts, "40", 3, 2),
            "size":Title(previewTexts, "", 3, 3),
        },
        {
            "field": "directorName",
            "title":Title(previewTexts, "5. Nome do Diretor:", 4, 1, padx=5, sticky=W),
            "input":Input(previewTexts, "40", 4, 2),
            "size":Title(previewTexts, "", 4, 3),
        },
        {
            "field": "directorAnimes",
            "title":Title(previewTexts, "6. Obras do Diretor:", 5, 1, padx=5, sticky=W),
            "input":Input(previewTexts, "40", 5, 2),
            "size":Title(previewTexts, "", 5, 3),
        },
        {
            "field": "composerName",
            "title":Title(previewTexts, "7. Nome do Compositor:", 0, 4, padx=5, sticky=W),
            "input":Input(previewTexts, "40", 0, 5),
            "size":Title(previewTexts, "", 0, 6),
        },
        {
            "field": "composerAnimes",
            "title":Title(previewTexts, "8. Obras do Compositor:", 1, 4, padx=5, sticky=W),
            "input":Input(previewTexts, "40", 1, 5),
            "size":Title(previewTexts, "", 1, 6),
        },
        {
            "field": "originalSource",
            "title":Title(previewTexts, "9. Origem:", 2, 4, padx=5, sticky=W),
            "input":Input(previewTexts, "40", 2, 5),
            "size":Title(previewTexts, "", 2, 6),
        },
        {
            "field": "platform",
            "title":Title(previewTexts, "10. Plataforma:", 3, 4, padx=5, sticky=W),
            "input":Input(previewTexts, "40", 3, 5),
            "size":Title(previewTexts, "", 3, 6),
        },
        {
            "field": "premiere",
            "title":Title(previewTexts, "11. Data de Estréia:", 4, 4, padx=5, sticky=W),
            "input":Input(previewTexts, "40", 4, 5),
            "size":Title(previewTexts, "", 4, 6),
        },
    ]
    # Texto de Teste
    previewTexts.grid(row=2, column=0, sticky=EW)

    #-----------------------------------------------------------------------
    # Layout de Ajuste finos
    adjustCanvas = Canvas(root, width=dj[0])
    adjustFrames = Frame(adjustCanvas)


    # RF007 - Frames onde serão ajustadas as coordenadas e tamanho de fonte
    previewFrames = [
        {
            "field": "title",
            "frame": AreaFrame(adjustFrames, "Título:", previewInputs[0]['input'], ("1 linha", "2 linhas"), 0, 0)
        },
        {
            "field": "genders",
            "frame": AreaFrame(adjustFrames, "Gêneros:", previewInputs[1]['input'], ("1 linha", "2 linhas"), 1, 0)
        },
        {
            "field": "studioName",
            "frame": AreaFrame(adjustFrames, "Nome do Estúdio:", previewInputs[2]['input'], ("1 linha",), 2, 0)
        },
        {
            "field": "studioAnimes",
            "frame": AreaFrame(adjustFrames, "Animes do Estúdio:", previewInputs[3]['input'], ("1 linha", "2 linhas", "3 linhas", "4 linhas"), 3, 0)
        },
        {
            "field": "directorName",
            "frame": AreaFrame(adjustFrames, "Nome do Diretor:", previewInputs[4]['input'], ("1 linha",), 4, 0)
        },
        {
            "field": "directorAnimes",
            "frame": AreaFrame(adjustFrames, "Animes do Diretor:", previewInputs[5]['input'], ("1 linha", "2 linhas", "3 linhas", "4 linhas"), 5, 0)
        },
        {
            "field": "composerName",
            "frame": AreaFrame(adjustFrames, "Nome do Compositor:", previewInputs[6]['input'], ("1 linha",), 6, 0)
        },
        {
            "field": "composerAnimes",
            "frame": AreaFrame(adjustFrames, "Animes do Compositor:", previewInputs[7]['input'], ("1 linha", "2 linhas", "3 linhas", "4 linhas"), 7, 0)
        },
        {
            "field": "originalSource",
            "frame": AreaFrame(adjustFrames, "Origem:", previewInputs[8]['input'], ("1 linha",), 8, 0)
        },        
        {
            "field": "platform",
            "frame": AreaFrame(adjustFrames, "Plataforma:", previewInputs[9]['input'], ("1 linha",), 9, 0)
        },        
        {
            "field": "premiere",
            "frame": AreaFrame(adjustFrames, "Data de Estréia:", previewInputs[10]['input'], ("1 linha",), 10, 0)
        },        

    ]

    # Barra de Scroll
    scrollbar = Scrollbar(root, orient='vertical')
    scrollbar.grid(row=3, column=1, sticky=NSEW)

    # Configurando o comando da scrollbar para controlar o scroll do canva
    scrollbar.config(command = adjustCanvas.yview)

    # Configurando scroll pra controlar a área vertical
    adjustCanvas['yscrollcommand'] = scrollbar.set

    # Conectar a barra de rolagem ao evento/área que você quer rolar
    adjustCanvas.bind('<Configure>', lambda event: adjustCanvas.configure(scrollregion = adjustCanvas.bbox("all")))

    # Adicionando o adjustFrames ao canva para habilitar o scroll
    adjustCanvas.create_window((0,0), window=adjustFrames, anchor=NE)

    adjustCanvas.grid(row=3, column=0, sticky=EW)

    #-----------------------------------------------------------------------
    # Acionar Preview
    pathBaseImage = ''
    pathMainFont = ''
    pathItalicFont = ''
    pathDirectory = ''
    pathDataText = ''

    buttonFrame = Frame(root, width=dj[0], padx=5, pady=5, bd=3, relief='groove')

    confirmationButton = ActionButton(buttonFrame, 'SALVAR CONFIGURAÇÕES', 'lightblue', "blue", 'confirmar', 4, 0, sticky=EW, listInputs=previewFrames)

    demoButton = ActionButton(buttonFrame, "DEMONSTRAÇÃO", bgColor="lightyellow", fontColor="black", action="preview", row=4, column=1, sticky=EW, listInputs=previewFrames, paths=(pathBaseImage, pathMainFont, pathItalicFont, '', ''))

    runButton = ActionButton(buttonFrame, "EXECUTAR", '#7BFF78', '#0D650B', 'gerar', 4, 2, sticky=EW, listInputs=previewFrames, paths=(pathBaseImage, pathMainFont, pathItalicFont, pathDirectory, pathDataText))

    buttonFrame.grid(row=4, column=0, sticky=EW)
    #-----------------------------------------------------------------------

    # RF010 - Busca por configurações salvas anteriormente
    if os.path.isfile(os.path.join(locationPath, r'src\data\configs.txt')):
        logging.info('Carregando Configurações Padrão')
        with open(os.path.join(locationPath, r'src\data\configs.txt')) as fileObject:
            itemConfigs = fileObject.readlines()
            itemConfigs = [line.rstrip() for line in itemConfigs]
            configs = []
            temp = {}
            for item in itemConfigs:
                if item == '':
                    configs.append(temp)
                    temp = {}
                else:
                    item = item.split(' ')
                    if len(item) > 2:
                        item[1] = ' '.join(item[1:])
                    temp[item[0][:-1]] = item[1]
            if temp:
                configs.append(temp)
        
        for item in previewFrames:
            logging.info(f'Configurações do frame: *{item["frame"].getTitle()[:-1]}* carregadas')
            for config in configs:
                if item['frame'].getTitle() == config['campo']:
                    item['frame'].setCoordx(config['coordx'])
                    item['frame'].setCoordy(config['coordy'])
                    for frame in item['frame'].getSubFrames():
                        if frame['subField'] == '1 linha':
                            for key, value in config.items():
                                if '1' == key[0]:
                                    frame[key[1:]].setText(value)
                        elif frame['subField'] == '2 linhas':
                            for key, value in config.items():
                                if '2' == key[0]:
                                    frame[key[1:]].setText(value)
                        elif frame['subField'] == '3 linhas':
                            for key, value in config.items():
                                if '3' == key[0]:
                                    frame[key[1:]].setText(value)
                        elif frame['subField'] == '4 linhas':
                            for key, value in config.items():
                                if '4' == key[0]:
                                    frame[key[1:]].setText(value)


    adjustCanvas.grid_columnconfigure(0, weight=1)
    # Responsividade
    inputFrame.grid_columnconfigure([0,3], weight=0)
    inputFrame.grid_columnconfigure(1, weight=1)
    inputFrame.grid_columnconfigure(2, weight=3)
    inputFrame.grid_rowconfigure([0,1,2,3,4], pad=10)
    previewFrame.grid_columnconfigure(0, weight=1)
    previewTexts.grid_columnconfigure([0,7], weight=1)
    buttonFrame.grid_columnconfigure([0,1,2], weight=1)
    #previewTexts.grid_columnconfigure([0,1,2,3,4,5], weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)


    # Thread de verificações assíncronas
    thread = threading.Thread(target=_asyncio_thread)
    thread.start()

    root.protocol("WM_DELETE_WINDOW", onClosing)
    # Loop do tkinter
    root.mainloop()
