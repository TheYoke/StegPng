import numpy as np
from numpy.random import MT19937, RandomState, SeedSequence
from PIL import Image

import sys
import os
from os.path import splitext


def to_binary(b):
    a = np.frombuffer(b, 'uint8')
    return np.vstack([a >> 7-i & 1 for i in range(8)]).T.reshape(-1)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(f'{sys.argv[0]} IN_FILE IN_IMAGE [OUT_IMAGE]')
        print('IN_FILE: Path to a file you want to encode to the image.')
        print('IN_IMAGE: Path to an image you want to encode the file to.')
        print('OUT_IMAGE: Path you want to save the encoded image to. (default: suffix IN_IMAGE with "_encoded")')
        exit(1)

    IN_FILE = sys.argv[1]
    IN_IMAGE = sys.argv[2]

    if len(sys.argv) >= 4:
        OUT_IMAGE = sys.argv[3]
    else:
        name, ext = splitext(IN_IMAGE)
        OUT_IMAGE = name + "_encoded" + ext

    im = Image.open(IN_IMAGE)
    width, height, channel = im.width, im.height, len(im.getbands())
    n_bits = width * height * channel

    data_len = os.stat(IN_FILE).st_size * 8
    if data_len + 32 > n_bits:
        print("This image doesn't have enough pixels to encode the input data.")
        exit(1)

    with open(IN_FILE, 'rb') as f:
        data = to_binary(f.read())

    i = np.arange(n_bits)
    RandomState(MT19937(SeedSequence(n_bits))).shuffle(i)
    i = i[:data_len + 32]

    a = np.asarray(im).flatten()
    a[i[:32]] = a[i[:32]] ^ a[i[:32]] & 1 | to_binary(data_len.to_bytes(4, 'big'))
    a[i[32:]] = a[i[32:]] ^ a[i[32:]] & 1 | data

    Image.fromarray(a.reshape(height, width, channel)).save(OUT_IMAGE)
    print('The encoded image is saved to:', OUT_IMAGE)
