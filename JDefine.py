#Version 1.0, 1.28.2023

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import urllib.request
from bs4 import BeautifulSoup
import re

class JDefine():
    #Create variables and sequences that can be passed among the methods
    def __init__(self):
        self.wordlist = []
        self.notfound = []
        self.alreadyfound = set()
        self.currentword = None
        self.inputflag = 0
        self.outputflag = 0

    #Retrieve a list of words from a user-designated text file
    def input_file(self):
        filename = filedialog.askopenfilename(initialdir= \
        r"C:\Users", title="Select Input File", filetypes=((\
        "Text File", "*.txt"), ("All Files", "*.*")))
        
        #Reset wordlist if new text file is loaded
        if self.inputflag == 1:
            self.wordlist = []

        #Load words from file     
        try:
            if filename:              
                with open(filename, "r", encoding="utf-8") as file:                  
                    for line in file:
                        line = line.strip()
                        line = line.encode("utf-8")
                        if len(line) == 0: continue
                        self.wordlist.append(line)
                    self.inputflag = 1

            #If Cancel or X clicked, exit program gracefully
            else:
                SystemExit()
        except:
            messagebox.showerror("File Error", "Couldn't read the file. " \
            "Please make sure your file is formatted correctly.")

    #Have user designate file for saving definitions
    def output_file(self):

        #Make sure input file has been selected first
        if self.inputflag != 1:
            messagebox.showerror("File Error", "You must select an input "\
            "file before designating an output file.")
            SystemExit()
            return
        try:
            self.savename = filedialog.asksaveasfilename(title="Save Output" \
            " As", filetypes=(("Text File", "*.txt"), ("All Files", "*.*")),
            defaultextension = ".txt")
            if self.savename:
                self.outputflag = 1
                return self.savename
            else:
                messagebox.showerror("File Error", "Invalid file name. " \
                "Please enter a valid file name.")                      
                SystemExit()

        except:
            messagebox.showerror("File Error", "Invalid file name. " \
            "Please enter a valid file name.")            
            SystemExit()

    #Progress bar window
    def openwindow(self):
        self.top = Toplevel()
        self.progress_label = Label(self.top, text="")
        self.progress_label.pack()
        self.top.title("Retrieving Definitions...")
        self.top.geometry("300x100")

        self.progress = ttk.Progressbar(self.top, orient=HORIZONTAL, \
        maximum=len(self.wordlist), length=300, mode="determinate")
        self.progress.pack(pady=10)

    #Fill progress bar and format text displayed above bar
    def step(self):
        for _ in self.wordlist:
            self.top.update()
            self.progress_label.config\
            (text=str(round(self.progress["value"]))
            + "/" + str(len(self.wordlist)) + " words")
            self.progress["value"] += float(1/len(self.wordlist))

    #Look up words using the "weblio" dictionary (https://www.weblio.jp/)
    def weblio(self):

        #Ensure output file has been designated before performing lookup
        if self.outputflag != 1:
            messagebox.showerror("File Error", "You must designate an output"\
            " file before you can begin looking up definitions.")
            return
        
        #Create progress bar
        self.openwindow()

        with open(self.savename, "a", encoding="utf-8") as output:
            for word in self.wordlist:
                self.step()
                slice = (str(word)[2:])
                conversion = slice.replace("\\x", "%").replace("\'", "")

                #Complete URL
                url = "https://www.weblio.jp/content/" + conversion

                try:
                    #Read html and use BeautifulSoup to parse
                    html = urllib.request.urlopen(url)
                    soup = BeautifulSoup(html, "html.parser")

                    #Different words have different html doc formats,
                    #so different search patterns are needed to extract them.
                    #Start with most general pattern and narrow down

                    try: #Pattern 1 (should find most kanji compounds)

                        #Narrow search to html tag containing definitions
                        ptags = soup.find_all("p")

                        #Use regex to extract and format definitions
                        definition = re.findall("<p>[\s\S]*?<b>([\s\S]*?)" \
                        "</b>([\s\S]*?)</p>", str(ptags))

                        for item in definition:

                            #Matches almost always have initial element of
                            #len 1; throw exception for non-matches and
                            #proceed to Pattern 2. Use "alreadyfound" set
                            #to avoid false positives and continue extraction

                            if len(item[0]) != 1 and word not in \
                            self.alreadyfound:
                                raise Exception()
                            
                            #Hone in on definition portion of data
                            if len(item[0]) == 1 and len(item[1]) != 0 and \
                            item[1].startswith("（") == False:

                                #Determine which output format to use.
                                #First occurrence of word prints word
                                #followed by tab (for tab-delimited format)                        
                                if self.currentword == None:
                                    self.currentword = word.decode()
                                    self.alreadyfound.add(word)
                                    output.write("\n\n" + word.decode() + \
                                    "\t" + re.sub("<a[\s\S]*?>|</a>|<span " \
                                    "class[\s\S]*?</span>|<b>|</b>", "", \
                                    item[1]))

                                #For words with multiple definitions,
                                #separate them using vertical bars (|)
                                elif self.currentword == word.decode():
                                    self.alreadyfound.add(word)
                                    output.write("　　|　　" + re.sub("<a" \
                                    "[\s\S]*?>|</a>|<span class[\s\S]*?" \
                                    "</span>|<b>|</b>", "", item[1]))
                                
                                #When switching to a new word, add line breaks
                                #and repeat process
                                else:
                                    self.currentword = word.decode()
                                    self.alreadyfound.add(word)
                                    output.write("\n\n" + word.decode() + \
                                    "\t" + re.sub("<a[\s\S]*?>|</a>|<span " \
                                    "class[\s\S]*?</span>|<b>|</b>", "", \
                                    item[1]))

                    except: 
                        try: #Pattern 2
                            definition = re.findall("<p style[\s\S]*?</p>" \
                            "[\s\S]*?<p>([\s\S]*?)</p>", str(ptags))

                            if len(definition) == 0:
                                raise Exception()   

                            for item in definition:
                                if "<br/>" not in item:
                                    if self.currentword == None:
                                        self.currentword = word.decode()
                                        output.write("\n\n" + word.decode() +\
                                        "\t" + re.sub("<a[\s\S]*?>|</a>|" \
                                        "span class[\s\S]*?</span>|<b>|</b>"\
                                        "", "", item))

                                    elif self.currentword == word.decode():                   
                                        output.write("　　|　　" + re.sub(\
                                        "<a[\s\S]*?>|</a>|<span class[\s\S]"\
                                        "*?</span>|<b>|</b>", "", item))
                                    else:
                                        self.currentword = word.decode()
                                        output.write("\n\n" + word.decode() +\
                                        "\t" + re.sub("<a[\s\S]*?>|</a>|" \
                                        "<span class[\s\S]*?</span>|<b>|</b>"\
                                        "", "", item))

                        except:
                            try: #Pattern 3
                                definition = re.findall("<p>[\s\S]*?《[\s\S]"\
                                "*?([\s\S]*?)</p>", str(ptags))

                                if len(definition) == 0:
                                    raise Exception()                           

                                for item in definition:
                                    if self.currentword == None:
                                        self.currentword = word.decode()                            
                                        output.write("\n\n" + word.decode() \
                                        + "\t" + re.sub("<a[\s\S]*?>|</a>|" \
                                        "<span class[\s\S]*?</span>|<b>|</b>"\
                                        , "", item))
                                    
                                    elif self.currentword == word.decode():
                                        output.write("　　|　　" + re.sub(\
                                        "<a[\s\S]*?>|</a>|<span class[\s\S]" \
                                        "*?</span>|<b>|</b>", "", item))

                                    else:
                                        self.currentword = word.decode()
                                        output.write("\n\n" + word.decode() \
                                        + "\t" + re.sub("<a[\s\S]*?>|</a>|" \
                                        "<span class[\s\S]*?</span>|<b>|</b>"\
                                        , "", item))

                            except:
                                try: #Pattern 4
                                    dtags = soup.find_all("div")
                                    
                                    definition = re.findall("<br class=" \
                                    "\"AM\"/>[\s\S]*?>([\s\S]*?)</div>", \
                                     str(dtags))

                                    if len(definition) == 0:
                                        raise Exception()   

                                    output.write("\n\n" + word.decode() + \
                                    "\t" + re.sub("<a[\s\S]*?>|</a>|" \
                                    "<span class[\s\S]*?</span>|<b>|</b>|" \
                                    "<br/>|<h3[\s\S]*?\">|<h4[\s\S]*?\">|" \
                                    "</h3>|</h4>|<br class=[\s\S]*?clr\"/>",\
                                     "", definition[0]))
                                
                                except:        
                                    try: #Pattern 5
                                        definition = re.findall("<span" \
                                        " class=\"hinshi\">[\s\S]*?</span>" \
                                        "([\s\S]*?)</p>", str(dtags))

                                        if len(definition) == 0:
                                            raise Exception()      

                                        output.write("\n\n" + word.decode() \
                                        + "\t" + re.sub("<a[\s\S]*?>|</a>|" \
                                        "<span class[\s\S]*?</span>|<b>|</b>"\
                                        , "", definition[0]))
                                    
                                    except:
                                        #If word not found, add to 
                                        #notfound list
                                        self.notfound.append(word)

                #For invalid URLs
                except:
                    self.notfound.append(word)

            #Let user know which words weren't found in dictionary
            for word in self.notfound:
                output.write("\n\n" + "Unable to find: " + word.decode())

       #Get rid of progress bar window
        self.top.destroy()

        #Clear the wordlists for subsequent searches
        self.wordlist = []
        self.notfound = []
        self.alreadyfound = set()

        #Notify user that search is done
        messagebox.showinfo("Done!", "Definitions extracted!")