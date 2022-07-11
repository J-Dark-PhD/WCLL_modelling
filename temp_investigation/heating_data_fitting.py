import numpy as np
from scipy.stats import linregress
import matplotlib.pyplot as plt

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

data_luigi = np.genfromtxt("luigi_neutronics_data.csv", delimiter=",", names=True)
data_moro = np.genfromtxt("moro_neutronics_data.csv", delimiter=",", names=True)

x_luigi = data_luigi["x"]
q_luigi = data_luigi["Q"]
x_moro = data_moro["x"]
q_moro = data_moro["Q"]

# plt.figure()
# plt.plot(x_luigi, q_luigi, label="Luigi")
# plt.plot(x_moro, q_moro, label="Moro")
# plt.xlabel(r"Distance from the FW (cm)")
# plt.ylabel(r"Nuclear heating (W/cm$^{3}$)")
# plt.xlim(0, 60)
# plt.legend()

# # log version
# plt.figure()
# plt.plot(x_luigi, q_luigi, label="Luigi")
# plt.plot(x_moro, q_moro, label="Moro")
# plt.xlabel(r"Distance from the FW (cm)")
# plt.ylabel(r"Nuclear heating (W/cm$^{3}$)")
# plt.yscale("log")
# plt.xlim(0, 60)
# plt.legend()

luigi_front = [
    (4.7295, 13.7560),
    (5.3157, 11.6218),
    (5.7434, 10.5560),
    (6.2156, 9.2492),
    (6.7413, 8.1024),
    (7.3116, 7.3594),
    (7.8819, 6.6844),
    (8.3777, 6.0043),
    (9.1650, 5.6488),
    (9.7341, 5.1941),
    (10.8758, 4.6602),
    (12.0567, 4.1807),
    (13.5671, 3.7192),
    (15.0947, 3.2329),
]

luigi_rear = [
    (16.6114, 3.1143),
    (18.0862, 2.7846),
    (19.6092, 2.4632),
    (21.0770, 2.3222),
    (22.6850, 2.1205),
    (24.2179, 1.9343),
    (25.7508, 1.7683),
    (27.2837, 1.6027),
    (28.8166, 1.4793),
    (30.3496, 1.3625),
    (31.8825, 1.2482),
    (33.3999, 1.1476),
    (34.9054, 1.0392),
    (36.4812, 0.9741),
    (38.0722, 0.8776),
    (39.5149, 0.8281),
    (40.6793, 0.7253),
    (41.3935, 0.7399),
    (42.7025, 0.6806),
    (44.1458, 0.6429),
    (45.4643, 0.5753),
    (47.0723, 0.5559),
    (48.6052, 0.5136),
    (50.2078, 0.4670),
    (51.6710, 0.4428),
    (53.2039, 0.4110),
    (54.7020, 0.3925),
    (55.7721, 0.3635),
    (57.0188, 0.3692),
    (58.6986, 0.3920),
    (60.1963, 0.3619),
    (62.0263, 0.3025),
    (63.6557, 0.2827),
    (65.1653, 0.2649),
    (66.7215, 0.2497),
    (68.2544, 0.2262),
    (69.7873, 0.2155),
    (71.3202, 0.2047),
    (72.9726, 0.2071),
    (74.2641, 0.2338),
    (75.4312, 0.3276),
]

luigi_eurofer = [
    (4.564208533, 6.17709058),
    (5.085262626, 5.007300971),
    (6.252729951, 3.973129041),
    (7.486071082, 3.194142415),
    (8.806740608, 2.775553448),
    (9.38018488, 2.360187476),
    (10.75829199, 2.167140804),
    (12.08103879, 1.823327641),
    (13.49562609, 1.656981559),
    (14.96837704, 1.358033763),
    (16.34386569, 1.216581971),
    (17.89194244, 1.077562003),
    (19.22921565, 0.933577695),
    (20.55807675, 0.845496965),
    (22.08680045, 0.736230527),
    (23.72723142, 0.639190514),
    (25.08260952, 0.566528808),
    (26.56819888, 0.503463356),
    (28.10761166, 0.435119894),
    (29.47024341, 0.398547038),
    (30.47329085, 0.354701433),
    (31.75481479, 0.323259372),
    (33.22850275, 0.285188525),
    (34.8016656, 0.256030263),
    (36.21798945, 0.227163962),
    (37.67774417, 0.199882449),
    (39.14255452, 0.176626381),
    (40.65301307, 0.157402878),
    (42.18607766, 0.142329729),
    (43.73174113, 0.125438115),
    (45.18852249, 0.106779491),
    (46.56464838, 0.099279552),
    (48.25735501, 0.086764247),
    (49.75257913, 0.078816773),
    (51.242207, 0.070802226),
    (52.89233908, 0.064395468),
    (54.34955879, 0.05945036),
    (55.88136758, 0.056904383),
    (57.41251606, 0.058070379),
    (59.01872854, 0.058674351),
    (60.43296276, 0.051509032),
    (61.56650646, 0.043948861),
    (62.88848638, 0.040258608),
    (64.64772943, 0.036561976),
    (66.03740113, 0.03507256),
    (67.54635327, 0.032463327),
    (69.11315548, 0.030506099),
    (70.64455709, 0.03037611),
    (72.26833171, 0.031555004),
    (73.61248839, 0.036788079),
    (74.23925405, 0.04927862),
]

x_range_1 = np.linspace(2.8, 15)
x_range_2 = np.linspace(15, 60)

