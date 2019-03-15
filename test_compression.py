#!/usr/bin/python3

import base64
import json
import time
import zlib

import cbor2

first_chunk = 1
last_chunk = 219

print("Chunk #, JSON Bytes, JSON+DEFLATE_SPEED Bytes, JSON+DEFLATE_SPEED ms, JSON+DEFLATE_DEFAULT Bytes, JSON+DEFLATE_DEFAULT ms, JSON+DEFLATE_MAX Bytes, JSON+DEFLATE_MAX ms, ascii85 Bytes, DEFLATE_SPEED+ascii85 Bytes, DEFLATE_DEFAULT+ascii85 Bytes, DEFLATE_MAX+ascii85 Bytes, ascii85+DEFLATE_SPEED Bytes, ascii85+DEFLATE_DEFAULT Bytes, ascii85+DEFLATE_MAX Bytes, CBOR Bytes, CBOR+DEFLATE_SPEED Bytes, CBOR+DEFLATE_SPEED ms, CBOR+DEFLATE_DEFAULT Bytes, CBOR+DEFLATE_DEFAULT ms, CBOR+DEFLATE_MAX Bytes, CBOR+DEFLATE_MAX ms")

for chunk in range(first_chunk, last_chunk+1):
    with open("json/chunk" + str(chunk) + ".json", 'rb') as fp:
        chunk_json = fp.read()

    time1_json_deflatespeed = time.time()

    chunk_json_deflatespeed = zlib.compress(chunk_json, zlib.Z_BEST_SPEED)[2:-4]
    chunk_json_deflatespeed_reversed = zlib.decompress(chunk_json_deflatespeed, -zlib.MAX_WBITS)

    time2_json_deflatespeed = time.time()

    if len(chunk_json) != len(chunk_json_deflatespeed_reversed):
        raise Exception("deflatespeed reverse failed on chunk" + str(chunk))

    time1_json_deflatedefault = time.time()

    chunk_json_deflatedefault = zlib.compress(chunk_json)[2:-4]
    chunk_json_deflatedefault_reversed = zlib.decompress(chunk_json_deflatedefault, -zlib.MAX_WBITS)

    time2_json_deflatedefault = time.time()

    if len(chunk_json) != len(chunk_json_deflatedefault_reversed):
        raise Exception("deflatedefault reverse failed on chunk" + str(chunk))

    time1_json_deflatemax = time.time()

    chunk_json_deflatemax = zlib.compress(chunk_json, zlib.Z_BEST_COMPRESSION)[2:-4]
    chunk_json_deflatemax_reversed = zlib.decompress(chunk_json_deflatemax, -zlib.MAX_WBITS)

    time2_json_deflatemax = time.time()

    if len(chunk_json) != len(chunk_json_deflatemax_reversed):
        raise Exception("deflatemax reverse failed on chunk" + str(chunk))

    chunk_obj = json.loads(chunk_json)
    headers_bytes = bytes.fromhex(chunk_obj["result"]["hex"])
    chunk_obj["result"]["hex"] = headers_bytes
    chunk_cbor = cbor2.dumps(chunk_obj)

    time1_cbor_deflatespeed = time.time()

    chunk_cbor_deflatespeed = zlib.compress(chunk_cbor, zlib.Z_BEST_SPEED)[2:-4]
    chunk_cbor_deflatespeed_reversed = zlib.decompress(chunk_cbor_deflatespeed, -zlib.MAX_WBITS)

    time2_cbor_deflatespeed = time.time()

    if len(chunk_cbor) != len(chunk_cbor_deflatespeed_reversed):
        raise Exception("cbor deflatespeed reverse failed on chunk" + str(chunk))

    time1_cbor_deflatedefault = time.time()

    chunk_cbor_deflatedefault = zlib.compress(chunk_cbor)[2:-4]
    chunk_cbor_deflatedefault_reversed = zlib.decompress(chunk_cbor_deflatedefault, -zlib.MAX_WBITS)

    time2_cbor_deflatedefault = time.time()

    if len(chunk_cbor) != len(chunk_cbor_deflatedefault_reversed):
        raise Exception("cbor deflatedefault reverse failed on chunk" + str(chunk))

    time1_cbor_deflatemax = time.time()

    chunk_cbor_deflatemax = zlib.compress(chunk_cbor, zlib.Z_BEST_COMPRESSION)[2:-4]
    chunk_cbor_deflatemax_reversed = zlib.decompress(chunk_cbor_deflatemax, -zlib.MAX_WBITS)

    time2_cbor_deflatemax = time.time()

    if len(chunk_cbor) != len(chunk_cbor_deflatemax_reversed):
        raise Exception("cbor deflatemax reverse failed on chunk" + str(chunk))

    chunk_obj = json.loads(chunk_json)
    chunk_obj["result"]["hex"] = str(base64.a85encode(headers_bytes, foldspaces=True))
    chunk_ascii85 = bytes(json.dumps(chunk_obj), "ascii")

    headers_bytes_deflatespeed = zlib.compress(headers_bytes, zlib.Z_BEST_SPEED)[2:-4]
    headers_bytes_deflatedefault = zlib.compress(headers_bytes)[2:-4]
    headers_bytes_deflatemax = zlib.compress(headers_bytes, zlib.Z_BEST_COMPRESSION)[2:-4]

    chunk_obj = json.loads(chunk_json)
    chunk_obj["result"]["hex"] = str(base64.a85encode(headers_bytes_deflatespeed, foldspaces=True))
    chunk_deflatespeed_ascii85 = json.dumps(chunk_obj)

    chunk_obj = json.loads(chunk_json)
    chunk_obj["result"]["hex"] = str(base64.a85encode(headers_bytes_deflatedefault, foldspaces=True))
    chunk_deflatedefault_ascii85 = json.dumps(chunk_obj)

    chunk_obj = json.loads(chunk_json)
    chunk_obj["result"]["hex"] = str(base64.a85encode(headers_bytes_deflatemax, foldspaces=True))
    chunk_deflatemax_ascii85 = json.dumps(chunk_obj)

    chunk_ascii85_deflatespeed = zlib.compress(chunk_ascii85, zlib.Z_BEST_SPEED)[2:-4]
    chunk_ascii85_deflatedefault = zlib.compress(chunk_ascii85)[2:-4]
    chunk_ascii85_deflatemax = zlib.compress(chunk_ascii85, zlib.Z_BEST_COMPRESSION)[2:-4]

    print(chunk, ",", len(chunk_json), ", ", 
          len(chunk_json_deflatespeed), ",", 
          int((time2_json_deflatespeed - time1_json_deflatespeed) * 1000), ", ",
          len(chunk_json_deflatedefault), ",", 
          int((time2_json_deflatedefault - time1_json_deflatedefault) * 1000), ", ",
          len(chunk_json_deflatemax), ",",
          int((time2_json_deflatemax - time1_json_deflatemax) * 1000), ",", 
          len(chunk_ascii85), ", ",
          len(chunk_deflatespeed_ascii85), ", ",
          len(chunk_deflatedefault_ascii85), ", ",
          len(chunk_deflatemax_ascii85), ", ",
          len(chunk_ascii85_deflatespeed), ", ",
          len(chunk_ascii85_deflatedefault), ", ",
          len(chunk_ascii85_deflatemax), ", ",
          len(chunk_cbor), ", ",
          len(chunk_cbor_deflatespeed), ",", 
          int((time2_cbor_deflatespeed - time1_cbor_deflatespeed) * 1000), ", ",
          len(chunk_cbor_deflatedefault), ",", 
          int((time2_cbor_deflatedefault - time1_cbor_deflatedefault) * 1000), ", ",
          len(chunk_cbor_deflatemax), ",",
          int((time2_cbor_deflatemax - time1_cbor_deflatemax) * 1000))
