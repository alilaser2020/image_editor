import PySimpleGUI as sg
from PIL import Image, ImageFilter, ImageOps
from io import BytesIO


def update_image(original, blur, contrast, emboss, contour, flipx, flipy):
    """
    A method for updating given image
    :param original:
    :param blur:
    :param contrast:
    :param emboss:
    :param contour:
    :param flipx:
    :param flipy:
    :return:
    """
    image = original.filter(ImageFilter.GaussianBlur(blur))
    image = image.filter(ImageFilter.UnsharpMask(contrast))
    if emboss:
        image = image.filter(ImageFilter.EMBOSS())
    if contour:
        image = image.filter(ImageFilter.CONTOUR())
    if flipx:
        image = ImageOps.mirror(image)
    if flipy:
        image = ImageOps.flip(image)

    bio = BytesIO()
    image.save(bio, format="PNG")
    window["-IMAGE-"].update(data=bio.getvalue())


sg.theme("GrayGrayGray")

image_col = sg.Column([[sg.Image("test.png", key="-IMAGE-")]])

control_col = sg.Column([
    [sg.Frame("Blur", layout=[[sg.Slider(range=(0, 10), orientation="h", key="-BLUR-")]])],
    [sg.Frame("Contrast", layout=[[sg.Slider(range=(0, 10), orientation="h", key="-CONTRAST-")]])],
    [sg.Checkbox("Emboss", key="-EMBOSS-", expand_x=True),
     sg.Checkbox("Contour", key="-CONTOUR-", expand_x=True)],
    [sg.Checkbox("Flip x", key="-FLIPX-", expand_x=True),
     sg.Checkbox("Flip y", key="-FLIPY-", expand_x=True)],
    [sg.Button("Save", key="-SAVE-", expand_x=True)]
])

layout = [
    [control_col, image_col]
]

window = sg.Window("Image Editor", layout)
image_path = sg.popup_get_file("Open", no_window=True)
original = Image.open(image_path)

while True:
    event, values = window.read(timeout=50)
    if event == sg.WIN_CLOSED:
        break

    update_image(original,
                 values["-BLUR-"],
                 values["-CONTRAST-"],
                 values["-EMBOSS-"],
                 values["-CONTOUR-"],
                 values["-FLIPX-"],
                 values["-FLIPY-"]
                 )

window.close()
