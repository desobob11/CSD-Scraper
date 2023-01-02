class Back_End():

    def bin_encode(source: str, dest: str) -> None:
        with open(source, "r") as file:
            contents = file.read()
            with open(dest, "wb") as bin:
                for i in contents:  
                    byte = (ord(i) + 100).to_bytes(1, byteorder="big", signed=False)
                    bin.write(byte)

    def bin_decode(source: str, dest: str) -> None:
        with open(source, "rb") as file:
            b = None
            arr = []
            while b != bytes(0):
                b = file.read(1)
                arr.append(b)
            arr.pop()

            with open(dest, "w") as txt:
                for i in arr:
                    char = chr(int.from_bytes(i, byteorder="big") - 100)
                    txt.write(char)