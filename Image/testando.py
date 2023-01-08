# Importando módulos necessários
from PIL import Image, ImageDraw, ImageFont
import os, re

# DEFs
def verificarArquivo(tipo):
    """
        Verifica se o caminho para cada arquivo está funcional e correto, retornando o necessário
    """
    # Regex pra testar extensões de arquivo
    extensionRegex = re.compile(r'[^.]+$')

    # Fluxo para verificação
    if tipo == 'imagem':
        while True:
            try:
                path_image = r'C:/Users/Riku Aoki/Documents/Programas/GuiaCDT/src/images/test-cdt.png'
                #path_image = r'{}'.format(input('Qual o path da imagem base (1920x1080) ?'))
                if os.path.isfile(path_image):
                    extension = extensionRegex.search(path_image).group()
                    if extensionRegex.search(path_image).group() == 'png':
                        return path_image
                        break
                    else:
                        print('\nO arquivo encontrado tem extensão: .' + str(extension) +
                              '\nEu esperava a extensão ".png"\n')
                else:
                    print('\nEsperava algo como C:/Users/NameUser/Images/image.png, ' +
                          'porém, não encontrei uma imagem no path recebido\n')
                    
            except Exception as e:
                print('A operação falhou pois recebi o seguinte erro:')
                print(e)
    elif tipo == 'texto':
        while True:
            try:
                path_text = r'C:/Users/Riku Aoki/Documents/Programas/GuiaCDT/src/data/text.txt'
                #path_text = r'{}'.format(input('Qual o path do arquivo de texto com a info dos animes ?'))
                if os.path.isfile(path_text):
                    extension = extensionRegex.search(path_text).group()
                    if extensionRegex.search(path_text).group() == 'txt':
                        with open(path_text) as text_info:
                                text = text_info.read()
                                text = text.split('\n')
                        while '' in text:
                            text.remove('')
                        if len(text) % 11 == 0:
                            return text
                            break
                        else:
                            print('Parece que algum dos animes não está com as 11 informações exigidas, ' +
                                  'verifique e tente novamente.')
                    else:
                        print('\nO arquivo encontrado tem extensão: .' + str(extension) +
                              '\nEu esperava a extensão ".txt"\n')
                else:
                    print('\nEsperava algo como C:/Users/NameUser/Project/text.txt, ' +
                          'porém, não encontrei um arquivo .txt no path recebido\n')

            except Exception as e:
                print(e)
    else:
        print('Não trabalho com esse tipo, somente "texto" ou "imagem"')

def gerarDicio(animeInfos):
    # Dicionário que conterá todos os animes
    dicioList = {}
    # Informações a serem coletadas
    infoDicio = {
    'name':'',
    'genders':'',
    'studio':'',
    'studio_animes':'',
    'director':'',
    'director_animes':'',
    'composer':'',
    'composer_animes':'',
    'original_source':'',
    'platform':'',
    'premiere':''}
    # Contadores p/ gerenciamento de laço
    numLoop = 0
    contKey = 0
    contDicio = 0
    cont = 1
    # Adicionando informações
    for key in infoDicio.keys():
        for position in range(contKey, len(animeInfos), 11):
            new_key = key + str(cont)
            dicioList[new_key] = animeInfos[position]
            contDicio += 1
            numLoop += 1
            cont += 1
            if numLoop == int(len(text) / 11):
                cont = 1
                break
        numLoop = 0
        contKey += 1
        contDicio = 0
    return dicioList

# Pede e confere o path de imagem
path_image = verificarArquivo('imagem')

# Pede e confere o path de texto, retornando o texto com as informações
text = verificarArquivo('texto')

# Gerando lista com as informações
dicioList = gerarDicio(text)

# Definições de Fonte
def fonte(size, tipo = 'normal'):
    if tipo == 'normal':
        myFont = ImageFont.truetype(r'C:/Users/Riku Aoki/Documents/Programas/GuiaCDT/src/fonts/coolvetica rg.otf', size)
    elif tipo == 'italic':
        myFont = ImageFont.truetype(r'C:/Users/Riku Aoki/Documents/Programas/GuiaCDT/src/fonts/coolvetica rg it.otf', size)
    elif tipo == 'condensed':
        myFont = ImageFont.truetype(r'C:/Users/Riku Aoki/Documents/Programas/GuiaCDT/src/fonts/coolvetica condensed rg.otf', size)
    return myFont

