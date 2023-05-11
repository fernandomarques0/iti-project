import sys
import os

from datetime import datetime
from functions import *

arg1 = sys.argv[1] # Recebe 'txt' ou 'mp4'
arg2 = sys.argv[2] # Recebe 'nomedoarquivo.txt' ou 'nomedoarquivo.mp4'

# Executa compressão e descompressão de 9bits até 16bits.
for i in range(9,17):
    N_BITS = i
    print(f"EXECUTANDO COM {N_BITS} bits - arquivo {arg1}\n")
    
    msg = read_file(arg2)
    start = datetime.now()
    msg_compress = compressor_lzw(msg, N_BITS)
    end = datetime.now()
    print(f"Tempo de compressão = {end - start}")

    generate_file(msg_compress)
    tamanho_arquivo = os.path.getsize("compressed-file.lzw")
    mb = tamanho_arquivo/(1024*1024)
    print(f"Arquivo comprimido gerado com tamanho = {mb:.2f}mb")

    start = datetime.now()
    msg_descompress = descompressor_lzw(msg_compress, N_BITS)
    end = datetime.now()
    print(f"Tempo de descompressão = {end - start} \n")
    genarate_decompressed_file(msg_descompress, arg1)
