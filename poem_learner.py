#!/usr/bin/Python
from getch import getch
from sys import argv, stdin, stdout, exit
from os import system


# return lines from file
def get_poem_line_list(filename):
    if not filename:
        filename = raw_input(" What is the text file name? > ")
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    return lines


class PoemRunner:
    """Creates PoemLine objects out of lines and controls the top level running"""

    def __init__(self, line_list):
        self.line_list = line_list
        self.poemlines = []
        self.makeLines()
        self.learned = []
        self.ind = 0
        print self.poemlines
        self.startLearn()

    def makeLines(self):
        # I wonder if there is a more Pythonic way of doing this..
        first = self.line_list[0].strip()
        for line in [line.strip() for line in self.line_list if line.strip()][1:]:
            p = PoemLine(first, line)
            first = line
            self.poemlines.append(p)

    def startLearn(self):
        # groan
        while 1:
            self.getNext()

    def getNext(self):
        n = self.poemlines[self.ind]
        by = n.ask()
        self.ind += by
        
        #make sure index stays in range (cant move above and below "buffer")
        if self.ind < 0 : self.ind = 0
        if self.ind == len(self.poemlines): self.ind -= 1

class PoemLine:
    """Each PoemLine object includes the current line and next line.
    The next line can be seen one word at a time.
    a = beginning of line (clear next line)
    f = forward one word
    n = forward one line
    q = quit
    """

    def __init__(self, line, nextline):
        self.line = line
        self.nextline = nextline
        self.makeWords()
        self.hints = []

    def makeWords(self):
        temp = []
        for word in self.nextline.split():
            temp.append(word)
        self.nextline = temp
    
    def ask(self):
        i = 0
        # Don't think system actually throws an error
        # Might not work under Windows.
        try: 
            system('clear')
        except:
            system('cls')
        print self.line

        while i < len(self.nextline):
            a = getch().lower()
            while a not in 'fnpqa':
                a = getch().lower()

            # get a hint (forward)
            if a == 'p':

                # go up one
                return -1

            elif a == 'f':
                stdout.write(self.nextline[i] + ' ')

            # let me see the whole thing (next)
            elif a == 'n':
                out = ' '.join(self.nextline[i:])
                stdout.write(out)
                a = getch()
                if a == 'q':
                    exit(0)
                elif a == 'a':
                    return 0
                elif a == 'p':
                    return 0
                # got it right, dont repeat
                return 1
                break

            # quit
            # probably a more elegant way to do this
            elif a == 'q':
                exit(0)
            
            # go back to beginning of line
            elif a == 'a':
                return 0
            i += 1
        
        # if code reaches here, the prompt is at the end of the current line.
        # So, the functionality here may be a bit different than when in the middle of the line.
        
        # if f is pressed once more, don't go on to the next line
        a = getch()
        while a.lower() not in 'anq':
            a = getch()
            if a == 'n':
                return 1
            elif a == 'a':
                return 0
                
            # not really a quit here, but two q's in a row are intuitive
            elif a == 'q':
                return 0
        # Have to make sure we never return NULL (can't do arithmetic with it)
        # Returning 0 just repeats the ask()
        return 0



if __name__ == "__main__":
    # If no file is passed, ask for it
    if len(argv) == 2:
        filename = argv[1]
    else:
        filename = ''
        # INPUT = stdin.read()
        # print INPUT
            
    g = get_poem_line_list(filename)
    p = PoemRunner(g)
        


