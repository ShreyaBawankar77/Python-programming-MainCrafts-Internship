# Python program to check Armstrong number

num = int(input("Enter a number: "))

temp = num
sum = 0
digits = len(str(num))

while temp > 0:
    digit = temp % 10
    sum += digit ** digits
    temp = temp // 10

if num == sum:
    print("Armstrong Number")
else:
    print("Not an Armstrong Number")
