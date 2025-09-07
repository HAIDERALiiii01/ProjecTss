print('''
⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡟⠀⠀⠉⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⠏⠀⠀⠀⢀⣾⢿⣿⣿⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⠃⠀⠀⠀⢠⡿⠃⠀⠉⠛⠿⣧⣀⠉⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⠃⠀⠀⠀⣠⡿⠁⠀⠀⠀⠀⠀⠈⠙⠻⣶⣄⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⡿⠁⠀⠀⠀⣰⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣷⣄⡀⢀⣼⣏⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣹⡟⠀⠈⠙⢿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠟⠀⠀⠀⢠⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡋⠙⠻⣦⣄⠀⠀⠀⠀⠀⠀⢀⣼⠏⠀⠀⠀⢠⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠷⣦⣄⠉⣻⣶⣤⣀⠀⢀⣾⠃⠀⠀⠀⣠⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀⣰⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣤⡀⠀⠀⣴⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⡟⠁⠀⠀⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⡟⠀⠀⠀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣤⣤⣤⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿

''')

auc_dic = {}
while True:
    name_of_user = input("Enter your name: ")
    bid_of_user = input("Enter your bid: $")
    auc_dic[name_of_user] = bid_of_user
    
    any_more = input("Are there other users who wants to bid?? y/n\n").strip().lower()
    if any_more =="y":
        print("\n" * 100)    
    elif any_more =="n":
        break
    else:
        print("Please type 'y' or 'n'.") 

highest_bid = 0   
winner = ""         
for auction in auc_dic:
        score = int(auc_dic[auction])
        if score > highest_bid:
            highest_bid = score
            winner = auction

print(f"The highest bid is from {winner}, which is ${highest_bid}")            