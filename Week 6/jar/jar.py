
def main():
    jar = Jar()
    print(str(jar.capacity))
    jar.deposit(2)
    print(str(jar))
    jar.withdraw(12)
    print(str(jar))






class Jar:
    def __init__(self, capacity=12):
        self._capacity = capacity
        self._size = 0

    def __str__(self):
         return self._size * "🍪"

    def deposit(self, n):
        if n + self._size <= self._capacity and n >= 0:
            self._size += n
            print("Succeed.")
        else:
            raise ValueError("Excess amount of cookies.")

    def withdraw(self, n):
        if self._size - n >= 0:
            self._size -= n
            print("Succeed.")
        else:
            raise ValueError("It is illegal to take that much.")

    @property
    def capacity(self):
        return self._capacity

    @property
    def size(self):
        return self._size


main()