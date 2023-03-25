

def list_tutorial():
    print("------------------WELCOME CLIENT!-----------------------------")
    print("Here is how the game will proceed: ")
    print("1. You as the client put your name and the port to run.")
    print("   Pick one port from 50051, 50052 or 50053")
    print("2. You are allowed to proceed Ring algorithm(election). Or just skip and wait until the election is succeed.")
    print("   Make sure that one out of 3 clients runs the election")
    print("   The winner will be the admin(aka. game master or leader) of the game")
    print("3. After successful election. Press enter to get in the game")
    print("-----------------------------------------------")

def list_game_cmd():
    print("-----------------------------------------------")
    print("How to play the game: ")
    print("1. you will be assigned the symbol from the game master.")
    print("2. once it is your turn, just give the position at range 1-9.")
    print("3. or type other command.")
    print("------3.1. ""board"" to see current game board")
    print("------3.2. ""status"" or just press enter to check if it is your turn")
    print("------3.3. ""countdown"" time left over in your turn")
    print("------3.4. ""cls"" to clear the screen")
    print("------3.5. ""quit"" to left the game")
    print("-----------------------------------------------")

def list_ADMIN_cmd():
    print("-------------------YOUR PRIVILEGES----------------------------")
    print("How to use game master cmds: ")
    print("1. you will be assigned the symbol from the game master.")
    print("2. once it is your turn, just give the position at range 1-9.")
    print("3. or type other command.")
    print("------3.1. ""board"" to see current game board")
    print("------3.2. ""status"" or just press enter to check if it is your turn")
    print("------3.3. ""countdown"" time left over in your turn")
    print("------3.4. ""cls"" to clear the screen")
    print("------3.5. ""quit"" to left the game")
    print("-----------------------------------------------")