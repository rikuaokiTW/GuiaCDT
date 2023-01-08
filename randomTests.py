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
