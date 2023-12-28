import PySimpleGUI as sg
from PIL import Image, ImageFilter, ImageOps
from io import BytesIO

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
original = Image.open("test.png")

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

window.close()