# ##### luigi
data_luigi_front = np.array(luigi_front)
res_lf = linregress(np.log10(data_luigi_front[:, 0]), np.log10(data_luigi_front[:, 1]))
q_luigi_front = 10 ** (res_lf.intercept) * x_range_1**res_lf.slope
data_luigi_rear = np.array(luigi_rear)
lipb_bulk_x_values = data_luigi_rear[:, 0]
lipb_bulk_logy_values = np.log(data_luigi_rear[:, 1])
res_lb = linregress(lipb_bulk_x_values, lipb_bulk_logy_values)
q_luigi_rear = np.exp(res_lb.intercept) * np.exp(x_range_2 * res_lb.slope)

plt.figure()
# plt.plot(
#     x_range_1,
#     q_luigi_front,
#     color="tab:red",
#     label="Front : {:.1f} x ^ {:.2}".format(10**res_lf.intercept, res_lf.slope),
# )
# plt.plot(
#     x_range_2,
#     q_luigi_rear,
#     color="black",
#     label="Rear : {:.1f} exp ({:.2}*x)".format(np.exp(res_lb.intercept), res_lb.slope),
# )
plt.scatter(data_luigi_front[:, 0], data_luigi_front[:, 1], color="green")
plt.scatter(data_luigi_rear[:, 0], data_luigi_rear[:, 1], color="green", label="LiPb")
data_luigi_eurofer = np.array(luigi_eurofer)
plt.scatter(
    data_luigi_eurofer[:, 0], data_luigi_eurofer[:, 1], color="blue", label="Eurofer"
)
r = np.linspace(2.8, 60, num=50)
luigi_q = 25.53 * np.exp(-0.5089 * r) + 5.443 * np.exp(-0.0879 * r)
plt.plot(r, luigi_q, label="Eq. 12 (Candido 2021)", color="black")
plt.yscale("log")
plt.xlabel(r"Distance from the FW (cm)")
plt.xlim(0, 60)
plt.ylabel(r"Nuclear heating (W/cm$^{3}$)")
plt.legend()

# ##### Moro

moro_front = [
    (4.6902, 19.7908),
    (5.2450, 15.9999),
    (5.8117, 13.1176),
    (6.6282, 11.3025),
    (7.1679, 9.3324),
    (8.0115, 8.7780),
    (8.7588, 7.7631),
    (9.7022, 7.0363),
    (10.4802, 6.4098),
    (11.3929, 6.0080),
    (12.2015, 5.6689),
    (13.0836, 5.2947),
    (13.9229, 4.9409),
]
moro_rear = [
    (15.6442, 4.2875),
    (17.3656, 3.7097),
    (19.0869, 3.3981),
    (20.8083, 2.9878),
    (22.5296, 2.6814),
    (24.2510, 2.4276),
    (25.9723, 2.1786),
    (27.6937, 1.9724),
    (29.4150, 1.7857),
    (31.1363, 1.6892),
    (32.8577, 1.5248),
    (34.5790, 1.3725),
    (36.3004, 1.2299),
    (38.0217, 1.1135),
    (39.7431, 1.0022),
    (41.4644, 0.9047),
    (43.1858, 0.8483),
    (44.9071, 0.7794),
    (46.6285, 0.7025),
    (48.3498, 0.6369),
    (50.0712, 0.5725),
    (51.7925, 0.5415),
    (53.5139, 0.4924),
    (55.2352, 0.4439),
    (56.9566, 0.4001),
    (58.6779, 0.3774),
    (60.4149, 0.3603),
    (62.1206, 0.3299),
    (63.8419, 0.2821),
    (65.5633, 0.2532),
    (67.2846, 0.2200),
    (69.0060, 0.2057),
    (70.7273, 0.1849),
    (72.4487, 0.1759),
    (74.1700, 0.1798),
    (75.9892, 0.2077),
    (77.5525, 0.2619),
    (78.5516, 0.3545),
]
data_moro_front = np.array(moro_front)
res_lf = linregress(np.log10(data_moro_front[:, 0]), np.log10(data_moro_front[:, 1]))
q_moro_front = 10 ** (res_lf.intercept) * x_range_1**res_lf.slope
data_moro_rear = np.array(moro_rear)
lipb_bulk_x_values = data_moro_rear[:, 0]
lipb_bulk_logy_values = np.log(data_moro_rear[:, 1])
res_lb = linregress(lipb_bulk_x_values, lipb_bulk_logy_values)
q_moro_rear = np.exp(res_lb.intercept) * np.exp(x_range_2 * res_lb.slope)

# plt.figure()
# plt.plot(
#     x_range_1,
#     q_moro_front,
#     color="tab:red",
#     label="q_moro : {:.4e} x ^ {:.4}".format(10**res_lf.intercept, res_lf.slope),
# )
# plt.plot(
#     x_range_2,
#     q_moro_rear,
#     color="black",
#     label="moro rear : {:.4e} exp ({:.4}*x)".format(
#         np.exp(res_lb.intercept), res_lb.slope
#     ),
# )
# plt.scatter(data_moro_front[:, 0], data_moro_front[:, 1], color="tab:green")
# plt.scatter(data_moro_rear[:, 0], data_moro_rear[:, 1], color="tab:green")
# plt.yscale("log")
# plt.xlabel("x (cm)")
# plt.xlim(0, 60)
# plt.ylabel(r"Q (W/cm$^{3}$)")
# plt.legend()
plt.show()
