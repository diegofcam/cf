import qrcode
import os
import uuid
from pdfme import build_pdf

facturaInicio = 1000
facturaFinal = 1020

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=5,
    border=4,
)
images = []
# we create directory fo images
contents = []

for x in range (facturaInicio,facturaFinal):
    link = f'https://cf.lcrjardin.com/{str(uuid.uuid4())}'
    contents.append({'link':link,'factura':x})

directory = f'jobs/{str(uuid.uuid4())}'
os.mkdir(directory)
counter = 0

for content in contents:
    qr.add_data(content['link'])
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    qr.clear()
    imglocation = f'{directory}/some_file_{str(counter)}.png'
    img.save(imglocation)
    images.append({'location':imglocation,'factura':content['factura']})
    counter +=1

print('listo!')

document = {}
document['style'] = {
    'margin_bottom': 15,
    'text_align': 'j'
}
document['sections'] = []
section1 = {}
document['sections'].append(section1)
document['formats'] = {
    'url': {'c': 'blue', 'u': 1},
    'title': {'b': 1, 's': 10}
}
section1['content'] = content1 = []

table_def1 = {
    'widths': [1, 1, 1, 1, 1],
    'style': {'border_width': 0, 'margin_left': 0, 'margin_right': 0},
}

tabledata = []
countImagesPerRow = 0
tabledatarow  = []
tabledatarowTitles = []
tabledaterowFooters = []
imagesPerRow = 5

for image in images:

    factura = image['factura']
    tabledatarowTitles.append(f'Siga el qr para calificarnos')
    tabledatarow.append({'image': image['location']})
    tabledaterowFooters.append(f'Factura {factura}')


    if (countImagesPerRow == (imagesPerRow-1)):
        tabledata.append(tabledatarowTitles)
        tabledata.append(tabledatarow)
        tabledata.append(tabledaterowFooters)
        tabledatarow  = []
        tabledatarowTitles = []
        tabledaterowFooters = []
        countImagesPerRow = 0
    else:
        countImagesPerRow += 1

table_def1['table'] = tabledata
content1.append(table_def1)

with open(f'{directory}/document.pdf', 'wb') as f:
    build_pdf(document, f)

stop = 1


## vamos a usar pdfkit
