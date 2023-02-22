"""
# Importando módulos necessários
from PIL import Image, ImageDraw, ImageFont
import os

# Flag para parar os laços
Flag = True

# Pede e confere os paths de arquivo
while True:
    try:
        path_image = r'{}'.format(input(
                            'Qual o path da imagem base (1920x1080) ?'))
        break
    except:
        pass

 
# Open an Image
image = Image.open(r'C:/Users/Riku Aoki/Documents/Programas/CDT/Image/cdt.png')
 
# Call draw Method to add 2D graphics in an image
Img1 = ImageDraw.Draw(image)
 
# Custom font style and font size
myFont = ImageFont.truetype(
    r'C:/Users/Riku Aoki/Documents/Programas/CDT/Image/coolvetica_rg.otf', 50)

# texto
text = "Kinsou no Vermeil: Gakeppuchi Majutsushi wa"
text2 = "Saikyou no Yakusai to Mahou Sekai wo tsukisusumu"

# Add Text to an image
Img1.text((960, 100),
          text,
          anchor="mm",
          font=myFont, fill =(255, 255, 255))
 
# Display edited image
image.show()
 
# Save the edited image
#image.save(r'C:/Users/Riku Aoki/Documents/Programas/CDT/Image/teste.png')
25 - 175
"""
"""
import os
import re
from tkinter import *
from tkinter.tix import *

class FileVerification:
    def __init__(self):
        self.extensionRegex = re.compile(r'[^.]+$')
        
    def verify(self, path):
        if os.path.isfile(path) or os.path.isdir(path):
            return True
        else:
            return False
        
    def check_font_file(self, path):
        extension = self.extensionRegex.search(path).group()
        if extension in ['otf', 'ttf']:
            return True
        else:
            return False

class MyApp:
    def __init__(self, master):
        self.master = master
        self.master.title("File Verification Interface")
        self.master.geometry("300x200")
        self.master.resizable(False, False)
        
        self.file_verification = FileVerification()
        
        self.base_image_label = Label(master, text="Imagem Base")
        self.base_image_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        
        self.base_image_entry = Entry(master)
        self.base_image_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.principal_font_label = Label(master, text="Fonte Principal")
        self.principal_font_label.grid(row=1, column=0, padx=5, pady=5, sticky=W)
        
        self.principal_font_entry = Entry(master)
        self.principal_font_entry.grid(row=1, column=1, padx=5, pady=5)
        
        self.italic_font_label = Label(master, text="Fonte com Itálico")
        self.italic_font_label.grid(row=2, column=0, padx=5, pady=5, sticky=W)
        
        self.italic_font_entry = Entry(master)
        self.italic_font_entry.grid(row=2, column=1, padx=5, pady=5)
        
        self.destiny_path_label = Label(master, text="Local de Destino")
        self.destiny_path_label.grid(row=3, column=0, padx=5, pady=5, sticky=W)
        
        self.destiny_path_entry = Entry(master)
        self.destiny_path_entry.grid(row=3, column=1, padx=5, pady=5)
        
        self.verify_button = Button(master, text="Verificar", command=self.verify_files())
        self.verify_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        
        def verify_files(self):
            base_image_path = self.base_image_entry.get()
            principal_font_path = self.principal_font_entry.get()
            italic_font_path = self.italic_font_entry.get()
            destiny_path = self.destiny_path_entry.get()
        
            if self.file_verification.verify(base_image_path):
                print("Imagem Base: OK")
            else:
                print("Imagem Base: Arquivo não encontrado")
        
            if self.file_verification.check_font_file(principal_font_path):
                print("Fonte Principal: OK")
            else:
                print("Fonte Principal: Arquivo não encontrado ou formato inválido")
        
            if self.file_verification.check_font_file(italic_font_path):
                print("Fonte com Itálico: OK")
            else:
                print("Fonte com Itálico: Arquivo não encontrado ou formato inválido")
        
            if self.file_verification.verify(destiny_path):
                print("Local de Destino: OK")
            else:
                print("Local de Destino: Pasta não encontrada")

root = Tk()
app = MyApp(root)
root.mainloop()
"""

print('sim')