# Quebra Texto
def quebraTexto(item, text, maxCharac):
    """
        Recebe o item, ou seja, de onde é o texto, e o número
    máximo de caracteres ideais nessa área, podendo efetuar o corte.
    """
    contDecre = maxCharac
    length = len(text)
    cut = maxCharac
    cut2 = maxCharac * 2
    cut3 = maxCharac * 3
    # Para a área title
    if item == 'title':
        if length <= maxCharac:
            x = 960
            y = 102
            return x, y, text
        elif length > maxCharac:
            texto = list(text)
            for x in range(contDecre):
                if texto[cut] == ' ':
                    break
                else:
                    cut -= 1
            coordx = 960
            coord1y = 64
            coord2y = 129
            texto1 = text[:cut]
            texto2 = text[cut:]
            return coordx, coord1y, coord2y, texto1, texto2
        
    # Para a área genders
    elif item == 'genders':
        if length <= maxCharac:
            x = 390
            y = 306
            return x, y, text
        elif length > maxCharac:
            texto = list(text)
            for x in range(contDecre):
                if texto[cut] == ' ':
                    break
                else:
                    cut -= 1
            coordx = 390
            coord1y = 306
            coord2y = 350
            texto1 = text[:cut]
            texto2 = text[cut:]
            return coordx, coord1y, coord2y, texto1, texto2

    # Para a área de estúdio
    elif item == 'studio_animes':
        if length <= maxCharac:
            x = 390
            y = 487
            return x, y, text
        # Caso o área seja de 2 linhas
        elif length > maxCharac and length <= maxCharac * 2:
            texto = list(text)
            for x in range(contDecre):
                if texto[cut] == ' ':
                    break
                else:
                    cut -= 1
            coordx = 390
            coord1y = 487
            coord2y = 521
            texto1 = text[:cut]
            texto2 = text[cut:]
            return coordx, coord1y, coord2y, texto1, texto2
        # Caso o área seja de 3 linhas
        elif length > maxCharac * 2 and length <= maxCharac * 3:
            texto = list(text)
            for x in range(contDecre):
                if texto[cut] == ' ':
                    break
                else:
                    cut -= 1
            for x in range(contDecre):
                if texto[cut2] == ' ':
                    break
                else:
                    cut2 -= 1
            coordx = 390
            coord1y = 487
            coord2y = 521
            coord3y = 552
            texto1 = text[:cut]
            texto2 = text[cut:cut2]
            texto3 = text[cut2:]
            return coordx, coord1y, coord2y, coord3y, texto1, texto2, texto3
        # Caso o área seja de 4 linhas
        elif length > maxCharac * 3:
            texto = list(text)
            for x in range(contDecre):
                if texto[cut] == ' ':
                    break
                else:
                    cut -= 1
            for x in range(contDecre):
                if texto[cut2] == ' ':
                    break
                else:
                    cut2 -= 1
            for x in range(contDecre):
                if texto[cut3] == ' ':
                    break
                else:
                    cut3 -= 1
            coordx = 390
            coord1y = 464
            coord2y = 493
            coord3y = 522
            coord4y = 547
            texto1 = text[:cut]
            texto2 = text[cut:cut2]
            texto3 = text[cut2:cut3]
            texto4 = text[cut3:]
            return coordx, coord1y, coord2y, coord3y, coord4y, texto1, texto2, texto3, texto4

    # Para área de diretor
    elif item == 'director_animes':
        if length <= maxCharac:
            x = 390
            y = 670
            return x, y, text
        # Caso o área seja de 2 linhas
        elif length > maxCharac and length <= maxCharac * 2:
            texto = list(text)
            for x in range(contDecre):
                if texto[cut] == ' ':
                    break
                else:
                    cut -= 1
            coordx = 390
            coord1y = 670
            coord2y = 702
            texto1 = text[:cut]
            texto2 = text[cut:]
            return coordx, coord1y, coord2y, texto1, texto2
        # Caso o área seja de 3 linhas
        elif length > maxCharac * 2 and length <= maxCharac * 3:
            texto = list(text)
            for x in range(contDecre):
                if texto[cut] == ' ':
                    break
                else:
                    cut -= 1
            for x in range(contDecre):
                if texto[cut2] == ' ':
                    break
                else:
                    cut2 -= 1
            coordx = 390
            coord1y = 670
            coord2y = 702
            coord3y = 733
            texto1 = text[:cut]
            texto2 = text[cut:cut2]
            texto3 = text[cut2:]
            return coordx, coord1y, coord2y, coord3y, texto1, texto2, texto3
        # Caso o área seja de 4 linhas
        elif length > maxCharac * 3:
            texto = list(text)
            for x in range(contDecre):
                if texto[cut] == ' ':
                    break
                else:
                    cut -= 1
            for x in range(contDecre):
                if texto[cut2] == ' ':
                    break
                else:
                    cut2 -= 1
            for x in range(contDecre):
                if texto[cut3] == ' ':
                    break
                else:
                    cut3 -= 1
            coordx = 390
            coord1y = 654
            coord2y = 683
            coord3y = 710
            coord4y = 737
            texto1 = text[:cut]
            texto2 = text[cut:cut2]
            texto3 = text[cut2:cut3]
            texto4 = text[cut3:]
            return coordx, coord1y, coord2y, coord3y, coord4y, texto1, texto2, texto3, texto4

    # Para área de compositor
    elif item == 'composer_animes':
        if length <= maxCharac:
            x = 390
            y = 858
            return x, y, text
        # Caso o área seja de 2 linhas
        elif length > maxCharac and length <= maxCharac * 2:
            texto = list(text)
            for x in range(contDecre):
                if texto[cut] == ' ':
                    break
                else:
                    cut -= 1
            coordx = 390
            coord1y = 858
            coord2y = 891
            texto1 = text[:cut]
            texto2 = text[cut:]
            return coordx, coord1y, coord2y, texto1, texto2
        # Caso o área seja de 3 linhas
        elif length > maxCharac * 2 and length <= maxCharac * 3:
            texto = list(text)
            for x in range(contDecre):
                if texto[cut] == ' ':
                    break
                else:
                    cut -= 1
            for x in range(contDecre):
                if texto[cut2] == ' ':
                    break
                else:
                    cut2 -= 1
            coordx = 390
            coord1y = 858
            coord2y = 891
            coord3y = 923
            texto1 = text[:cut]
            texto2 = text[cut:cut2]
            texto3 = text[cut2:]
            return coordx, coord1y, coord2y, coord3y, texto1, texto2, texto3
        # Caso o área seja de 4 linhas
        elif length > maxCharac * 3:
            texto = list(text)
            for x in range(contDecre):
                if texto[cut] == ' ':
                    break
                else:
                    cut -= 1
            for x in range(contDecre):
                if texto[cut2] == ' ':
                    break
                else:
                    cut2 -= 1
            for x in range(contDecre):
                if texto[cut3] == ' ':
                    break
                else:
                    cut3 -= 1
            coordx = 390
            coord1y = 841
            coord2y = 870
            coord3y = 899
            coord4y = 924
            texto1 = text[:cut]
            texto2 = text[cut:cut2]
            texto3 = text[cut2:cut3]
            texto4 = text[cut3:]
            return coordx, coord1y, coord2y, coord3y, coord4y, texto1, texto2, texto3, texto4
    else:
        print(length, maxCharac)


