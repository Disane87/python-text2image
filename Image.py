# Needs min Python 3
# 

from PIL import Image, ImageDraw, ImageFont
import os
import re
import requests
import json
import base64
import webbrowser
from settings import Settings

def main():    
    # settings
    source_image = "images/pexels-photo-442573.jpeg"
    txt = "Text automatisiert in Bilder"+os.linesep+"einfügen mit Python"
    settings = Settings("config.json")

    #images = getPexelsPhotos("code", settings.pexels_api_key)
    # for image in images['photos']:
    #     webbrowser.open(image["url"])

    # internal settings, no need to change them!
    fontsize = 1

    # generating images
    image = Image.open(source_image).convert('RGBA')
    image_with_text = Image.new('RGBA', image.size, (255,255,255,0))
    draw = ImageDraw.Draw(image_with_text)

    # initial position of the text
    font_pos_x = 0
    font_pos_y = 0

    # getting font
    font = ImageFont.truetype(settings.fontfile, fontsize)

    # caluclate position of text (centered)
    image_width = image.size[0]
    image_height = image.size[1]

    # line height and width initial value
    line_height = 0
    line_width = 0

    print("Image height: "+str(image_height))
    print("Image width: "+str(image_width))

    # getting the perfect size of the fraction of teh text to fit in the image
    while (font.getsize(txt)[0] < settings.img_fraction*image.size[0]):
        fontsize += 1
        font = ImageFont.truetype(settings.fontfile, fontsize)

    # check if there is a new line terminator
    if txt.find(os.linesep) >= 0:
        print("New line found. Checking longest line width")
        lines = txt.split(os.linesep)
        for line in lines:

            # find the longest line
            if(font.getsize(line)[0] > line_width):
                line_width = font.getsize(line)[0]

            line_height += font.getsize(line)[1]
    else:    
        line_width = font.getsize(txt)[0]
        line_height = font.getsize(txt)[1]


    # calculating text position
    font_pos_x = (image_width - line_width) / 2
    font_pos_y = (image_height - line_height) / 2 

    # optionally de-increment to be sure it is less than criteria
    fontsize -= 1
    font = ImageFont.truetype(settings.fontfile, fontsize)

    print("Final font size: ",fontsize)

    # applying border if needed
    if(settings.border):
        print("Applying border ",fontsize)
        draw.text((font_pos_x-settings.border_size, font_pos_y-settings.border_size), txt, font=font, fill=settings.border_color, align=settings.text_alignment)
        draw.text((font_pos_x+settings.border_size, font_pos_y-settings.border_size), txt, font=font, fill=settings.border_color, align=settings.text_alignment)
        draw.text((font_pos_x-settings.border_size, font_pos_y+settings.border_size), txt, font=font, fill=settings.border_color, align=settings.text_alignment)
        draw.text((font_pos_x+settings.border_size, font_pos_y+settings.border_size), txt, font=font, fill=settings.border_color, align=settings.text_alignment)

    # draw text to image
    draw.text((font_pos_x, font_pos_y), txt, font=font, fill=settings.txt_color, align=settings.text_alignment) # put the text on the image

    # overlay text layer with the picture
    out = Image.alpha_composite(image, image_with_text)

    # show image
    out.show()

    # save image if not in previewmode
    if settings.preview_mode:
        file_name = re.sub(r"[^a-zA-Z0-9 | ]*","", txt).replace(" ", "_")+'.png'
        out.save(os.path.join(settings.output_dir, file_name)) # save it

        if settings.wp_auto_upload:
            token = base64.standard_b64encode((settings.wp_user + ':' + settings.wp_auth_key).encode('utf-8')) # we have to encode the usr and pw
            headers = {'Authorization': 'Basic ' + token.decode('utf-8')}
            media = {'file': open(os.path.join(settings.output_dir, file_name),'rb')} # 'picture.jpg' path to the image
            data = {'description': txt, 'title': txt}

            image = requests.post(settings.wp_url + '/media', headers=headers, files=media, data=data)
            link = json.loads(image.content.decode('utf-8'))['link']
            postid =json.loads(image.content.decode('utf-8'))['id']

            print('Your image is published on {} with ID {}'.format(link, postid))

            if settings.debug:
                resp = requests.delete(settings.wp_url + '/media/'+str(postid))
                print('DEBUG: Media with ID {} deleted.'.format(postid))

def getPexelsPhotos(searchString, apiKey, itemsPerPage=30, page=1):
    url = "https://api.pexels.com/v1/search"
    querystring = {"query":searchString,"per_page":itemsPerPage,"pages":page}

    headers = {
        'Authorization': "Bearer {}".format(apiKey),
        'Cache-Control': "no-cache",
        'User-Agent': 'My User Agent 1.0',
        'Postman-Token': "6b0ce672-7ad7-495a-9084-96b3c3a0ced5"
    }

    res = requests.request("GET", url, headers=headers, params=querystring,)

    if(res.ok):
        return json.loads(res.content.decode('utf-8'))
    else:
        return False
main()

