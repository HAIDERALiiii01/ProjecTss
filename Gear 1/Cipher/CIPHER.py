alphabets = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def cipher():
    print('''
                                   88                                 
                                   88                                 
                                   88                                 
 ,adPPYba, 8b       d8 8b,dPPYba,  88,dPPYba,   ,adPPYba, 8b,dPPYba,  
a8"     "" `8b     d8' 88P'    "8a 88P'    "8a a8P_____88 88P'   "Y8  
8b          `8b   d8'  88       d8 88       88 8PP""""""" 88          
"8a,   ,aa   `8b,d8'   88b,   ,a8" 88       88 "8b,   ,aa 88          
 `"Ybbd8"'     Y88'    88`YbbdP"'  88       88  `"Ybbd8"' 88          
               d8'     88                                             
              d8'      88                                             
''')
    decision =  input("Type 'encode' to encrypt, type 'decode' to decrypt: \n").strip().lower()
    message = input("Type your message: ").strip().lower()
    shift = int(input("Type the shift number: "))

    def encrypt(original_text, shift_amount):
        cipher_text = ""

        for letter in original_text:
            if letter in alphabets:
                shifted_position = alphabets.index(letter) + shift_amount
                cipher_text += alphabets[shifted_position % len(alphabets)]
            else:
                cipher_text += letter  
 

        print(f"Here is the encoded code: {cipher_text}")
        print('''
░█▀▀░█▀█░█▀▀░█▀█░█▀▄░█▀▀░█▀▄
░█▀▀░█░█░█░░░█░█░█░█░█▀▀░█░█
░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀▀░░▀▀▀░▀▀░
''')

    def decrypt(original_text, shift_amount):
        cipher_text = ""

        for letter in original_text:
            if letter in alphabets:
                shifted_position = alphabets.index(letter) - shift_amount
                cipher_text += alphabets[shifted_position % len(alphabets)]
            else:
             cipher_text += letter  

    

        print(f"Here is the decoded code: {cipher_text}")
        print('''
░█▀▄░█▀▀░█▀▀░█▀█░█▀▄░█▀▀░█▀▄
░█░█░█▀▀░█░░░█░█░█░█░█▀▀░█░█
░▀▀░░▀▀▀░▀▀▀░▀▀▀░▀▀░░▀▀▀░▀▀░
''')


        

    if decision == "encode":
        encrypt(original_text=message, shift_amount=shift)
    elif decision == "decode":
        decrypt(original_text=message, shift_amount=shift)    
    else:
        print("Please choose between 'encode' and 'decode'.")
cipher()

while True:
    once_more = input("Do you want to run the code again??\nIf yes then type 'y'\nIf no then type 'n'\nYour choice: ").strip().lower()
    if once_more == "y":
        cipher()
    elif once_more == "n":
        print("Okay then.")
        break
    else:
        print("Invalid input! Please from 'y' or 'n'")        