from PIL import Image, ImageOps, ImageDraw

mask = Image.open('mask.png').convert('L')
im = Image.open('batman.jpg')

size = (128, 128)
mask = Image.new('L', size, 0)
draw = ImageDraw.Draw(mask) 
draw.ellipse((0, 0) + size, fill=255)

im = Image.open('Batman.jpg')

output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
output.putalpha(mask)

output.save('output.png')