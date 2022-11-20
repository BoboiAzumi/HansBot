import base64

def Encode(Str):
    Str = Str.encode("ascii")
    Base64 = base64.b64encode(Str)
    Str = Base64.decode("ascii")
    return Str

def Decode(Str):
    Str = Str.encode("ascii")
    Base64 = base64.b64decode(Str)
    Str = Base64.decode("ascii")
    return Str
    