import PySimpleGUI as sg
from PIL import Image, ImageFilter, ImageOps
from io import BytesIO


def reset_items():
    """
    A method for reset all items (blur, contrast, emboss, contour, flipx and flipy) after opening a new image
    :return:
    """
    window["-BLUR-"].update(0)
    window["-CONTRAST-"].update(0)
    window["-EMBOSS-"].update(False)
    window["-CONTOUR-"].update(False)
    window["-FLIPX-"].update(False)
    window["-FLIPY-"].update(False)


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
    global image
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
    [sg.Button("Save", key="-SAVE-", expand_x=True)],
    [sg.Button("Open", key="-OPEN-", expand_x=True)]
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

    if event == "-SAVE-":
        save_path = sg.popup_get_file("Save", no_window=True, save_as=True) + ".png"
        image.save(save_path, "PNG")

    if event == "-OPEN-":
        image_path = sg.popup_get_file("Open", no_window=True)
        original = Image.open(image_path)
        reset_items()

window.close()
