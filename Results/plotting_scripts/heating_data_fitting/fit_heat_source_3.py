import numpy as np
from scipy.stats import linregress
import matplotlib.pyplot as plt


data_lipb_front = [
    # x (cm)    , Q (W/cm3)
    (0.045652174, 18587918.91),
    (0.056521739, 13043213.87),
    (0.067391304, 10000000),
    (0.076086957, 8013941.242),
    (0.084782609, 7017038.287),
    (0.095652174, 6422325.422),
    (0.106521739, 5623413.252),
    (0.117391304, 5379838.403),
    (0.126086957, 5146813.857),
    (0.132608696, 4923882.632),
    (0.145652174, 4124626.383),
]


data_lipb_bulk = [
    # x (cm)    , Q (W/cm3)
    (0.156521739, 3945970.609),
    (0.165217391, 3611538.989),
    (0.176086957, 3305451.348),
    (0.184782609, 3305451.348),
    (0.197826087, 2894266.125),
    (0.204347826, 2768902.684),
    (0.217391304, 2534230.736),
    (0.226086957, 2424462.017),
    (0.234782609, 2319447.866),
    (0.245652174, 2218982.341),
    (0.254347826, 2030917.621),
    (0.267391304, 1942949.615),
    (0.276086957, 1778279.41),
    (0.284782609, 1701254.28),
    (0.295652174, 1627565.448),
    (0.306521739, 1627565.448),
    (0.317391304, 1489624.9),
    (0.326086957, 1425102.67),
    (0.334782609, 1363375.184),
    (0.345652174, 1247825.47),
    (0.356521739, 1142068.906),
    (0.365217391, 1092600.861),
    (0.376086957, 1045275.495),
    (0.382608696, 1000000),
    (0.397826087, 915247.3109),
    (0.404347826, 875603.9101),
    (0.413043478, 837677.6401),
    (0.423913043, 801394.1242),
    (0.434782609, 801394.1242),
    (0.447826087, 733473.8171),
    (0.454347826, 701703.8287),
    (0.463043478, 671309.9387),
    (0.476086957, 614414.6161),
    (0.484782609, 562341.3252),
    (0.495652174, 537983.8403),
    (0.504347826, 514681.3857),
    (0.515217391, 514681.3857),
    (0.526086957, 492388.2632),
    (0.534782609, 450657.0338),
    (0.547826087, 431137.0885),
    (0.556521739, 412462.6383),
    (0.563043478, 377505.3205),
    (0.576086957, 361153.8989),
    (0.584782609, 377505.3205),
    (0.597826087, 345510.7295),
]


data_eurofer_front = [
    (0.004347826, 8376776.401),
    (0.015217391, 8013941.242),
    (0.023913043, 7334738.171),
    (0.034782609, 7017038.287),
    (0.045652174, 6144146.161),
    (0.054347826, 5379838.403),
    (0.067391304, 4124626.383),
    (0.076086957, 3775053.205),
    (0.084782609, 3305451.348),
    (0.095652174, 2768902.684),
    (0.106521739, 2424462.017),
    (0.117391304, 2319447.866),
    (0.123913043, 2122868.422),
    (0.134782609, 1942949.615),
    (0.145652174, 1778279.41),
    (0.154347826, 1489624.9),
    (0.167391304, 1363375.184),
]


data_eurofer_bulk = [
    (0.167391304, 1363375.184),
    (0.176086957, 1247825.47),
    (0.184782609, 1193776.642),
    (0.195652174, 1092600.861),
    (0.204347826, 1000000),
    (0.217391304, 875603.9101),
    (0.226086957, 837677.6401),
    (0.234782609, 801394.1242),
    (0.245652174, 701703.8287),
    (0.254347826, 671309.9387),
    (0.267391304, 587801.6072),
    (0.276086957, 537983.8403),
    (0.284782609, 514681.3857),
    (0.295652174, 450657.0338),
    (0.306521739, 431137.0885),
    (0.315217391, 377505.3205),
    (0.326086957, 361153.8989),
    (0.334782609, 330545.1348),
    (0.345652174, 302530.5457),
    (0.354347826, 289426.6125),
    (0.365217391, 264896.9288),
    (0.376086957, 242446.2017),
    (0.384782609, 221898.2341),
    (0.395652174, 212286.8422),
    (0.404347826, 194294.9615),
    (0.415217391, 177827.941),
    (0.426086957, 162756.5448),
    (0.434782609, 155706.8405),
    (0.445652174, 148962.49),
    (0.452173913, 136337.5184),
    (0.463043478, 124782.547),
    (0.476086957, 114206.8906),
    (0.484782609, 109260.0861),
    (0.495652174, 104527.5495),
    (0.506521739, 91524.73109),
    (0.513043478, 87560.39101),
    (0.523913043, 80139.41242),
    (0.534782609, 76668.22075),
    (0.545652174, 73347.38171),
    (0.554347826, 67130.99387),
    (0.565217391, 64223.25422),
    (0.576086957, 56234.13252),
]

