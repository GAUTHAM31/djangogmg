import hashlib, zlib
import cPickle as pickle
import urllib

my_secret = "michnorts"

def encode_data(data):
    """Turn `data` into a hash and an encoded string, suitable for use with `decode_data`."""
    text = zlib.compress(pickle.dumps(data, 0)).encode('base64').replace('\n', '')
    m = hashlib.md5(my_secret + text).hexdigest()[:12]
    return m, text

def decode_data(hash, enc):
    """The inverse of `encode_data`."""
    text = urllib.unquote(enc)
    m = hashlib.md5(my_secret + text).hexdigest()[:12]
    if m != hash:
        raise Exception("Bad hash!")
    data = pickle.loads(zlib.decompress(text.decode('base64')))
    return data


if __name__ == "__main__":
    hash0, enc = encode_data(['emp1','27','29',1])
    print hash0, enc
    d=decode_data(hash0, enc)
    print d[0],d[1],d[2],d[3]

