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
    
    def writeImage(self, image, text, textFont, coordx, coordy, anchor='ma', spacing=0):
        if '\n' in text:
            print('Entrou no multiline')
            self.multiLine(image).multiline_text((coordx, coordy), text, anchor=anchor, font=textFont, fill=(255, 255, 255), align="center", spacing=spacing)
        else:
            print(f'texto: {text} entrou em oneLine')
            self.oneLine(image).text((coordx, coordy), text, anchor=anchor,
               font=textFont, fill=(255, 255, 255))


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
    def __init__(self, master, name, row, column, padx=0, pady=0, bgColor='', fgColor='', columnspan = 1, sticky = EW, listInputs=[]):
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
        self.label.grid(row=self._row, column=self._column, columnspan=self._columnspan, sticky=self.sticky)
        self.label.bind("<Configure>", self.setSize)
        #self.label.columnconfigure(self._column, weight=2)
        logging.debug('*** Fim de Criação de Instância ***')

    def getValue(self):
        return self.label.cget("text")
    
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
    
    def removeWidget(self):
        self.label.grid_remove()


class Input(Entry):
    def __init__(self, master, width, row, column, textDefault = '', columnspan=1):
        logging.debug('*** Criando Instância de Input ***')
        logging.debug(f'Instância gerada no frame {master}, linha {row} e coluna {column}')
        super().__init__()
        self.__master = master
        self._width = width
        self._row = row
        self._column = column
        self.verification = FileVerification()
        
        self.input = Entry(self.__master, width=self._width)
        self.input.grid(row=self._row, column=self._column, columnspan=columnspan, sticky=EW)
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
    
    def removeWidget(self):
        self.input.grid_remove()

