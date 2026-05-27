# Python program to print Fibonacci sequence

n = int(input("Enter number of terms: "))

a = 0
b = 1

print("Fibonacci Sequence:")

for i in range(n):
    print(a, end=" ")
    
    c = a + b
    a = b
    b = c