# Adicionando itens e fazendo as imagens
for numAnime in range(1, int(len(text) / 11 + 1)):
    # Cortes
    corte_titulo = 38
    corte_lateral = 40
    # Evitando erro de concatenação
    numAnime = str(numAnime)
    # Símbolos não aceitos como nome em arquivo
    forbidden = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']

    # Definindo chaves corretas
    name = 'name' + numAnime
    genders = 'genders' + numAnime
    studio = 'studio' + numAnime
    studio_animes = 'studio_animes' + numAnime
    director = 'director' + numAnime
    director_animes = 'director_animes' + numAnime
    composer = 'composer' + numAnime
    composer_animes = 'composer_animes' + numAnime
    original_source = 'original_source' + numAnime
    platform = 'platform' + numAnime
    premiere = 'premiere' + numAnime

    # Nome final da imagem
    final_name = list(dicioList[name])
    for symbol in forbidden:
        try:
            while symbol in final_name:
                final_name.remove(symbol)
        except:
            pass
    final_name = ''.join(final_name)
    name_image = os.path.join(r'C:\\Users\\Riku Aoki\\Documents\\Programas\\GuiaCDT\\src\\images',
                              final_name)
    
    # Abre a imagem escolhida
    image = Image.open(path_image)

    # Chama o método "draw" da biblioteca para adicionar gráficos 2D em uma imagem
    imageDraw = ImageDraw.Draw(image)

    # Identificador de anime
    numAnime = str(numAnime)

    # def Tittle
    dados = quebraTexto('title', dicioList[name], corte_titulo)
    if len(dados) == 3:
        imageDraw.text((dados[0], dados[1]), dados[2], anchor='mm',
               font=fonte(110), fill=(255, 255, 255))
    elif len(dados) == 5:
        imageDraw.text((dados[0], dados[1]), dados[3], anchor='mm',
               font=fonte(75), fill=(255, 255, 255))
        imageDraw.text((dados[0], dados[2]), dados[4], anchor='mm',
               font=fonte(75), fill=(255, 255, 255))

    # def Genders
    dados = quebraTexto('genders', dicioList[genders], corte_lateral)
    if len(dados) == 3:
        imageDraw.text((dados[0], dados[1]), dados[2], anchor='mm',
               font=fonte(40), fill=(255, 255, 255))
    elif len(dados) == 5:
        imageDraw.text((dados[0], dados[1]), dados[3], anchor='mm',
               font=fonte(40), fill=(255, 255, 255))
        imageDraw.text((dados[0], dados[2]), dados[4], anchor='mm',
               font=fonte(40), fill=(255, 255, 255))

    # def Studio
    dados = quebraTexto('studio_animes', dicioList[studio_animes], corte_lateral)
    if len(dados) == 3:
        imageDraw.text((390, 453), dicioList[studio], anchor='mm',
               font=fonte(40), fill=(255, 255, 255)) # Atenção com o tamanho da fonte, pode mudar
        imageDraw.text((dados[0], dados[1]), dados[2], anchor='mm',
               font=fonte(35, tipo = 'italic'), fill=(255, 255, 255))
    elif len(dados) == 5:
        imageDraw.text((390, 453), dicioList[studio], anchor='mm',
               font=fonte(40), fill=(255, 255, 255)) # Atenção com o tamanho da fonte, pode mudar
        imageDraw.text((dados[0], dados[1]), dados[3], anchor='mm',
               font=fonte(35, tipo = 'italic'), fill=(255, 255, 255))
        imageDraw.text((dados[0], dados[2]), dados[4], anchor='mm',
               font=fonte(35, tipo = 'italic'), fill=(255, 255, 255))
    elif len(dados) == 7:
        imageDraw.text((390, 453), dicioList[studio], anchor='mm',
               font=fonte(40), fill=(255, 255, 255)) # Atenção com o tamanho da fonte, pode mudar
        imageDraw.text((dados[0], dados[1]), dados[4], anchor='mm',
               font=fonte(35, tipo = 'italic'), fill=(255, 255, 255))
        imageDraw.text((dados[0], dados[2]), dados[5], anchor='mm',
               font=fonte(35, tipo = 'italic'), fill=(255, 255, 255))
        imageDraw.text((dados[0], dados[3]), dados[6], anchor='mm',
               font=fonte(35, tipo = 'italic'), fill=(255, 255, 255))
    elif len(dados) == 9:
        imageDraw.text((390, 440), dicioList[studio], anchor='mm',
               font=fonte(31), fill=(255, 255, 255)) # Atenção com o tamanho da fonte, pode mudar
        imageDraw.text((dados[0], dados[1]), dados[5], anchor='mm',
               font=fonte(30, tipo = 'italic'), fill=(255, 255, 255))
        imageDraw.text((dados[0], dados[2]), dados[6], anchor='mm',
               font=fonte(30, tipo = 'italic'), fill=(255, 255, 255))
        imageDraw.text((dados[0], dados[3]), dados[7], anchor='mm',
               font=fonte(30, tipo = 'italic'), fill=(255, 255, 255))
        imageDraw.text((dados[0], dados[4]), dados[8], anchor='mm',
               font=fonte(30, tipo = 'italic'), fill=(255, 255, 255))

    # def director
    dados = quebraTexto('director_animes', dicioList[director_animes], corte_lateral)
    if len(dados) == 3:
        imageDraw.text((390, 635), dicioList[director], anchor='mm',
               font=fonte(40), fill=(255, 255, 255)) # Atenção com o tamanho da fonte, pode mudar
        imageDraw.text((dados[0], dados[1]), dados[2], anchor='mm',
               font=fonte(35, tipo = 'italic'), fill=(255, 255, 255))
    elif len(dados) == 5:
        imageDraw.text((390, 635), dicioList[director], anchor='mm',
               font=fonte(40), fill=(255, 255, 255)) # Atenção com o tamanho da fonte, pode mudar
        imageDraw.text((dados[0], dados[1]), dados[3], anchor='mm',
               font=fonte(35, tipo = 'italic'), fill=(255, 255, 255))
        imageDraw.text((dados[0], dados[2]), dados[4], anchor='mm',
               font=fonte(35, tipo = 'italic'), fill=(255, 255, 255))
    elif len(dados) == 7:
        imageDraw.text((390, 635), dicioList[director], anchor='mm',
               font=fonte(40), fill=(255, 255, 255)) # Atenção com o tamanho da fonte, pode mudar
        imageDraw.text((dados[0], dados[1]), dados[4], anchor='mm',
               font=fonte(35, tipo = 'italic'), fill=(255, 255, 255))
        imageDraw.text((dados[0], dados[2]), dados[5], anchor='mm',
               font=fonte(35, tipo = 'italic'), fill=(255, 255, 255))
        imageDraw.text((dados[0], dados[3]), dados[6], anchor='mm',
               font=fonte(35, tipo = 'italic'), fill=(255, 255, 255))
    elif len(dados) == 9:
        imageDraw.text((390, 630), dicioList[director], anchor='mm',
               font=fonte(31), fill=(255, 255, 255)) # Atenção com o tamanho da fonte, pode mudar
        imageDraw.text((dados[0], dados[1]), dados[5], anchor='mm',
               font=fonte(30, tipo = 'italic'), fill=(255, 255, 255))
        imageDraw.text((dados[0], dados[2]), dados[6], anchor='mm',
               font=fonte(30, tipo = 'italic'), fill=(255, 255, 255))
        imageDraw.text((dados[0], dados[3]), dados[7], anchor='mm',
               font=fonte(30, tipo = 'italic'), fill=(255, 255, 255))
        imageDraw.text((dados[0], dados[4]), dados[8], anchor='mm',
               font=fonte(30, tipo = 'italic'), fill=(255, 255, 255))

    # def composer
    dados = quebraTexto('composer_animes', dicioList[composer_animes], corte_lateral)
    if len(dados) == 3:
        imageDraw.text((390, 824), dicioList[composer], anchor='mm',
               font=fonte(40), fill=(255, 255, 255))
        imageDraw.text((dados[0], dados[1]), dados[2], anchor='mm',
               font=fonte(35, tipo = 'italic'), fill=(255, 255, 255))
    elif len(dados) == 5:
        imageDraw.text((390, 824), dicioList[composer], anchor='mm',
               font=fonte(40), fill=(255, 255, 255))
        imageDraw.text((dados[0], dados[1]), dados[3], anchor='mm',
               font=fonte(35, tipo = 'italic'), fill=(255, 255, 255))
        imageDraw.text((dados[0], dados[2]), dados[4], anchor='mm',
               font=fonte(35, tipo = 'italic'), fill=(255, 255, 255))
    elif len(dados) == 7:
        imageDraw.text((390, 824), dicioList[composer], anchor='mm',
               font=fonte(40), fill=(255, 255, 255))
        imageDraw.text((dados[0], dados[1]), dados[4], anchor='mm',
               font=fonte(35, tipo = 'italic'), fill=(255, 255, 255))
        imageDraw.text((dados[0], dados[2]), dados[5], anchor='mm',
               font=fonte(35, tipo = 'italic'), fill=(255, 255, 255))
        imageDraw.text((dados[0], dados[3]), dados[6], anchor='mm',
               font=fonte(35, tipo = 'italic'), fill=(255, 255, 255))
    elif len(dados) == 9:
        imageDraw.text((390, 817), dicioList[composer], anchor='mm',
               font=fonte(31), fill=(255, 255, 255))
        imageDraw.text((dados[0], dados[1]), dados[5], anchor='mm',
               font=fonte(30, tipo = 'italic'), fill=(255, 255, 255))
        imageDraw.text((dados[0], dados[2]), dados[6], anchor='mm',
               font=fonte(30, tipo = 'italic'), fill=(255, 255, 255))
        imageDraw.text((dados[0], dados[3]), dados[7], anchor='mm',
               font=fonte(30, tipo = 'italic'), fill=(255, 255, 255))
        imageDraw.text((dados[0], dados[4]), dados[8], anchor='mm',
               font=fonte(30, tipo = 'italic'), fill=(255, 255, 255))
    
    # def original_source 1007
    imageDraw.text((390, 1011), dicioList[original_source], anchor='mm',
               font=fonte(40), fill=(255, 255, 255))

    # def platform 1023
    imageDraw.text((1044, 1025), dicioList[platform], anchor='mm',
               font=fonte(35), fill=(255, 255, 255))

    # def premiere 994
    imageDraw.text((1723, 995), dicioList[premiere], anchor='mm',
               font=fonte(70), fill=(255, 255, 255))


    # Mostra a imagem
    #image.show()

    # Salva a imagem
    image.save(name_image + '.png')

"""
    Montando imagem:
    Imagem > Texto > Quebras de Texto > Coordenadas de Texto > Escrever na Imagem
"""
        
print('Ha')
