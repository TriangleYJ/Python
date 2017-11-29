# coding=utf-8
from __future__ import division
from math import log10
from PIL import Image
import matplotlib.pyplot as plt

image_origin = Image.open('white2.jpg')

expected = [log10(1 + 1 / d) for d in range(1, 10)]

list = []

intensity_cnt = [0 for _ in range(9)]

#RGB값을 명암값으로
def intensity(r, g, b):
    return 0.299 * r + 0.587 * g + 0.114 * b

#사진의 픽셀을 list배열에 받기
for i in range(image_origin.width):
    for j in range(image_origin.height):
        pixel = image_origin.getpixel((i, j))
        list.append(intensity(pixel[0], pixel[1], pixel[2]))

#각 픽셀에게 계급 지정
for i in list:
    if i <= 256 / 9:
        intensity_cnt[0] += 1

    elif i <= 256 * 2 / 9:
        intensity_cnt[1] += 1

    elif i <= 256 * 3 / 9:
        intensity_cnt[2] += 1

    elif i <= 256 * 4 / 9:
        intensity_cnt[3] += 1

    elif i <= 256 * 5 / 9:
        intensity_cnt[4] += 1

    elif i <= 256 * 6 / 9:
        intensity_cnt[5] += 1

    elif i <= 256 * 7 / 9:
        intensity_cnt[6] += 1

    elif i <= 256 * 8 / 9:
        intensity_cnt[7] += 1

    else:
        intensity_cnt[8] += 1

#intensity_cnt 배열 정렬
intensity_cnt.sort()
intensity_cnt.reverse()


#위에서 각각 도수별 들어가있는 픽셀 수를 전체 합이 1이 되게 조정
for i in range(len(intensity_cnt)):
    intensity_cnt[i] = intensity_cnt[i]/(image_origin.width*image_origin.height)

benford_law = [0.30103, 0.17609, 0.12494, 0.09691, 0.07918, 0.06695, 0.05799, 0.05115, 0.04576]

#사진의 명암값에서 벤포드 법칙과의 차와 최종 합
d_total = 0
for i in range(9):
    d_total += abs(intensity_cnt[i] - benford_law[i])

#measurment_bl 구하기
d_max=0
d_max_1 = [1, 0, 0, 0, 0, 0, 0, 0, 0]
for i in range(9):
    d_max += abs(d_max_1[i]-benford_law[i])

measurement_bl = (d_max-d_total)/d_max

print(measurement_bl)
