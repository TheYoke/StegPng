# StegPng
Conceal your secret message in an ordinary PNG image

### Requirements
- Python 3.6+
- numpy
- Pillow

### Description
`encoder.py` encodes your file's binary data into the least significant bit of some random channels in some random pixels in a random order.  
`decoder.py` reverses the encoder's process and outputs the encoded file.

---

![an ordinary summation](sum_a2b.png)  
