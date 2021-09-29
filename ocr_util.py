import configparser



def read(filepath,encoding = 'utf-8'):
    with open(filepath, 'r', encoding=encoding) as f:
        return f.read()\

def write(filepath,data):
    with open(filepath, 'w') as f:
        f.write(data)

def write_bytes(filepath,data):
    with open(filepath, "wb") as f:
        f.write(data)

