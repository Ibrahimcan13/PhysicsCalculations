import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 1. SAHNE VE EKSEN HAZIRLIĞI
fig, ax = plt.subplots(figsize=(10, 6))

# Sinüs dalgasının x eksenindeki noktaları (0 ile 2*pi arası)
x = np.linspace(0, 2 * np.pi, 10000)

# Kamerayı sabitlemek için eksen sınırlarını kilitliyoruz
ax.set_xlim(0, 2 * np.pi)
ax.set_ylim(-1.5, 1.5)

# Piste içi boş, neon tarzı turkuaz (cyan) bir çizgi bırakıyoruz
# Buradaki virgül (line,) nesneyi liste içinden nizamîce çıkarmak içindir
line, = ax.plot([], [], lw=2.5, color='cyan')

# Estetik arka plan ayarı (OLED ekranda jilet gibi dursun diye koyu tema)
fig.patch.set_facecolor('#121212')
ax.set_facecolor('#1e1e1e')
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')
ax.tick_params(colors='white')
ax.grid(True, linestyle='--', alpha=0.2)
ax.set_title('Akan Sinüs Dalgası (120 FPS Antrenman Turu)', color='white', fontsize=14)


# 2. PİSTON: HER KAREDE ÇALIŞACAK UPDATE FONKSİYONU
def update(frame):
    y = np.sin(x - frame / 12.0)
    line.set_data(x, y)
    return line,


ani = FuncAnimation(fig, update, frames=200, interval=6, blit=True)

plt.show()