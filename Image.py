from PIL import Image, ImageDraw, ImageFont
# get an image
base = Image.open('images/abstract-business-code-270348.jpg').convert('RGBA')
text = "TESThdaskdhahsdhd"

# make a blank image for the text, initialized to transparent text color
txt = Image.new('RGBA', base.size, (255,255,255,0))

image_width = base.size[0] / 2.0
image_height = base.size[1] / 2.0

# get a font
fnt = ImageFont.truetype('font/LuckiestGuy.ttf', 40)
# get a drawing context
d = ImageDraw.Draw(txt)

text_size = d.textsize(text, font=fnt)


print("Image height: "+str(image_height))
print("Image width: "+str(image_width))
image_width = image_width - text_size[0] 
image_height = image_height - text_size[1] 

print("Text-Size: "+str(text_size))

print("Calculated height middle: "+str(image_height))
print("Calculated width middle: "+str(image_width))

# draw text, half opacity
d.text((image_width,image_height), text, font=fnt, fill=(255,255,255,255))

out = Image.alpha_composite(base, txt)

# out.show()

#git push --set-upstream disane87@gitlab.com:Disane87/python-text2image.git master