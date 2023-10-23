from typing import Any
import random
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import argparse
### lets design a 8 bit hash function that is secure and collision resistant on classical computers
def to_bitstring(num):
    return "{0:08b}".format(num)


class Hash:
    def __init__(self, length = 8) -> None:
        self.length = length
    
    def __call__(self, input) -> Any:
        return self.__hash__(input)

    def plot(self, scale = 1):
        data = []
        for i in range(self.length*scale):
            data.append([ self.__hash__(i*self.length + j) for j in range(self.length)])
        fig, ax = plt.subplots()
        im = ax.imshow(data)
        fig.colorbar(im)
        plt.show()

    def testCollision(self):
        s = {}
        for i in range(0,256):
            hashed = self.__hash__(i)
            if hashed in s:
                print("Collision found for inputs {} and {}".format(s[hashed],i))
            else:
                s[hashed] = i
        print("No collisions found")

class XorHASH(Hash):
    def __init__(self) -> None:
        super().__init__()
    
    def __hash__(self, input):
        return input^0b01101001
    
class PearsonHash(Hash):
    def __init__(self, length = 8) -> None:
        super().__init__(length)
        self.T = [i for i in range(2**self.length)]
        random.shuffle(self.T)
        # self.T = self.easy_suffle()

    def __hash__(self, input) -> int:
        try:
            data = ''.join(format(byte, '08b') for byte in input.encode())
        except:
            data = "{0:08b}".format(int(input))
        
        hash = self.T[int(data[:self.length],2)]
        blocks = len(data)//self.length

        for i in range(1,blocks):
            hash = self.T[hash ^ int(data[i*self.length:(i+1)*self.length],2)]
        return hash
    
    @staticmethod
    def easy_suffle():
        T = [i for i in range(256)]
        def convert(x):
            x = list("{0:08b}".format(x))
            x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7] = x[5], x[4], x[3], x[0], x[2], x[6], x[7], x[1]
            return int("".join(x),2)
        return list(map(convert,T))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hash Function')
    parser.add_argument("--n", type=int, default=8)
    parser.add_argument("--extend", type=int, default=1)

    args = parser.parse_args()
    print(args.n)

    hasher = PearsonHash(args.n)
    hasher.plot(args.extend)
    # print(hasher("Hello"))

        
    
        
            

