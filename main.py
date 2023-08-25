"""Main file for OpenAV"""
import os
from colorama import init,Fore, Back, Style
init()

#Cleaning the command prompt...
def clean_prompt():
    os.system('cls')



clean_prompt() #Cleaning prompt....
print(Fore.CYAN+"""
#########   #########   #########   #     #          #          #           #
#       #   #       #   #           ##    #         #  #         #         #
#       #   #########   #           # #   #        #    #         #       #
#       #   #           #######     #  #  #       ########         #     #
#       #   #           #           #   # #      #        #         #   #
#       #   #           #           #    ##     #          #         # #
#########   #           #########   #     #    #            #         #

"""+ Fore.LIGHTMAGENTA_EX+"\nIt's AKAP.Keep your security to us...\n\n")
print(Fore.YELLOW+'[!]To see help dialog use command help.\n')
#Asking for command....
while True:
    cmd = input(Fore.GREEN+'>>>')

    if cmd.lower() == 'exit':
        print(Fore.RED+'[*]Exiting the software.The program will run in background to provide you security...')
        break

    elif cmd.lower() == 'help':
        print(Fore.LIGHTMAGENTA_EX+"""
#HELP:To show this dialog...
#EXIT:To exit the program inteface...
#SCAN:To initiate scan of a file or folder...
#PASSSAFE:To enter password bank...
#QUARLIST:To see the quarntine...
#ACITVITY:View recent AV activity...
"""+Fore.RED+"""
#UPDATE:update databases...
#UNINSATALL:To delete reminants and remove the drivers...

        """)
    elif cmd.lower() == 'update':
        os.system('update.bat')

        
print(Style.RESET_ALL) #Resetiing fonts....