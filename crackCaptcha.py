from PIL import Image,ImageEnhance
from pytesseract import pytesseract
import requests
import io

'''
Page segmentation modes:
  0    Orientation and script detection (OSD) only.
  1    Automatic page segmentation with OSD.
  2    Automatic page segmentation, but no OSD, or OCR. (not implemented)
  3    Fully automatic page segmentation, but no OSD. (Default)
  4    Assume a single column of text of variable sizes.
  5    Assume a single uniform block of vertically aligned text.
  6    Assume a single uniform block of text.
  7    Treat the image as a single text line.
  8    Treat the image as a single word.
  9    Treat the image as a single word in a circle.
 10    Treat the image as a single character.
 11    Sparse text. Find as much text as possible in no particular order.
 12    Sparse text with OSD.
 13    Raw line. Treat the image as a single text line,
       bypassing hacks that are Tesseract-specific.
'''
def extractCaptcha(var):
    # Defining paths to tesseract.exe
    path_to_tesseract = r"/usr/bin/tesseract"
    # image_path = r"/home/shipway/Downloads/captcha.png"
    image_path = f"D:\Web_Designing\P2_tracker\images\{var}"
    # response = requests.get(image_path)

    # Opening the image & storing it in an image object
    img = Image.open(image_path)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(3)
    # img = Image.open(io.BytesIO(response.content))

    # Providing the tesseract executable
    # location to pytesseract library
    pytesseract.tesseract_cmd = path_to_tesseract

    # Passing the image object to image_to_string() function
    # This function will extract the text from the image
    text = pytesseract.image_to_string(img)
    #print(text[:-1])
    # captcha = (text.split(" "))[1]
    text = text.split(" ")
    if(len(text)==1):
        captcha = text[0].split("\n")[1]
        # print(captcha)
    # captcha = ''
    else:
        captcha = ''.join(text[1:])

    captcha = captcha.split("\n")[0]
    # captcha.upper()
    #print(text)
    print("captcha : ",captcha)

    return captcha

# ans = extractCaptcha("image502.png")
# print(ans)

'''
485
490
502 - empty captcha - problem solved
429 - just one string
689 - difference in 5 and S
'''
