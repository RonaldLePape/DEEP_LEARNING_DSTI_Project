import pandas as pd
import matplotlib.pyplot as plt
csv = r"C:\Users\ronal\Desktop\PROJETS PERSO\1-FORMATIONS\DSTI\DeepLearning\PROJECT\Yolo fine tuning\runs\classify\train\results.csv"

df = pd.read_csv(csv)
print(df.columns)  # see exact column names on your version

# Common columns include: 'epoch','train/loss','val/loss'
plt.figure()
plt.plot(df['epoch'], df['train/loss'], label='train loss')
plt.plot(df['epoch'], df['val/loss'],   label='val loss')
plt.xlabel("Epoch"); plt.ylabel("Loss"); plt.legend(); plt.title("YOLOv8-CLS Loss")
plt.show()