import numpy as np
from numpy.random import MT19937, RandomState, SeedSequence
from PIL import Image

import sys


def from_binary(a):
    a = a.reshape(-1, 8).T
    return bytes(np.sum([a[i] << 7-i for i in range(8)], 0, 'uint8'))

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(f'{sys.argv[0]} IN_IMAGE OUT_FILE')
        print('IN_IMAGE: Path to an encoded image you want to decode.')
        print('OUT_FILE: Path you want to save the decoded file to.')
        exit(1)

    IN_IMAGE = sys.argv[1]
    OUT_FILE = sys.argv[2]

    im = Image.open(IN_IMAGE)
    width, height, channel = im.width, im.height, len(im.getbands())
    n_bits = width * height * channel

    if n_bits < 32:
        print("This image cannot be an encoded image, because its too small.")
        exit(1)

    i = np.arange(n_bits)
    RandomState(MT19937(SeedSequence(n_bits))).shuffle(i)

    a = np.asarray(im).flatten()
    data_len = int.from_bytes(from_binary(a[i[:32]] & 1), 'big')

    if data_len + 32 > n_bits:
        print("Encoded file size is too large,")
        print("It's likely that this image doesn't encoded with the corresponding encoder")
        print("nor have any encoded data.")
        exit(1)

    data = a[i[32:data_len + 32]] & 1
    with open(OUT_FILE, 'wb') as f:
        f.write(from_binary(data))

    print('The decoded file is saved to:', OUT_FILE)