class AreaFrame(Frame):
    def __init__(self, master, frameTitle, campo, nameFrames, row, column, bgColor="gray", padx=10, pady=10, bd=3):
        logging.debug('*** Criando Instância de AreaFrame ***')
        logging.debug(f'Instância gerada no frame {master}, linha {row} e coluna {column}')
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
        logging.debug('*** Fim de Criação de Instância ***')

        for i in range(self._numFrames):
            # Exceções de 1 linha
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
                if self._nameFrames[i] == '4 linhas':
                    newFrame['inputCharacter2'].removeWidget()
                    newFrame.update({"inputCharacter2":Title(self.areaFrame, "-", 4, columnICharac2, padx=2, bgColor="gray", fgColor="white", columnspan=2, sticky=W)})
            newFrame["fieldName"] = self._frameTitle
            self.subFrames.append(newFrame)
        #for item in self.subFrames:
        #    item['labelCoordx'].config()
        
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
    def __init__(self, master, text, bgColor, fontColor, action, row, column, sticky=N, span=1, listInputs=[], paths=''):
        logging.debug('*** Criando Instância de ActionButton ***')
        logging.debug(f'Instância gerada no frame {master}, linha {row} e coluna {column}')
        super().__init__()
        self.__master = master
        self._action = action
        self.listInputs = listInputs
        self.pathMainFont = paths[0] if paths else ''
        self.pathItalicFont = paths[1] if paths else ''
        self.slice = SliceText()
        self.draw = ImageText()

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
        preview_image = Image.open(os.path.join(os.getcwd(), r'src/images/preview.png'))
        for item in self.listInputs:
            #if item['field'] == 'title' or item['field'] == 'genders':
            field = item['field']
            coordx = item['frame'].getCoordx()
            coordy = item['frame'].getCoordy()
            text = item['frame'].getText()
            for frames in item['frame'].getSubFrames():
                if frames['subField'] == '1 linha':
                    maxFont = int(frames['inputCharacter1'].getValue())
                    maxLine1 = int(frames['inputCharacter2'].getValue())
                    fontHeight1 = int(frames['inputFont'].getValue())
                    try:
                        fontHeight2 = int(frames['inputFont2'].getValue())
                    except:
                        fontHeight2 = 0
                elif frames['subField'] == '2 linhas':
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
                textToAdd = self.slice.threeSlice(text, len(text), maxLine1, maxLine2 if maxLine2 else 0, maxLine3 if maxLine3 else 0)
                print(f'Paramêtros de Texto: texto: {text}, tamanho: {len(text)}, LimitC2: {maxLine1}, LimitC3: {maxLine2}, limitC4: {maxLine3}, texto final: {textToAdd}, coordx: {coordx}, coordy: {coordy}, campo: {field}')
            else:
                textToAdd = self.slice.twoSlice(text, len(text), maxFont, maxLine1=maxLine1)
                print(f'Paramêtros de Texto: texto: {text}, tamanho: {len(text)}, LimitC1: {maxFont}, LimitC2: {maxLine1}, texto final: {textToAdd}, coordx: {coordx}, coordy: {coordy}, campo: {field}')

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
            
            print(f'Fonte Height definida: {previewFontHeight} com textSpacing: {textSpacing} para o texto: {textToAdd}')
            
            if field == 'title':
                preview_coordx = (int(coordx) / 1920 * 523) + 5
            else:
                preview_coordx = (int(coordx) / 1920 * 523) + 2
            preview_coordy = int(coordy) / 1080 * 300

            # Definindo a fonte
            if 'Animes' in field:
                textFont = self.draw.fontText(self.pathItalicFont, previewFontHeight, 'italic')
            else:
                textFont = self.draw.fontText(self.pathMainFont, previewFontHeight)

            # Editando a imagem
            self.draw.writeImage(preview_image, textToAdd, textFont, preview_coordx, preview_coordy, anchor='mm' if item['field'] == 'title' else 'ma', spacing=textSpacing if textSpacing else 0)
            """ 
                if isinstance(limitCharacter2, int):
                    
                    # Tratando texto
                    twoLines = ['title', 'genders', 'orinalSource', 'platform', 'premiere']
                    text = frames['inputCampo'].getValue()
                    if field in twoLines:
                        text = self.slice.twoSlice(text, len(text), int(frames['inputCharacter1'].getValue()))
                    else:
                        text = self.slice.threeSlice(text, len(text), int(frames['inputCharacter1'].getValue()), limitCharacter2)
                    #text_to_add = frames['inputCampo'].getValue()

                    # Coordenadas adaptadas pra preview
                    limitCharacter = int(frames['inputCharacter1'].getValue())
                    if len(text) <= limitCharacter:
                        previewFontHeight = round((int(frames['inputFont'].getValue()) / 1080) * 300)
                    elif len(text) > limitCharacter and len(text) <= int(frames['inputCharacter2'].getValue()):
                        previewFontHeight = round((int(frames['inputFont2'].getValue()) / 1080) * 300)
                    #preview_font_height = round((int(item['inputFont'].getValue()) / 1080) * 300)
                    preview_coordx = int(coordx) / 1920 * 523
                    preview_coordy = int(coordy) / 1080 * 300

                    # Definindo a fonte
                    text_font = ImageFont.truetype(os.path.join(os.getcwd(), r'src/fonts/coolvetica rg.otf'), previewFontHeight)

                    # Editando a imagem
                    preview_image_edit = ImageDraw.Draw(preview_image)
                    preview_image_edit.text((preview_coordx, preview_coordy), text, anchor="mm", font=text_font)


                    # Limpe a entry box
                    #item['inputCampo'].delete(0, END)
                    #item['inputCampo'].insert(0, "Saving File...")
                
                else:
                    pass
                """
        # Salvando a imagem
        preview_image.save(os.path.join(os.getcwd(), r'src/images/new_preview.png'))
        # Espere alguns segundos e mostre a imagem
        image_preview.after(2000, self.show_pic(os.path.join(os.getcwd(), r'src/images/new_preview.png')))

    def show_pic(self, pathNewPic):
        global new_preview
        new_preview = PhotoImage(file=pathNewPic)
        image_preview.config(image=new_preview)
    
    def setPaths(self, newPaths=''):
        self.pathMainFont = newPaths[0] if newPaths else ''
        self.pathItalicFont = newPaths[1] if newPaths else ''


