import numpy as np
import matplotx
import matplotlib.pyplot as plt


r = np.linspace(0, 0.5, num=50)

luigi_q = 25.53 * np.exp(-0.5089 * r * 1e2) + 5.443 * np.exp(-0.0879 * r * 1e2)

r_close = np.linspace(0, 0.15, num=50)
r_far = np.linspace(0.15, 0.5, num=50)
dark_q_close = 0.4 * r_close ** (-1.213)
dark_q_far = 8.5 * np.exp(-5.485 * r_far)

plt.plot(r, luigi_q, label="Candido")
plt.plot(r_close, dark_q_close, color="tab:orange")
plt.plot(r_far, dark_q_far, color="tab:orange", label="Dark")
plt.yscale("log")
matplotx.line_labels()
plt.tight_layout()
plt.show()
