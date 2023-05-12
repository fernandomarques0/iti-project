import bitarray

def read_file(arg2):
    with open(arg2, 'rb') as file:
        bytes_array = []
        byte = file.read(1)
        while byte:
            value = int.from_bytes(byte, byteorder='little')
            bytes_array.append(value)
            byte = file.read(1)
    
    return bytes_array

def compressor_lzw(data, N_BITS, dict_length):
    dictionary = {i.to_bytes(): i for i in range(256)} 
    message = bitarray.bitarray() 

    flag = 0
    s = data[0].to_bytes()  
    for char in range(len(data)):

        if (char+1) >= len(data):
            if s in dictionary:
                message.extend(bin(dictionary[s])[2:].zfill(N_BITS))
                break
        else:
            c = data[char+1].to_bytes()
        
        seq = [s, c]
        seq = ''.join([byte.decode('iso-8859-1') for byte in seq])

        if seq.encode() in dictionary:
            s = seq.encode()
        else:
            message.extend(bin(dictionary[s])[2:].zfill(N_BITS))   

            if len(dictionary) == dict_length:
                flag = 1
                s = c
                continue
            else:
                dictionary[seq.encode()] = len(dictionary)  
                
            s = c
    if flag:
        print("Dictionary is full")
    return message
    

def descompressor_lzw(data, N_BITS, dict_length):
    dictionary = {i: i.to_bytes() for i in range(256)} 
    s = ""
    msg_decompress = []  
    i = 0

    while i < len(data):
        cod =  int(data[i:i+N_BITS].to01(), 2)  
        i += N_BITS 

       
        if cod in dictionary:
            current_out = dictionary[cod]   
        elif cod >= len(dictionary):    
            if s:
                current_out = s + s[0].to_bytes() 
            else:
                current_out = s 
        else:
            raise ValueError('Error')

        msg_decompress.append(current_out) 
        if s:
            if len(dictionary) == dict_length: 
                s = current_out
                continue
            else:
                dictionary[len(dictionary)] = s + current_out[0].to_bytes() 
        
        s = current_out
    
    return msg_decompress

def generate_file(data):
    with open('compressed-file.lzw', 'wb') as f:  
        f.write(data.tobytes())

def genarate_decompressed_file(data, arg1):
    if arg1 == 'mp4':
        with open('descompress-disco.mp4', 'wb') as f: 
            for b in data:
                f.write(b)

    elif arg1 == 'txt':
        new_message = ''.join([b.decode('iso-8859-1') for b in data]) 
        with open('descompress-file.txt', 'w') as f: 
            f.write(new_message)
