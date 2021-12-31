from PIL import Image, ImageColor

IMAGE_WIDTH = 1920
IMAGE_HEIGHT = 1080

def initialize():
    im = Image.new('RGB', (IMAGE_WIDTH,IMAGE_HEIGHT), color='white') 
    return im

def raytrace(im):
    # main code goes here
    im.putpixel((IMAGE_WIDTH//2,IMAGE_HEIGHT//2), ImageColor.getcolor('purple','RGB')) 
    return im

def save(im, img_name='test_image.png'):
    im.save(img_name)

def main():
    im = initialize()
    im = raytrace(im)
    save(im)

if __name__ == "__main__":
    main()