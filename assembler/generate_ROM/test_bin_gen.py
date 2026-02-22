data = bytes(range(256))

with open("test.bin", "wb") as f:
    f.write(data)