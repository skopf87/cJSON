"""Python-json oracle plus differential malformed/bounded input compatibility with upstream."""
import ctypes as c
import json
from pathlib import Path
import random
import sys

def load(path):
    lib=c.CDLL(str(path))
    lib.cJSON_ParseWithLengthOpts.argtypes=[c.c_void_p,c.c_size_t,c.POINTER(c.c_void_p),c.c_int]
    lib.cJSON_ParseWithLengthOpts.restype=c.c_void_p
    lib.cJSON_PrintUnformatted.argtypes=[c.c_void_p];lib.cJSON_PrintUnformatted.restype=c.c_void_p
    lib.cJSON_Delete.argtypes=[c.c_void_p];lib.cJSON_free.argtypes=[c.c_void_p]
    return lib

def parse(lib,data,n=None,require=0):
    buf=c.create_string_buffer(data)
    end=c.c_void_p()
    tree=lib.cJSON_ParseWithLengthOpts(buf,len(data)+1 if n is None else n,c.byref(end),require)
    offset=end.value-c.addressof(buf) if end.value else None
    if not tree:return False,offset,None
    s=lib.cJSON_PrintUnformatted(tree)
    assert s
    output=c.string_at(s)
    lib.cJSON_free(s);lib.cJSON_Delete(tree)
    return True,offset,output

lib=load(sys.argv[1]);upstream=load(sys.argv[2]);rng=random.Random(313373)
alphabet='abZ09 \\"\n\r\t/éΩ中😀'
count=0
for i in range(1800):
    value={''.join(rng.choices(alphabet,k=rng.randrange(0,40))):[''.join(rng.choices(alphabet,k=rng.randrange(0,300))),rng.randrange(-10**6,10**6),bool(i%2),None]}
    data=json.dumps(value,ensure_ascii=bool(i%2)).encode()
    a=parse(lib,data);b=parse(upstream,data)
    assert a==b,(i,a,b)
    assert a[0] and json.loads(a[2])==value,(i,a,value)
    count+=1
for p in sorted((Path(__file__).resolve().parents[1]/'fixtures/cjson').glob('*.json')):
    data=p.read_bytes();a=parse(lib,data)
    assert a==parse(upstream,data)
    assert a[0] and json.loads(a[2])==json.loads(data)
    count+=1
# Malformed bytes: preserve upstream acceptance, result and error offsets rather than imposing a new grammar.
for data in [b'',b'"',b'"\\',b'"abc',b'"\\uD800"',b'"\\uZZZZ"',b'"a\0b"',b'"\\q"',b'\xff',b'{"a":}',b'"a\nb"'] + [rng.randbytes(rng.randrange(0,64)) for _ in range(1000)]:
    for require in [0,1]:
        assert parse(lib,data,require=require)==parse(upstream,data,require=require),(data,require)
        count+=1
# Truncate at every exact input length, including before the closing quote.
for data in [b'"abc"',b'"\\nX\\u0041\\uD83D\\uDE00"',b'{"key":"value","arr":[1,true]}']:
    for n in range(len(data)+1):
        assert parse(lib,data,n)==parse(upstream,data,n),(data,n)
        count+=1
print(f'{count} independent JSON/differential/bounded cases passed')
