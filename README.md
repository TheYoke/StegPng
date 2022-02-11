# StegPng
Conceal your secret message in an ordinary PNG image

### Requirements
- Python 3.6+
- numpy
- Pillow

### Description
`encoder.py` encodes your file's data into the least significant bit of each random pixel in an random order.
`decoder.py` reverses the encoder's process and outputs the encoded file.

