import os
from userid import *

def begin():
    '''
    Deletes .pyc files and runs the program.
    '''
    # Opens file directory
    directory = os.listdir('.')
    for filename in directory:
        # Delete pyc memory files
        if filename[-3:] == 'pyc':
            os.remove(filename)

    start = Tk()

    # Create GUI instance, open program window
    openwindow = Login(start)


def main():
    """A while loop that continues running the program when user exits the gui, prompting the user
       if they want to continue using the program 
    input:
        1. finish - string - user input yes/no to determine the full exit or the restart of the application
    returns:
        1. begin() - function call that opens the program window
    """
    #set done variable to false
    done = False

    while not done: #while loop that keeps running the program until user wants to exit

        begin() #function call that opens the tkinter window application

        full_exit = False #set full_exit variable to false

        while not full_exit:
            try: #error handling
                finish = raw_input("Login as another user? (yes/no):")

                #ends both while loops smoothly and completely exits the application
                if finish.lower() == "no":
                    full_exit = True
                    done = True

                #stops the program from asking the user input question and runs the application again
                elif finish.lower() == "yes":
                    full_exit = True

                #raises value error and asks the user to input answer until the right answers are entered
                elif finish.lower() != "no" or finish.lower() != "yes":
                    raise ValueError("Invalid Input")


            except ValueError,errorvar:
                print errorvar,": Please enter 'yes' or 'no'"

print("Test Script GUI")
print("---------------")

# Function call to run the entire application
main() 