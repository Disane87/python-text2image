from PIL import Image, ImageDraw, ImageFont
import os

# settings
source_image = "images/abstract-business-code-270348.jpg"
txt = "Microsoft SQL-Server mit Powershell neustarten"
txt_color = "white"
fontsize = 1
fontfile = "font/LuckiestGuy.ttf"
border = True
border_color = "black" 
border_size = 5
output_dir = "output"

# generating images
image = Image.open(source_image).convert('RGBA')
image_with_text = Image.new('RGBA', image.size, (255,255,255,0))
draw = ImageDraw.Draw(image_with_text)

# portion of image width you want text width to be
img_fraction = 0.95

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

    font_pos_x = (image_width - font.getsize(txt)[0]) / 2
    font_pos_y = (image_height - font.getsize(txt)[1]) / 2 

    if(fontsize > 50):
        print("==================================================")
        print("Current font size: ",fontsize)
        print("Calculated height middle: "+str(font_pos_x))
        print("Calculated width middle: "+str(font_pos_y))

print("==================================================")

# optionally de-increment to be sure it is less than criteria
fontsize -= 1
font = ImageFont.truetype(fontfile, fontsize)

print("Final font size: ",fontsize)

# applying border if needed
if(border):
    print("Applying border ",fontsize)
    draw.text((font_pos_x-border_size, font_pos_y-border_size), txt, font=font, fill=border_color)
    draw.text((font_pos_x+border_size, font_pos_y-border_size), txt, font=font, fill=border_color)
    draw.text((font_pos_x-border_size, font_pos_y+border_size), txt, font=font, fill=border_color)
    draw.text((font_pos_x+border_size, font_pos_y+border_size), txt, font=font, fill=border_color)

# draw text to image
draw.text((font_pos_x, font_pos_y), txt, font=font, fill=txt_color) # put the text on the image

# overlay text layer with the picture
out = Image.alpha_composite(image, image_with_text)

# show image
out.show()

# save image
out.save(os.path.join(output_dir, txt.replace(" ", "_")+'.png')) # save it