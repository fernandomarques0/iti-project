from datetime import datetime
from functions import *

K = [9, 10, 11, 12, 13, 14, 15, 16]
PERSONS = 40
FACES = 10
success = []

for k in K:
    start = datetime.now()
    tests = []
    dictionarys = []
    quantity_success = 0

    for i in range(PERSONS):
        img = []

        for j in range(FACES):
            file = f"orl_faces/s{i+1}/{j+1}.pgm"
            content = read_file(file)
            img.append(content)

        number = random.randint(0, FACES-1)
        tests.append(img[number])
        del img[number]

        dictionarys.append(compressor_lzw(img, k, 2**k))

    for i in range(len(tests)):
        m_value = float('inf')
        index = -1

        for j in range(len(dictionarys)):
            leng = test(tests[i], dictionarys[j], k, 2**k)

            if leng < m_value:
                m_value = leng
                index = j

        if i == index:
            quantity_success += 1

    end = datetime.now()
    success.append(quantity_success)
    print(f"K: {k}")
    print(f"success: {quantity_success}")
    print(f"Execution time: {end - start}\n")
