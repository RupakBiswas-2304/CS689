import random
import argparse
import numpy as np

class CustomGate:
    def __init__(self, qbit = 2) -> None:
        self.qbit = qbit
        self.matrix = np.zeros((2**qbit,2**qbit), dtype=int)
        self.matrix_rev = None
        self.inputs = [i for i in range(2**qbit)]

    def truth_table(self):
        input = np.array([self.encode(i) for i in self.inputs])
        output = np.matmul(self.matrix, input)
        
        print("Truth Table")
        for i in range(2**self.qbit):
            inp, out = "", ""
            for j in range(2**self.qbit):
                inp += str(input[i][j][0])
                out += str(output[i][j][0])

            print(f"{self.simple_decode(inp)} -> {self.simple_decode(out)}")
    
    def encode(self, val):
        zero = np.array([[1], [0]])
        one = np.array([[0], [1]])
        x = one if val%2 else zero
        val = val//2
        t = self.qbit - 1
        while val or t:
            x = np.kron( one if val%2 else zero, x)
            val = val//2
            t -= 1
        return x
    
    def simple_decode(self, x):
        val = 0
        for _x in x:
            if _x == "1":
                return val
            val += 1
        return val

    
    def __str__(self) -> str:
        res = ""
        for row in self.matrix:
            for element in row:
                res += "{},".format(element)
            res += "\n"
        return res
    
    def str_arr(self):
        for row in self.matrix:
            for element in row:
                print(element)
    
    def hotencode(self, p):
        r = [0]*(2**self.qbit)
        r[p] = 1
        return r

    def generate_random_permutation(self):
        P = [i for i in range(2**self.qbit)]
        Q = [0]*(2**self.qbit)
        random.shuffle(P)
        x, y = [], []
        idx = 0
        for p in P:
            Q[p] = idx
            idx += 1
            x.append(self.hotencode(p))

        for q in Q:
            y.append(self.hotencode(q))
        
        self.matrix_rev = np.array(y)
        self.matrix = np.array(x)

    def load_random_permutation(self):
        permute_matrix = f"./input/permute_matrix_{self.qbit}.txt"
        reverse_permute_matrix = f"./input/reverse_permute_matrix_{self.qbit}.txt"

        with open(permute_matrix, "r") as f:
            self.matrix = np.array([[int(i) for i in line.strip()[:-1].split(",")] for line in f.readlines()])
            f.close()
        with open(reverse_permute_matrix, "r") as f:
            self.matrix_rev = np.array([[int(i) for i in line.strip()[:-1].split(",")] for line in f.readlines()])
            f.close()
        
        self.matrix = self.matrix.reshape((2**self.qbit,2**self.qbit))
        self.matrix_rev = self.matrix_rev.reshape((2**self.qbit,2**self.qbit))

    def save_random_permutation(self):
        permute_matrix = f"./input/permute_matrix_{self.qbit}.txt"
        reverse_permute_matrix = f"./input/reverse_permute_matrix_{self.qbit}.txt"

        with open(permute_matrix, "w") as f:
            for row in self.matrix:
                for element in row:
                    f.write("{},".format(element))
                f.write("\n")
            f.close()
        with open(reverse_permute_matrix, "w") as f:
            for row in self.matrix_rev:
                for element in row:
                    f.write("{},".format(element))
                f.write("\n")
            f.close()



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--qbit", type=int, default=4)
    parser.add_argument("--generate", action="store_true", default=False)
    parser.add_argument("--save", action="store_true", default=False)

    args = parser.parse_args()
    qbit = args.qbit
    generate = args.generate
    save = args.save

    gate = CustomGate(qbit)

    if generate:
        gate.generate_random_permutation()
    else:
        gate.load_random_permutation()

    if save:
        gate.save_random_permutation()
    # print(gate)
    gate.truth_table()

    gate.matrix = gate.matrix_rev
    # print(gate)
    gate.truth_table()
    