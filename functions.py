import bitarray

# LER ARQUIVO BYTE A BYTE E ADICIONA NUMA LIST O VALOR INTEIRO REFERENTE AO BYTE.
def read_file(arg2):
    with open(arg2, 'rb') as file:
        bytes_array = []
        byte = file.read(1)
        while byte:
            value = int.from_bytes(byte, byteorder='little')
            bytes_array.append(value)
            byte = file.read(1)
    
    return bytes_array

# LER ARQUIVO BYTE A BYTE E ADICIONA NUMA LIST O VALOR INTEIRO REFERENTE AO BYTE.
def compressor_lzw(data, N_BITS):
    dictionary = {i.to_bytes(): i for i in range(256)} # Dicionário referencia o caracterer em byte e seu código ascii
    message = bitarray.bitarray() # BitArray que armazena os bits comprimidos.

    flag = 0
    s = data[0].to_bytes()  # Recebe valor em inteiro e converte para bytes.
    for char in range(len(data)):

        # Verifica se o próximo caracterer chegou no final da lista de data, adiciona o ultima sequencia no array de bits
        if (char+1) >= len(data):
            if s in dictionary:
                message.extend(bin(dictionary[s])[2:].zfill(N_BITS))
                break
        else:
            c = data[char+1].to_bytes()
        
        # Cria uma lista de bytes e depois converte a lista para string, decodificando para iso-8859-1, pois o default é utf-8 e alguns códigos dariam erro.
        seq = [s, c]
        seq = ''.join([byte.decode('iso-8859-1') for byte in seq])

        # Verifica se a seq em byte existe no dictionary.
        if seq.encode() in dictionary:
            s = seq.encode()
        else:
            message.extend(bin(dictionary[s])[2:].zfill(N_BITS))   # Adiciona código ascii em n_bits no array de bits.

            # Verifica se o dicionário chegou no limite e torna estático.
            if len(dictionary) == 2**N_BITS:
                flag = 1
                s = c
                continue
            else:
                dictionary[seq.encode()] = len(dictionary)  # Adiciona no dicionário com key = byte e código em inteiro.
                
            s = c
    if flag:
        print("Dicionário encheu")
    return message
    

def descompressor_lzw(data, N_BITS):
    dictionary = {i: i.to_bytes() for i in range(256)} # Dicionário referencia o codigo ascii com seu caracterer em byte
    s = ""
    msg_decompress = []  # Lista que irá armazenar o data descomprimido.
    i = 0

    while i < len(data):
        cod =  int(data[i:i+N_BITS].to01(), 2)  # Converter o byte do i para seu valor em inteiro.
        i += N_BITS # Percorre o array de bits de n_bits em n_bits.

        # Verifica se o código está no dictionary
        if cod in dictionary:
            current_out = dictionary[cod]   # A saida atual se torna o caractere em byte do código encontrado.
        elif cod >= len(dictionary):    # Verifico se código recebido tem um valor maior que o tamanho do dicionário (significa que não está inserido ainda)
            if s:
                current_out = s + s[0].to_bytes() # Adiciona a saida atual como o caractere anterior + caractere inicial dele em bytes.
            else:
                current_out = s 
        else:
            raise ValueError('Erro')

        msg_decompress.append(current_out) # Adiciona na lista de saída o valor da saida atual.
        if s:
            if len(dictionary) == 2**N_BITS: # Se o dicionário chegou ao limite, torna estático.
                s = current_out
                continue
            else:
                dictionary[len(dictionary)] = s + current_out[0].to_bytes() # Adiciona no dicionário a key = código e seu caractere anterior + caractere inicial da saida atual em bytes.
        
        s = current_out
    
    return msg_decompress

def generate_file(data):
    with open('compressed-file.lzw', 'wb') as f:  # Gera arquivo comprimido.
        f.write(data.tobytes())

def genarate_decompressed_file(data, arg1):
    if arg1 == 'mp4':
        with open('descompress-disco.mp4', 'wb') as f: # Gera arquivo mp4 descomprimido e "tocável"
            for b in data:
                f.write(b)

    elif arg1 == 'txt':
        new_message = ''.join([b.decode('iso-8859-1') for b in data]) # Concatena todos os bytes presentes na lista descomprimida e decodifica para utf8, tornando string.
        with open('descompress-file.txt', 'w') as f: # Gera arquivo txt descomprimido.
            f.write(new_message)
