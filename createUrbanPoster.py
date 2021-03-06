import sys

import requests
from PIL import Image
from numpy.polynomial import Polynomial as P

from image_utils import ImageText

bgColor = (29, 36, 57, 255)
textColor = (255, 255, 255)
url = "http://api.urbandictionary.com/v0/define?term={}"


def main(args):
    # Search for the word using the urbandictionary api and get definition and example
    word_to_search = str(args[1])

    api_search = url.format(word_to_search)
    response = requests.get(api_search)
    data = response.json()

    try:
        which_definition = int(args[3])
    except:
        which_definition = 0

    how_many_definitions = len(data["list"])

    if which_definition > how_many_definitions:
        defs = data["list"][how_many_definitions-1]
    elif which_definition <= 0:
        defs = data["list"][0]
    else:
        defs = data["list"][which_definition-1]

    if not defs:
        print("\nWord not found")
        quit()

    word = defs["word"]
    definition = defs["definition"]
    example = defs["example"]

    print(word + "\n\n" + definition + "\n\n" + example)

    width = 2480
    height = 3508

    # test if a font file has been given else quit
    try:
        font = str(args[2])
    except FileNotFoundError:
        print("\nNeed a font to draw the text")
        quit()

    # If font size specified set it else use a predefined function to find a tolerable value
    try:
        size_of_font = int(args[4])
    except:
        x_data = [14, 781, 147, 192, 210, 136, 245, 93, 637, 265, 328, 341, 8319]
        y_data = [500, 140, 280, 240, 250, 275, 245, 375, 160, 240, 220, 221, 47]

        deg = 5
        p = P.fit(x_data, y_data, deg)
        size = len(definition) + len(example)
        size_of_font = int(p(size))

    # If the Urban logo has been copied use it else make a new 1x1 picture
    try:
        logo = Image.open("Urban-Dictionary-logo.png")
    except FileNotFoundError:
        logo = Image.new("RGBA", (1, 1), bgColor)

    # Create the poster
    img = ImageText((width, height), background=bgColor)
    img_temp = ImageText((width, height), background=bgColor)

    font_size = ImageText.get_font_size(img, text=word, font=font, max_width=1000, max_height=240)
    w, h = img_temp.write_text_box((width, 100), word, box_width=1000, font_filename=font, font_size=font_size,
                                   color=textColor,
                                   place='center')
    img.write_text_box(((width - w) / 2, 150 - h), word, box_width=1000, font_filename=font, font_size=font_size,
                       color=textColor,
                       place='center')
    height = 150 + h / 2

    w, h = img_temp.write_text_box((width, height / 2), definition, box_width=2200, font_filename=font,
                                   font_size=size_of_font,
                                   color=textColor
                                   , place='justify')
    img.write_text_box(((width - w) / 2, height + 100), definition, box_width=2200, font_filename=font,
                       font_size=size_of_font,
                       color=textColor
                       , place='justify')
    height = height + 100 + h

    w, h = img_temp.write_text_box((width, 3000), example, box_width=2200, font_filename=font, font_size=size_of_font,
                                   color=textColor,
                                   place='justify')
    img.write_text_box(((width - w) / 2, height + 100), example, box_width=2200, font_filename=font,
                       font_size=size_of_font,
                       color=textColor,
                       place='justify')

    new_img = img.get_image()
    new_img.paste(logo, (-100, -10))

    new_img.save('Poster.png')

    print("\nCreated Poster and saved as Poster.png")

    print("\n\nFont size:", font_size)

    print("\nNumber of definitions:", how_many_definitions)


if __name__ == '__main__':
    main(sys.argv)
