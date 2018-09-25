from PIL import Image, ImageDraw, ImageFont
import os
import re

# settings
source_image = "images/pexels-photo-442573.jpeg"
txt = "Text automatisiert in Bilder"+os.linesep+"einfügen mit Python"
txt_color = "white"
fontsize = 1
fontfile = "font/LuckiestGuy.ttf"
border = True
border_color = "black" 
border_size = 5
output_dir = "output"
text_alignment = "center"
# portion of image width you want text width to be
img_fraction = 1

#
line_height = 0
line_width = 0

# generating images
image = Image.open(source_image).convert('RGBA')
image_with_text = Image.new('RGBA', image.size, (255,255,255,0))
draw = ImageDraw.Draw(image_with_text)

# initial position of the text
font_pos_x = 0
font_pos_y = 0

# getting font
font = ImageFont.truetype("arial.ttf", fontsize)

# caluclate position of text (centered)
image_width = image.size[0]
image_height = image.size[1]
print("Image height: "+str(image_height))
print("Image width: "+str(image_width))

# getting the perfect size of the fraction of teh text to fit in the image
while (font.getsize(txt)[0] < img_fraction*image.size[0]):
    fontsize += 1
    font = ImageFont.truetype(fontfile, fontsize)

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
font = ImageFont.truetype(fontfile, fontsize)

print("Final font size: ",fontsize)

# applying border if needed
if(border):
    print("Applying border ",fontsize)
    draw.text((font_pos_x-border_size, font_pos_y-border_size), txt, font=font, fill=border_color, align=text_alignment)
    draw.text((font_pos_x+border_size, font_pos_y-border_size), txt, font=font, fill=border_color, align=text_alignment)
    draw.text((font_pos_x-border_size, font_pos_y+border_size), txt, font=font, fill=border_color, align=text_alignment)
    draw.text((font_pos_x+border_size, font_pos_y+border_size), txt, font=font, fill=border_color, align=text_alignment)

# draw text to image
draw.text((font_pos_x, font_pos_y), txt, font=font, fill=txt_color, align=text_alignment) # put the text on the image

# overlay text layer with the picture
out = Image.alpha_composite(image, image_with_text)

# show image
out.show()

# save image
file_name = re.sub(r"[^a-zA-Z0-9 | ]*","", txt).replace(" ", "_")+'.png'
out.save(os.path.join(output_dir, file_name)) # save it