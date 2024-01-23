import instaloader,os
from PIL import Image, ImageOps, ImageDraw

def imgcrop(file):
    mask = Image.open('mask.png').convert('L')
    im = Image.open(file)

    size = (128, 128)
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask) 
    draw.ellipse((0, 0) + size, fill=255)

    im = Image.open(file)

    output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)

    output.save(file)
def instapic_downloader(username):
    insta = instaloader.Instaloader()
    dp = username
    insta.download_profile(dp,profile_pic_only=True)
    path=f"{dp}/"
    for filename in os.listdir(path):
        my_dest =dp+ ".png"
        my_source =path + filename
        my_dest =path + my_dest
                # rename() function will
                # rename all the files
        os.rename(my_source, my_dest)
        imgcrop(rf'{dp}\{dp}.png')

