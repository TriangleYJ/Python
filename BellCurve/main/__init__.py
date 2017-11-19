from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np

image_origin = Image.open('splw.png')


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
            rgb_ij[k] = (c0[k] - c1[k])**2 + (c2[k] - c3[k])**2
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


plt.figure()
plt.hist(res_ij_list, bins=300)
x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
plt.plot(x, mlab.normpdf(x, mu, sigma) * len(res_ij_list))
plt.show()





