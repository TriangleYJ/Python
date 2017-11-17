from PIL import Image

image_origin = Image.open('spython.png')
alpha = 0.1

width_origin = image_origin.width
height_origin = image_origin.height

width_half_origin = width_origin / 2
height_half_origin = height_origin / 2


def create_image(srt_point, size, x_reverse, y_reverse):
    srt_x = 0 if srt_point[0] == 0 else width_half_origin
    srt_y = 0 if srt_point[1] == 0 else height_half_origin
    end_x = width_half_origin if size[0] == 1 else width_origin
    end_y = height_half_origin if size[1] == 1 else height_origin

    crop_image = image_origin.copy().crop((srt_x, srt_y, end_x, end_y)).convert('RGB')
    if x_reverse:
        crop_image = crop_image.transpose(Image.FLIP_LEFT_RIGHT)
    if y_reverse:
        crop_image = crop_image.transpose(Image.FLIP_TOP_BOTTOM)

    return crop_image

    # 1--------2--------O   Srt point
    # |        |        |   1 : [0, 0],  2 : [1, 0],  3 : [0, 1],  4 : [1, 1]
    # |        |        |   End point
    # 3--------4--------5   5 : [2, 1],  6 : [1, 2],  7 : [2, 2]
    # |        |        |
    # |        |        |
    # O--------6--------7


def calculate():
    a_left = create_image([0, 0], [1, 2], False, False)
    _a_right = create_image([1, 0], [2, 2], True, False)
    a_top = create_image([0, 0], [2, 1], False, False)
    _a_bottom = create_image([0, 1], [2, 2], False, True)
    a_1 = create_image([0, 0], [1, 1], False, False)
    _a_4 = create_image([1, 1], [2, 2], True, True)
    a_2 = create_image([1, 0], [2, 1], False, False)
    _a_3 = create_image([0, 1], [1, 2], True, True)

    sh = s(a_left, _a_right)
    sv = s(a_top, _a_bottom)
    sd = (s(a_1, _a_4) + s(a_2, _a_3)) / 2  # Average
    measure = (sh + sv + sd) / 3  # Average
    return measure


def s(image1, image2):
    width = image1.width
    height = image1.height
    result = 0

    for i in range(width):
        for j in range(height):
            r1, g1, b1 = image1.getpixel((i, j))
            r2, g2, b2 = image2.getpixel((i, j))
            result += sim(r1 + g1 + b1, r2 + g2 + b2)

    return result / (width * height)


def sim(pixel1, pixel2):
    ii = pixel1 / (255 * 3)  # pixel data's range is 0 to 1, but original data's range is 0 to 255.
    ij = pixel2 / (255 * 3)  # And it need to divide to 3 to get average data.
    return 1 if (abs(ii - ij) < alpha) else 0


print(calculate())
