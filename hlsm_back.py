import io

class Back_End():

    def bin_encode(source: io.FileIO) -> list[bytes]:
        bin = []
        for i in source:  
            byte = (ord(i) + 100).to_bytes(1, byteorder="big", signed=False)
            bin.append(byte)
        return bin

    def bin_decode(source: io.BytesIO) -> str:
        b = None
        arr = []
        while b != bytes(0):
            b = source.read(1)
            arr.append(b)
        arr.pop()

        decoded = ""
        for i in arr:
            char = chr(int.from_bytes(i, byteorder="big") - 100)
            decoded += char
        return decoded
