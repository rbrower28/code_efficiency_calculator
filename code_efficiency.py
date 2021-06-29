""" This is the Code Efficiency Calculator.
Ever wonder how efficient your code really is?

This finds the amount of 'executable' lines of code in any python file.
Executable means every line that is essential to fulfill the purpose
of the program. This excludes:
- lines that start with #
- blank lines
- any line inside triple quotes (like this one!)

For example, all of these first few lines are non-executable!
Being comments, the computer doesnt actually run them, and the
code would be the same without!

For each file examined displays:
the total number of lines
number of lines that are executed when run
percent of lines run compared to the total
"""

import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename


def main():
    """ Runs the main portion of the code, which displays the
    screen and draws the user interface.

    Returns: nothing
    """

    # creates a tkinter interface
    root = tk.Tk() # assigns the screen to a variable
    root.title("Code Executability Calculator") # screen title
    style = ttk.Style() # ensures compatibility with color changes
    style.theme_use('classic')

    # sets the width and height of the screen
    canvas = tk.Canvas(root, width=400, height=350, bg="white")
    canvas.grid(rowspan=2)

    # sets up the initial display, performs the rest of the functions
    draw_startup(root, canvas)

    # runs the program on a tkinter interface until the page is closed
    root.mainloop()


def draw_startup(root, canvas):
    """ Lays out the startup page and sets up the interactible
    parts of the program. the parameter 'root' is the open page
    and 'canvas' is the interface tied to tkinter & its functions.

    Returns: nothing
    """

    # displays the startup text, which includes a description and instrucitons
    tb_text = tk.StringVar() # makes the text modifiable
    # displays the text box with the instructions
    text_box = tk.Label(root, font=("Helvetica", "24", "bold"),
            textvariable=tb_text, bg="white", padx=20, pady=10)
    tb_text.set("How many lines of\nyour code does your\ncomputer really need?"
            "\n\nUpload your own python\nfile to find out:")
    text_box.grid(column=0, row=0) # centers the text on the top row

    # makes the main button for the program, activates the function 'process_file'
    button_text = tk.StringVar() # makes the button text modifiable
    file_search = tk.Button(root, textvariable=button_text,
            font=("Helvetica", "24"), padx=10, pady=15, foreground="dodger blue",
            command=lambda:process_file(root, button_text, tb_text, canvas))
    button_text.set("Browse")
    file_search.grid(column=0, row=1) # centers the text on the 2nd row


def process_file(root, button_text, tb_text, canvas):
    """ Activated by the button on the lower half of the
    interface. Allows the user to search in the finder for
    a .py file, calls the function 'strip_code()', then
    modifies the text and button with 'write_results()'.

    Returns: nothing
    """

    button_text.set("loading...")

    # opens a finder window to search for a .py file
    py_file = askopenfilename(parent=root, title="Choose a file", filetypes=[("Python file", "*.py")])
    
    try:
        # reads every line of the code file and returns the total
        # amount of lines and the amount needed to run
        total_lines, exec_lines = strip_code(py_file)

        """ IF YOU WANT TO SEE THE END RESULTS IN THE TERMINAL
        UNCOMMENT THE FOLLOWING LINE. """
        # print(f"total: {total_lines}\nexecutable: {exec_lines}")

        # refresh(canvas)

        # changes the screen to display the final information
        write_results(total_lines, exec_lines, tb_text)
 
    except ZeroDivisionError:
        """ If the function tries to divide a number by zero, that means
        the total amount of lines is 0, making it a blank file.
        """
        tb_text.set("The file you chose is blank.\n\nPlease try again!")

    finally:
        button_text.set("Try another file") # pressing the button will repeat with another file


def strip_code(py_file):
    """ Runs through every line of the selected python file and designates
    each line as executable or not. Executable means not a blank space or
    a comment, or any line inside a triple quote.

    Returns:
    - The total lines of the code
    - The number of lines needed to run
    """

    with open(py_file, mode="rt") as python_file: # opens the file

        # starts both line counts at 0
        total_lines = 0
        executable_lines = 0

        # both booleans are for checking execuatability
        count_next = True
        trip_quote = False

        for line in python_file: # runs through each line in the file

            total_lines += 1 # increases the total line count by 1

            # if currently inside triple quotes, skip this block
            if trip_quote == False:
                count_next = True

                index = 0 # sets the index for the first character of the line.
                # if the first character is a space, it might be an indented line,
                # so we skip every space until we hit a readable character.
                while line[index] == " ":
                    index += 1 
                
                first_character = line[index] # sets the first character to a variable

                # starting with a comment mark or an enter means the line is non-executable
                if first_character in ("\n", "#"):
                    count_next = False

                # lines starting with triple quotes are also non-executable
                elif first_character == "\"" and line[index + 1] == "\"" and line[index + 2] == "\"":
                    count_next = False
                elif first_character == "\'" and line[index + 1] == "\'" and line[index + 2] == "\'":
                    count_next = False
                
            # if the line doesnt start with a comment, enter or triple quote,
            # then it must be run by the computer. If it qualifies, we add 1
            # to the 'executable_lines' count.
            if count_next:
                executable_lines += 1

            """ IF YOU WANT TO SEE EACH LINE WITH ITS STATUS IN THE TERMINAL
            UNCOMMENT THE FOLLOWING LINE. """
            # print(f"{count_next}: {line}")
            
            quote_count = 0 # starts the count of quotes in the line

            for i in line: # goes through each letter of the line

                # if a character is a single or double quote, add one
                # to the count. If not, reset the count to 0.
                if i == "\"" or i == "\'":
                    quote_count += 1
                else:
                    quote_count = 0

                # when we count three quotes in a row, we set 'triple_quote'
                # to true, which will make every line non-executable until
                # 3 quotes in a row are found again.
                if quote_count == 3 and trip_quote == True:
                    trip_quote = False
                    count_next = True
                    quote_count = 0

                elif quote_count == 3 and trip_quote == False:
                    trip_quote = True
                    count_next = False
                    quote_count = 0

    # returns both the total number of lines and the number that are run by the computer
    return total_lines, executable_lines


def write_results(total_lines, executable_lines, tb_text):
    """ Changes the interface text to display the file information
    found by 'strip_code'. Adds additional messages based on an
    extremely high or low percent executable lines of code.

    Returns: nothing
    """

    # calculates the percent of executable lines compared to the total
    exec_percent = (executable_lines / total_lines) * 100

    # defines 'msg' based on how high or low the resulting percent is
    if exec_percent > 75: # from 75% - 100%
        msg = "\nNow THAT's some\nefficient code!"
    elif exec_percent < 25: # from 0% - 25%
        msg = "\nWow... You must\nreally like comments!"
    else: # if the percent is between 25% and 75%, removes the message
        msg = ""

    # changes the text box to display the results
    # will redisplay for every code run through the program
    tb_text.set(f"Your code has a total\nof {total_lines} lines, but\nonly {executable_lines} "
            f"are run\nby the computer!\n\nThat's only {exec_percent:.1f}%!" + msg)


def refresh(self):
    self.destroy()
    self.__init__()


# calls the function main() and starts the program
if __name__ == "__main__":
    main()