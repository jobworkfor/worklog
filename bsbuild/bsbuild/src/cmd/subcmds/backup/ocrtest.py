import cv2
import pytesseract
from PIL import Image

imgPath = "D:\\20210818\\screencap_p-shensibo.png"

# if __name__ == '__main__':
#     text = pytesseract.image_to_string(Image.open("D:\\20210818\\screencap_p-shensibo.png"), config='--psm 6', lang="eng")
#     print(text)


# import cv2
#
# img_cv = cv2.imread(imgPath)
#
# # By default OpenCV stores images in BGR format and since pytesseract assumes RGB format,
# # we need to convert from BGR to RGB format/mode:
# img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
# print (type(img_rgb))
# print(pytesseract.image_to_string(img_rgb))
# # OR
# img_rgb = Image.frombytes('RGB', img_cv.shape[:2], img_cv, 'raw', 'BGR', 0, 0)
# print(pytesseract.image_to_string(img_rgb))


img = Image.open(imgPath).convert('L')
rect = (186, 1336, 888, 1450)
img = img.crop(rect)
pixels = img.load()

width = img.size[0]
height = img.size[1]
for x in range(width):
    for y in range(height):
        if (x > 90 and x < 125) \
                or (x > 210 and x < 245) \
                or (x > 337 and x < 380) \
                or (x > 460 and x < 500) \
                or (x > 580 and x < 620) \
                :
            pixels[x, y] = 255
            continue

        if pixels[x, y] == 255:
            pixels[x, y] = 0
        else:
            pixels[x, y] = 255

# img = img.resize((702 >> 2, 114 >> 2), Image.ANTIALIAS)

# for i in range(img.size[0]):
#     for j in range(img.size[1]):
#         x, y, z = pixels[i, j][0], pixels[i, j][1], pixels[i, j][2]
#         x, y, z = abs(x - 255), abs(y - 255), abs(z - 255)
#         pixels[i, j] = (x, y, z)

print(pytesseract.image_to_string(img, lang='eng', config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789'))
img.save('ocrdebug.png')
img.show()

# im = Image.open(imgPath).convert('L')
# im = PIL.ImageOps.invert(im)
#
# rect = (186, 1336, 273, 1484)
# rect = (186, 1336, 888, 1484)
# rect = (186, 1336, 515, 1484)
# num1 = im.crop(rect)
#
# num1.save('_0.png')
#
# print(pytesseract.image_to_string(num1, lang='eng', config='--psm 13 --oem 3 -c tessedit_char_whitelist=ABCDEF0123456789'))

# rect = (309, 1336, 395, 1484)
# num1 = im.crop(rect)
# print(pytesseract.image_to_string(num1, lang='eng', config='--psm 13 --oem 1 -c tessedit_char_whitelist=ABCDEF0123456789'))
