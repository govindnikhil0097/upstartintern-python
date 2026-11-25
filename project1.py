def wordCount(s):
    wordsList = s.split()
    count = len(wordsList)
    return count

def longestWord(s):
    words = s.split()
    if not words:
        return ""
    return max(words, key = len)

def reverseSentence(s):
    rs = " ".join(s.split()[::-1])
    return rs

def isPrime(n):
    if n < 2:
        return f"{n} is not Prime"
    prime = True
    for i in range(2, int(n**0.5)+ 1):
        if n % i == 0:
            prime = False
            break
    if prime:
        return f"{n} is Prime"
    else:
        return f"{n} is not Prime"

def main():
    print("Welcome to the program!\n\n")
    print("Menu\n1. Word Count\n2. Longest Word\n3. Reverse Sentence\n4. Check if a number is Prime\n\n")
    try:
        choice = int(input("Enter your choice : "))
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 4")
        return
    
    if choice == 1:
        sentence = input("Enter a sentence : ")
        count = wordCount(sentence)
        print(f"The number of words in the sentence is {count}")
    elif choice == 2:
        sentence = input("Enter a sentence : ")
        longWord = longestWord(sentence)
        print(f"The longest word in the sentence is {longWord}")
    elif choice == 3:
        sentence = input("Enter a sentence : ")
        revSent = reverseSentence(sentence)
        print(f"The Reverse sentence is : {revSent}")
    elif choice == 4:
        try:
            num = int(input("Enter a number: "))  
            print(isPrime(num))
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
    else:
        print("Invalid choice. Please select an option from 1 to 4.")

if __name__ == "__main__":
    main()