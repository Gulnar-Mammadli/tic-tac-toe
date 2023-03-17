game_board = {'1': ' ' , '2': ' ' , '3': ' ' ,
              '4': ' ' , '5': ' ' , '6': ' ' ,
              '7': ' ' , '8': ' ' , '9': ' '}

keys = []

for i in game_board:
    keys.append(i)

def printBoard(board):
    print(board['1'] + '|' + board['2'] + '|' + board['3'])
    print('-+-+-')
    print(board['4'] + '|' + board['5'] + '|' + board['6'])
    print('-+-+-')
    print(board['7'] + '|' + board['8'] + '|' + board['9'])

def play():
    turn = 'X'
    count = 0


    for i in range(10):
        printBoard(game_board)
        print("It's your turn," + turn + ".Move to which place?")

        move = input()        

        if game_board[move] == ' ':
            game_board[move] = turn
            count += 1
        else:
            print("That place is already filled.\nMove to which place?")
            continue
 
        if count >= 5:
            if game_board['1'] == game_board['2'] == game_board['3'] != ' ':
                printBoard(game_board)
                print("\nGame Over.\n")                
                print(" **** " +turn + " won. ****")                
                break
            elif game_board['4'] == game_board['5'] == game_board['6'] != ' ': 
                printBoard(game_board)
                print("\nGame Over.\n")                
                print(" **** " +turn + " won. ****")
                break
            elif game_board['7'] == game_board['8'] == game_board['9'] != ' ': 
                printBoard(game_board)
                print("\nGame Over.\n")                
                print(" **** " +turn + " won. ****")
                break
            elif game_board['1'] == game_board['4'] == game_board['7'] != ' ': 
                printBoard(game_board)
                print("\nGame Over.\n")                
                print(" **** " +turn + " won. ****")
                break
            elif game_board['2'] == game_board['5'] == game_board['8'] != ' ': 
                printBoard(game_board)
                print("\nGame Over.\n")                
                print(" **** " +turn + " won. ****")
                break
            elif game_board['3'] == game_board['6'] == game_board['9'] != ' ':
                printBoard(game_board)
                print("\nGame Over.\n")                
                print(" **** " +turn + " won. ****")
                break 
            elif game_board['7'] == game_board['5'] == game_board['3'] != ' ': 
                printBoard(game_board)
                print("\nGame Over.\n")                
                print(" **** " +turn + " won. ****")
                break
            
            elif game_board['1'] == game_board['5'] == game_board['9'] != ' ': 
                printBoard(game_board)
                print("\nGame Over.\n")                
                print(" **** " +turn + " won. ****")
                break 

       
        if count == 9:
            print("\nGame Over.\n")                
            print("It's a Tie!!")

        if turn =='X':
            turn = 'O'
        else:
            turn = 'X'        
    
    restart = input("Do want to play Again?(y/n)")
    if restart == "y" or restart == "Y":  
        for key in keys:
            game_board[key] = " "

        play()
if __name__ == "__main__":
    play()