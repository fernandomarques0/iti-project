import sys
import os

from datetime import datetime
from functions import *

arg1 = sys.argv[1] 
arg2 = sys.argv[2] 

N_BITS = 9

dict_length = 2**N_BITS

msg = read_file(arg2)
start = datetime.now()
msg_compress = compressor_lzw(msg, N_BITS, dict_length)
end = datetime.now()
print(f"Tempo de compressão = {end - start}")

generate_file(msg_compress)

start = datetime.now()
msg_descompress = descompressor_lzw(msg_compress, N_BITS, dict_length)
end = datetime.now()

print(f"Tempo de descompressão = {end - start} \n")
genarate_decompressed_file(msg_descompress, arg1)
