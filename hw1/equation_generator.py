import random
import string

OPERATORS = ['+', '-', '*']

GROUP_KEYS = {
    'op': 0,
    'int': 1,
    'alpha': 2,
    'space': 3,
    'etc': 4,
}

RANDOM_GEN_DICT = {
    'op': 1,
    'int': 20,
    'alpha': 20,
    'space': 2,
    'etc': 1,
}

def choose(dict):
    key_weight_array = [(key, dict[key]) for key in dict]
    key_weight_array.sort(key=lambda x: x[1])
    total_weight = sum([dict[key] for key in dict])
    rand = random.randrange(0, total_weight)
    bound = 0
    for (key, weight) in key_weight_array:
        bound += weight
        if (rand < bound):
            return key

def gen_op():
    return OPERATORS[random.randrange(0, len(OPERATORS))]

def gen_int():
    return str(random.randrange(0, 1000))

def gen_alpha():
    return random.choice(string.ascii_lowercase)

def gen_space():
    return ' '

def gen_etc():
    return random.choice(string.punctuation + string.ascii_uppercase)

def gen_alpha_or_int():
    if (random.getrandbits(1)):
        return gen_alpha()
    else:
        return gen_int()

def gen_random(length):
    str = ''
    key = None
    while (len(str) < length):
        if (key == 'alpha' or key == 'int'):
            weight_dict = {
                'op': 30,
                'int': 1,
                'alpha': 1,
                'space': 1,
                'etc': 1,
            }
        else:
            weight_dict = RANDOM_GEN_DICT
        key = choose(weight_dict)

        if (key == 'op'):
            str += gen_op()
        elif (key == 'int'):
            str += gen_int()
        elif (key == 'alpha'):
            str += gen_alpha()
        elif (key == 'space'):
            str += gen_space()
        else:
            str += gen_etc()
    if (key == 'op'):
        str = str[0:len(str) - 1]
    return str



def gen_valid(length):
    str = ''
    i = 0
    while (len(str) < length):
        if (random.random() < 0.15):
            str += gen_space()

        if (i % 2 == 0):
            str += gen_alpha_or_int()
        else:
            str += gen_op()
        i+=1

    if (i % 2 == 0):
        str += gen_alpha_or_int()
    return str

def main():
    f_w = open("input.txt", 'w')
    # valid
    for i in range(10):
        f_w.write(gen_valid(random.randrange(0,3)))
        f_w.write('\n')
    for i in range(60):
        f_w.write(gen_valid(random.randrange(3,10)))
        f_w.write('\n')
    for i in range(45):
        f_w.write(gen_valid(random.randrange(10,50)))
        f_w.write('\n')
    for i in range(30):
        f_w.write(gen_valid(random.randrange(50,200)))
        f_w.write('\n')
    for i in range(15):
        f_w.write(gen_valid(random.randrange(200,500)))
        f_w.write('\n')

    # both valid and invalid
    for i in range(10):
        f_w.write(gen_valid(random.randrange(0,3)))
        f_w.write('\n')
    for i in range(20):
        f_w.write(gen_random(random.randrange(3,10)))
        f_w.write('\n')
    for i in range(15):
        f_w.write(gen_random(random.randrange(10,50)))
        f_w.write('\n')
    for i in range(10):
        f_w.write(gen_random(random.randrange(50,200)))
        f_w.write('\n')
    for i in range(5):
        f_w.write(gen_random(random.randrange(200,500)))
        f_w.write('\n')
    f_w.close()

if __name__ == "__main__":
    main()
