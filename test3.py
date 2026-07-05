def is_even(num): return num % 2 == 0 
def is_odd(num): return not is_even(num)
def main(): print("Enter a number: ") num = int(input()) if is_odd(num): print(f"{num} is odd.") else: print(f"{num} is even.") if __name__ == "__main__": main()