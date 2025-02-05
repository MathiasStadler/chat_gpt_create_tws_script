# FROM HERE
# https://stackoverflow.com/questions/73332915/how-do-i-add-a-crosshair-to-all-plots-for-plotsubplots-true/73333790


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import MultiCursor

df = pd.DataFrame(np.arange(1, 21).reshape(5,4))
axs = df.plot(subplots=True)

cursor = MultiCursor(axs[0].get_figure().canvas, axs, color='r', lw=1)

plt.show()