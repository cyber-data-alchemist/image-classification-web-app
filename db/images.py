import os
import random
import numpy as np
import matplotlib.pyplot as plt

def create_trend_chart(filename, trend):
    x = np.arange(0, 100)

    if trend == 'up':
        y = np.cumsum(np.random.randn(100) + 0.5)
    elif trend == 'down':
        y = np.cumsum(np.random.randn(100) - 0.5)
    else:
        y = np.cumsum(np.random.randn(100))

    plt.figure(figsize=(10, 6))
    plt.plot(x, y)
    plt.xlabel('Time')
    plt.ylabel('Value')

    plt.savefig(filename)
    plt.close()

def main():
    image_folder = 'static/images/trainning'

    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    for i in range(100):
        trend = random.choice(['up', 'down'])
        filename = os.path.join(image_folder, f'image_{i}.jpg')
        create_trend_chart(filename)

if __name__ == '__main__':
    main()