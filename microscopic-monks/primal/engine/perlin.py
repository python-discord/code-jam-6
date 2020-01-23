import numpy as np
from noise import pnoise2


def perlin_array(shape=(2500, 2500),
                 scale=100, octaves=1,
                 persistence=0.5,
                 lacunarity=2.0,
                 seed=None):
    if not seed:
        seed = np.random.randint(0, 100)
        print("seed was {}".format(seed))

    arr = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            arr[i][j] = pnoise2(i / scale,
                                j / scale,
                                octaves=octaves,
                                persistence=persistence,
                                lacunarity=lacunarity,
                                repeatx=1024,
                                repeaty=1024,
                                base=seed)
    max_arr = np.max(arr)
    min_arr = np.min(arr)

    return (arr - min_arr) / (max_arr - min_arr)