# Funções Assíncronas de Check-up
async def verifyInputs():
    while True:
        try:
            for item in inputs:
                # Passando os paths para o escopo global do programa
                global pathImageBase, pathFontPrincipal, pathFontItalic, pathDirectory
                if item['type'] == 'image':
                    pathImageBase = item['input'].getValue()
                elif item['type'] == 'font1':
                    pathFontPrincipal = item['input'].getValue()
                elif item['type'] == 'font2':
                    pathFontItalic = item['input'].getValue()
                elif item['type'] == 'directory':
                    pathDirectory = item['input'].getValue()
                buttonDemo.setPaths((pathFontPrincipal, pathFontItalic))
                # Verificação de validade
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

                elif 'font' in item['type']:
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
            for item in previewFrames:
                for frame in item['frame'].getSubFrames():
                    if frame["subField"] == "1 linha":
                        if frame["inputCharacter2"].getValue():
                            for second_frame in item['frame'].getSubFrames():
                                if second_frame["subField"] == "2 linhas":
                                    second_frame["inputCharacter1"].setName(frame["inputCharacter2"].getValue())
                        else:
                            for second_frame in item['frame'].getSubFrames():
                                if second_frame["subField"] == "2 linhas":
                                    second_frame["inputCharacter1"].setName("0")
                    elif frame["subField"] == "2 linhas":
                        if frame["inputCharacter2"].getValue():
                            for second_frame in item['frame'].getSubFrames():
                                if second_frame["subField"] == "3 linhas":
                                    second_frame["inputCharacter1"].setName(frame["inputCharacter2"].getValue())
                        else:
                            for second_frame in item['frame'].getSubFrames():
                                if second_frame["subField"] == "3 linhas":
                                    second_frame["inputCharacter1"].setName("0")
                    elif frame["subField"] == "3 linhas":
                        if frame["inputCharacter2"].getValue():
                            for second_frame in item['frame'].getSubFrames():
                                if second_frame["subField"] == "4 linhas":
                                    second_frame["inputCharacter1"].setName(frame["inputCharacter2"].getValue())
                        else:
                            for second_frame in item['frame'].getSubFrames():
                                if second_frame["subField"] == "4 linhas":
                                    second_frame["inputCharacter1"].setName("0")
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
    dj = (700, 1000)
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
            "type": 'font1',
            "label":Title(input_frame, "Fonte Principal:", 1, 1),
            "input":Input(input_frame, "50", 1, 2, r'{}'.format(os.path.join(os.getcwd(), r"src\fonts\coolvetica rg.otf"))),
            "warning":VisualWarning(input_frame, r'{}'.format(os.path.join(os.getcwd(), r"src\icons\cancel.png")), 1, 0),
            "button":SearchButton(input_frame, "...", 4, 2, 1, 1, 3),
        },
        {
            "type": 'font2',
            "label":Title(input_frame, "Fonte com Itálico:", 2, 1),
            "input":Input(input_frame, "50", 2, 2, r'{}'.format(os.path.join(os.getcwd(), r"src\fonts\coolvetica rg it.otf"))),
            "warning":VisualWarning(input_frame, r'{}'.format(os.path.join(os.getcwd(), r"src\icons\cancel.png")), 2, 0),
            "button":SearchButton(input_frame, "...", 4, 2, 2, 2, 3),
        },
        {
            "type": 'directory',
            "label":Title(input_frame, "Local de Destino:", 3, 1),
            "input":Input(input_frame, "50", 3, 2, r'{}'.format(os.path.join(os.getcwd(), r"src\images"))),
            "warning":VisualWarning(input_frame, r'{}'.format(os.path.join(os.getcwd(), r"src\icons\cancel.png")), 3, 0),
            "button":SearchButton(input_frame, "...", 4, 2, 3, 3, 3),
        },
        {
            "type": 'text',
            "label":Title(input_frame, "Info Animes:", 4, 1),
            "input":Input(input_frame, "50", 4, 2, r'{}'.format(os.path.join(os.getcwd(), r"src\data\text.txt"))),
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
            "title":Title(preview_texts, "1. Título:", 0, 0, padx=5, sticky=W),
            "input":Input(preview_texts, "40", 0, 1),
            "size":Title(preview_texts, "", 0, 2),
        },
        {
            "field": "genders",
            "title":Title(preview_texts, "2. Gêneros:", 1, 0, padx=5, sticky=W),
            "input":Input(preview_texts, "40", 1, 1),
            "size":Title(preview_texts, "", 1, 2),
        },
        {
            "field": "studioName",
            "title":Title(preview_texts, "3. Nome do Estúdio:", 2, 0, padx=5, sticky=W),
            "input":Input(preview_texts, "40", 2, 1),
            "size":Title(preview_texts, "", 2, 2),
        },
        {
            "field": "studioAnimes",
            "title":Title(preview_texts, "4. Animes do Estúdio:", 3, 0, padx=5, sticky=W),
            "input":Input(preview_texts, "40", 3, 1),
            "size":Title(preview_texts, "", 3, 2),
        },
        {
            "field": "directorName",
            "title":Title(preview_texts, "5. Nome do Diretor:", 4, 0, padx=5, sticky=W),
            "input":Input(preview_texts, "40", 4, 1),
            "size":Title(preview_texts, "", 4, 2),
        },
        {
            "field": "directorAnimes",
            "title":Title(preview_texts, "6. Obras do Diretor:", 5, 0, padx=5, sticky=W),
            "input":Input(preview_texts, "40", 5, 1),
            "size":Title(preview_texts, "", 5, 2),
        },
        {
            "field": "composerName",
            "title":Title(preview_texts, "7. Nome do Compositor:", 0, 3, padx=5, sticky=W),
            "input":Input(preview_texts, "40", 0, 4),
            "size":Title(preview_texts, "", 0, 5),
        },
        {
            "field": "ComposerAnimes",
            "title":Title(preview_texts, "8. Obras do Compositor:", 1, 3, padx=5, sticky=W),
            "input":Input(preview_texts, "40", 1, 4),
            "size":Title(preview_texts, "", 1, 5),
        },
        {
            "field": "originalSource",
            "title":Title(preview_texts, "9. Origem:", 2, 3, padx=5, sticky=W),
            "input":Input(preview_texts, "40", 2, 4),
            "size":Title(preview_texts, "", 2, 5),
        },
        {
            "field": "platform",
            "title":Title(preview_texts, "10. Plataforma:", 3, 3, padx=5, sticky=W),
            "input":Input(preview_texts, "40", 3, 4),
            "size":Title(preview_texts, "", 3, 5),
        },
        {
            "field": "premiere",
            "title":Title(preview_texts, "11. Data de Estréia:", 4, 3, padx=5, sticky=W),
            "input":Input(preview_texts, "40", 4, 4),
            "size":Title(preview_texts, "", 4, 5),
        },
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
    previewFrames = [
        {
            "field": "title",
            "frame": AreaFrame(adjust_frame, "Título:", preview_inputs[0]['input'], ("1 linha", "2 linhas"), 0, 0)
        },
        {
            "field": "genders",
            "frame": AreaFrame(adjust_frame, "Gêneros:", preview_inputs[1]['input'], ("1 linha", "2 linhas"), 1, 0)
        },
        {
            "field": "studioName",
            "frame": AreaFrame(adjust_frame, "Nome do Estúdio:", preview_inputs[2]['input'], ("1 linha",), 2, 0)
        },
        {
            "field": "studioAnimes",
            "frame": AreaFrame(adjust_frame, "Animes do Estúdio:", preview_inputs[3]['input'], ("1 linha", "2 linhas", "3 linhas", "4 linhas"), 3, 0)
        },
        {
            "field": "directorName",
            "frame": AreaFrame(adjust_frame, "Nome do Diretor:", preview_inputs[4]['input'], ("1 linha",), 4, 0)
        },
        {
            "field": "directorAnimes",
            "frame": AreaFrame(adjust_frame, "Animes do Diretor:", preview_inputs[5]['input'], ("1 linha", "2 linhas", "3 linhas", "4 linhas"), 5, 0)
        },
        {
            "field": "composerName",
            "frame": AreaFrame(adjust_frame, "Nome do Compositor:", preview_inputs[6]['input'], ("1 linha",), 6, 0)
        },
        {
            "field": "composerAnimes",
            "frame": AreaFrame(adjust_frame, "Animes do Compositor:", preview_inputs[7]['input'], ("1 linha", "2 linhas", "3 linhas", "4 linhas"), 7, 0)
        },
        {
            "field": "originalSource",
            "frame": AreaFrame(adjust_frame, "Origem:", preview_inputs[8]['input'], ("1 linha",), 8, 0)
        },        
        {
            "field": "composerName",
            "frame": AreaFrame(adjust_frame, "Plataforma:", preview_inputs[9]['input'], ("1 linha",), 9, 0)
        },        
        {
            "field": "composerName",
            "frame": AreaFrame(adjust_frame, "Data de Estréia:", preview_inputs[10]['input'], ("1 linha",), 10, 0)
        },        

    ]

    # Barra de Scroll
    scrollbar = Scrollbar(root, orient='vertical')
    scrollbar.grid(row=3, column=1, sticky=NSEW)

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
    #dicioCoords = [{"field": "title", "coordx": titles_frame.getCoordx(), "coordy": titles_frame.getCoordy(),}]
    pathFontItalic = ''
    pathFontPrincipal = ''
    pathImageBase = ''
    pathDirectory = ''

    buttonDemo = ActionButton(root, "Demonstração", bgColor="lightyellow", fontColor="black", action="preview", row=4, column=0, sticky=EW, listInputs=previewFrames, paths=(pathFontPrincipal, pathFontItalic))
    """ buttonDemo = Button(root, text="Demonstração", command=lambda: add_it())
    buttonDemo.grid(row=4, column=0, sticky=EW) """

    #---------------------------------------------------------------------------
    # Ajustes salvos
    for item in previewFrames:
        if item['frame'].getTitle() == 'Título:':
            item['frame'].setCoordx('960')
            item['frame'].setCoordy('102')
            for frame in item['frame'].getSubFrames():
                if frame['subField'] == '1 linha':
                    frame['inputCharacter1'].setText('40')
                    frame['inputCharacter2'].setText('50')
                    frame['inputFont'].setText('110')
                    frame['inputFont2'].setText('75')
                elif frame['subField'] == '2 linhas':
                    frame['inputFont'].setText('75')
                    frame['inputSpacing'].setText('0')
        elif item['frame'].getTitle() == 'Gêneros:':
            item['frame'].setCoordx('393')
            item['frame'].setCoordy('272')
            for frame in item['frame'].getSubFrames():
                if frame['subField'] == '1 linha':
                    frame['inputCharacter1'].setText('40')
                    frame['inputCharacter2'].setText('50')
                    frame['inputFont'].setText('40')
                    frame['inputFont2'].setText('35')
                elif frame['subField'] == '2 linhas':
                    frame['inputFont'].setText('35')
                    frame['inputSpacing'].setText('0')
        elif item['frame'].getTitle() == 'Nome do Estúdio:':
            item['frame'].setCoordx('393')
            item['frame'].setCoordy('440')
            for frame in item['frame'].getSubFrames():
                if frame['subField'] == '1 linha':
                    frame['inputCharacter1'].setText('40')
                    frame['inputCharacter2'].setText('50')
                    frame['inputFont'].setText('40')
                    frame['inputFont2'].setText('35')
        elif item['frame'].getTitle() == 'Nome do Diretor:':
            item['frame'].setCoordx('393')
            item['frame'].setCoordy('622')
            for frame in item['frame'].getSubFrames():
                if frame['subField'] == '1 linha':
                    frame['inputCharacter1'].setText('40')
                    frame['inputCharacter2'].setText('50')
                    frame['inputFont'].setText('40')
                    frame['inputFont2'].setText('35')
        elif item['frame'].getTitle() == 'Nome do Compositor:':
            item['frame'].setCoordx('393')
            item['frame'].setCoordy('811')
            for frame in item['frame'].getSubFrames():
                if frame['subField'] == '1 linha':
                    frame['inputCharacter1'].setText('40')
                    frame['inputCharacter2'].setText('50')
                    frame['inputFont'].setText('40')
                    frame['inputFont2'].setText('35')
        elif item['frame'].getTitle() == 'Origem:':
            item['frame'].setCoordx('393')
            item['frame'].setCoordy('998')
            for frame in item['frame'].getSubFrames():
                if frame['subField'] == '1 linha':
                    frame['inputCharacter1'].setText('40')
                    frame['inputCharacter2'].setText('50')
                    frame['inputFont'].setText('40')
                    frame['inputFont2'].setText('35')
        elif item['frame'].getTitle() == 'Plataforma:':
            item['frame'].setCoordx('1064')
            item['frame'].setCoordy('1013')
            for frame in item['frame'].getSubFrames():
                if frame['subField'] == '1 linha':
                    frame['inputCharacter1'].setText('40')
                    frame['inputCharacter2'].setText('50')
                    frame['inputFont'].setText('40')
                    frame['inputFont2'].setText('35')
        elif item['frame'].getTitle() == 'Data de Estréia:':
            item['frame'].setCoordx('1726')
            item['frame'].setCoordy('978')
            for frame in item['frame'].getSubFrames():
                if frame['subField'] == '1 linha':
                    frame['inputCharacter1'].setText('40')
                    frame['inputCharacter2'].setText('50')
                    frame['inputFont'].setText('40')
                    frame['inputFont2'].setText('35')
        elif item['frame'].getTitle() == 'Animes do Estúdio:':
            item['frame'].setCoordx('393')
            item['frame'].setCoordy('477')
            for frame in item['frame'].getSubFrames():
                if frame['subField'] == '1 linha':
                    frame['inputCharacter2'].setText('50')
                    frame['inputFont'].setText('40')
                    frame['inputSpacing'].setText('0')
                elif frame['subField'] == '2 linhas':
                    frame['inputCharacter2'].setText('55')
                    frame['inputFont'].setText('35')
                    frame['inputSpacing'].setText('0')
                elif frame['subField'] == '3 linhas':
                    frame['inputCharacter2'].setText('60')
                    frame['inputFont'].setText('35')
                    frame['inputSpacing'].setText('0')
                elif frame['subField'] == '4 linhas':
                    frame['inputFont'].setText('35')
                    frame['inputSpacing'].setText('0')
        elif item['frame'].getTitle() == 'Animes do Diretor:':
            item['frame'].setCoordx('393')
            item['frame'].setCoordy('680')
            for frame in item['frame'].getSubFrames():
                if frame['subField'] == '1 linha':
                    frame['inputCharacter2'].setText('50')
                    frame['inputFont'].setText('40')
                    frame['inputSpacing'].setText('0')
                elif frame['subField'] == '2 linhas':
                    frame['inputCharacter2'].setText('55')
                    frame['inputFont'].setText('35')
                    frame['inputSpacing'].setText('0')
                elif frame['subField'] == '3 linhas':
                    frame['inputCharacter2'].setText('60')
                    frame['inputFont'].setText('35')
                    frame['inputSpacing'].setText('0')
                elif frame['subField'] == '4 linhas':
                    frame['inputFont'].setText('35')
                    frame['inputSpacing'].setText('0')
        elif item['frame'].getTitle() == 'Animes do Compositor:':
            item['frame'].setCoordx('393')
            item['frame'].setCoordy('848')
            for frame in item['frame'].getSubFrames():
                if frame['subField'] == '1 linha':
                    frame['inputCharacter2'].setText('50')
                    frame['inputFont'].setText('40')
                    frame['inputSpacing'].setText('0')
                elif frame['subField'] == '2 linhas':
                    frame['inputCharacter2'].setText('55')
                    frame['inputFont'].setText('35')
                    frame['inputSpacing'].setText('0')
                elif frame['subField'] == '3 linhas':
                    frame['inputCharacter2'].setText('60')
                    frame['inputFont'].setText('35')
                    frame['inputSpacing'].setText('0')
                elif frame['subField'] == '4 linhas':
                    frame['inputFont'].setText('35')
                    frame['inputSpacing'].setText('0')


    adjust_canvas.grid_columnconfigure(0, weight=1)
    # Responsividade
    input_frame.grid_columnconfigure([0,3], weight=0)
    input_frame.grid_columnconfigure(1, weight=1)
    input_frame.grid_columnconfigure(2, weight=3)
    input_frame.grid_rowconfigure([0,1,2,3,4], pad=10)
    preview_frame.grid_columnconfigure(0, weight=1)
    #preview_texts.grid_columnconfigure([0,1,2,3,4,5], weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)


    # Thread de verificações assíncronas
    thread = threading.Thread(target=_asyncio_thread)
    thread.start()

    root.protocol("WM_DELETE_WINDOW", onClosing)
    # Loop do tkinter
    root.mainloop()