# Python program to check palindrome

text = input("Enter a string: ")

reverse_text = text[::-1]

if text == reverse_text:
    print("Palindrome")
else:
    print("Not a Palindrome")
