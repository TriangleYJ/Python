from PIL import Image
import cmath as math
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np

image_origin = Image.open('sf.png')

s0 = 2
res_ij_list = []

mu_up = 0
down = 0
sigma_2_up = 0

for i in range(image_origin.width - 1):
    for j in range(image_origin.height - 1):
        c0 = image_origin.getpixel((i, j))
        c1 = image_origin.getpixel((i + 1, j + 1))
        c2 = image_origin.getpixel((i, j + 1))
        c3 = image_origin.getpixel((i + 1, j + 1))
        rgb_ij = [0, 0, 0]
        for k in range(3):
            rgb_ij[k] = ((c0[k] - c1[k]) ** 2 + (c2[k] - c3[k]) ** 2)
        s_ij = (rgb_ij[0] + rgb_ij[1] + rgb_ij[2]) ** 0.5
        res_ij = s_ij / s0
        mu_up += res_ij ** 2
        down += res_ij
        res_ij_list.append(res_ij)

mu = mu_up / down
for i in res_ij_list:
    sigma_2_up += i * ((i - mu) ** 2)
sigma_2 = sigma_2_up / down
sigma = sigma_2 ** 0.5

print('mu : %s' % mu)
print("sigma_2 : %s" % sigma_2)

bin_size = sigma / 100
print('bin_size : %s' % bin_size)


def create_histogram(list):
    n = 1
    histo = []
    _histo = 0

    list.sort()

    last = len(list) - 1
    for i, x in enumerate(list):
        if x < 0:
            continue
        if x >= bin_size * n or i == last:
            histo.append(_histo)
            _histo = 0
            n += 1
        _histo += 1
    return histo


def normal(x, _mu, _sigma):
    return (1 / (_sigma * (2 * math.pi) ** 0.5)) * math.exp(-1 * (x - _mu) ** 2 / (2 * _sigma ** 2))


histo = create_histogram(res_ij_list)
pi = []
norm = []
qi = []

for i in histo:
    pi.append(i / len(res_ij_list))
for i in range(len(histo)):
    norm.append(normal(i * bin_size + bin_size / 2, mu, sigma).real)  # 이렇게 하는 것인지는 확신 못함..
for i in norm:
    qi.append(i / sum(norm))  # 여기도 역시 확률의 총합을 1로 맞추기 위해서 이렇게 했는데..

#print(sum(qi)) #probability sum ~ 1
#print(sum(pi)) #probability sum ~ 1


m_rrz = 0
for i in range(len(pi)):  # pi.length == qi.length
    m_rrz += (pi[i] * math.log10(pi[i] / qi[i])).real
m_rrz = 1000 * m_rrz

print(m_rrz)  # 아마 작을수록 피트니스가 높은 듯..?


#  테스트용
plt.figure()
plt.plot(pi)
plt.plot(qi)
plt.show()