# data_1 = np.array(data_eurofer_total)

# res = linregress(data[:, 0], np.log(data[:, 1]))

x = np.linspace(0.00, 0.60)
y = np.linspace(0.04, 0.15)
y2 = np.linspace(0.00, 0.15)
z = np.linspace(0.15, 0.60)

# plt.plot(x, np.exp(res.intercept)*np.exp(x*res.slope), label="{:.5f} exp({:.5f} x)".format(np.exp(res.intercept), res.slope))
# q_candido = 25.53*np.exp(-0.5089*x) + 5.443*np.exp(-0.0879*x)
# plt.plot(x, q_candido, label="Candido LiPb")

# q_james_1_lipb = 114.07*y**(-1.261)
# q_james_2_lipb = 8.46291*np.exp(-0.05485*z)

# q_james_1_euro = 9.6209*np.exp(-0.12019*y)
# q_james_2_euro = 4.87010*np.exp(-0.07651*z)

# ##### LiPb
data_lipb_front = np.array(data_lipb_front)
res_lf = linregress(np.log10(data_lipb_front[:, 0]), np.log10(data_lipb_front[:, 1]))

# y = A * x ^ B  (1)
#
# (1) --> log(y) = log(A) + B * log(x)

# res.slope = B   --> B = res.slope
# res.intercept = log(A)  --> A = 10 ^ res.intercept

q_james_1_lipb = 10 ** (res_lf.intercept) * y**res_lf.slope
plt.plot(
    y,
    q_james_1_lipb,
    color="tab:red",
    label="James LiPb_front : {:.4e} x ^ {:.4}".format(
        10**res_lf.intercept, res_lf.slope
    ),
)


data_lipb_bulk = np.array(data_lipb_bulk)

lipb_bulk_x_values = data_lipb_bulk[:, 0]
lipb_bulk_logy_values = np.log(data_lipb_bulk[:, 1])

res_lb = linregress(lipb_bulk_x_values, lipb_bulk_logy_values)

# y = A * exp(x*B)  (1)
#
# (1) --> ln(y) = ln(A) + ln(exp(x*B)) = ln(A) + x*B
# res.slope = B   --> B = res.slope
# res.intercept = ln(A)  --> A = np.exp(res.intercept)

q_james_2_lipb = np.exp(res_lb.intercept) * np.exp(z * res_lb.slope)

plt.plot(
    z,
    q_james_2_lipb,
    color="black",
    label="James LiPb_bulk : {:.4e} exp ({:.4}*x)".format(
        np.exp(res_lb.intercept), res_lb.slope
    ),
)
plt.scatter(data_lipb_bulk[:, 0], data_lipb_bulk[:, 1], color="tab:green")
plt.scatter(data_lipb_front[:, 0], data_lipb_front[:, 1], color="tab:green")

# ##### Eurofer

data_eurofer_front = np.array(data_eurofer_front)
res_ef = linregress(data_eurofer_front[:, 0], np.log(data_eurofer_front[:, 1]))
q_james_1_euro = np.exp(res_ef.intercept) * np.exp(y2 * res_ef.slope)

data_eurofer_bulk = np.array(data_eurofer_bulk)
res_eb = linregress(data_eurofer_bulk[:, 0], np.log(data_eurofer_bulk[:, 1]))
q_james_2_euro = np.exp(res_eb.intercept) * np.exp(z * res_eb.slope)

plt.plot(
    y2,
    q_james_1_euro,
    color="tab:red",
    label="James Eurofer_front : {:.4e} exp ({:.4}*x)".format(
        np.exp(res_ef.intercept), res_ef.slope
    ),
)
plt.plot(
    z,
    q_james_2_euro,
    color="black",
    label="James Eurofer_bulk : {:.4e} exp ({:.4}*x)".format(
        np.exp(res_eb.intercept), res_eb.slope
    ),
)
plt.scatter(data_eurofer_bulk[:, 0], data_eurofer_bulk[:, 1], color="tab:grey")
plt.scatter(data_eurofer_front[:, 0], data_eurofer_front[:, 1], color="tab:grey")

print(res_lf.rvalue**2)
print(res_lb.rvalue**2)
print(res_ef.rvalue**2)
print(res_eb.rvalue**2)

plt.yscale("log")
plt.xlabel("x (m)")
plt.ylabel("Q (W/m3)")
plt.legend()
plt.show()
