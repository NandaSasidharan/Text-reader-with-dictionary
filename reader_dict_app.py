import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import Menu
from tkinter import filedialog as fd # to open file from menu
import json


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.text = None
        self.my_dict = None
        self.filepath = None
        self.definition = None
        self.story = None
        self.scrollbar = None
        self.label = None
        self.entry = None
        self.master = master
        self.grid()
        self.load_dictionary()
        self.create_widgets()

    def select_file(self):
        filetypes = (('text files', '*.txt'),('All files', '*.*'))
        self.filepath = fd.askopenfilename(title='Open a file', initialdir='./', filetypes=filetypes)
        

    def load_dictionary(self):
        with open("dictionary/kaikki_formatted.json", 'r', encoding='utf8') as file:
            self.my_dict = json.load(file)

    def load_file(self):
        if self.filepath:        
            try:
                with open(self.filepath, 'r') as file:
                    # Read the file contents into a string
                    self.text = file.read()
            except:
                with open(self.filepath, 'r', encoding='utf8') as file:
                    # Read the file contents into a string
                    self.text = file.read()
            

    def create_widgets(self):
        # Create a custom font
        custom_font = tkFont.Font(family="Times", size=20)
        # Create a Text widget to display story
        self.story = tk.Text(self, width=70, height=20, wrap='word', bg='#bdc1a2', fg='black', padx=50, pady=50,
                             font=custom_font)
        self.story.insert("end", "Load text file to read.")
        self.story.grid(row=0, column=0, columnspan=2, sticky=tk.EW, padx=5, pady=5)

        # create a scrollbar widget and set its command to the text widget
        self.scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.story.yview)
        self.scrollbar.grid(row=0, column=2, sticky=tk.NS)
        #  communicate back to the scrollbar
        self.story['yscrollcommand'] = self.scrollbar.set

        # Create a Text widget to display definition of words
        self.definition = tk.Text(self, width=70, height=7, wrap='word', bg='#b1c0a2', fg='gray', padx=50, pady=0,
                                  font=custom_font)
        self.definition.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        # Create a label saying how to search for meaning
        self.label = ttk.Label(self, text='Click at the word beginning or search here:', font=custom_font,
                               foreground='gray', anchor=tk.W)
        self.label.grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        # Create an Entry widget for user input
        self.entry = tk.Entry(self, font=custom_font)
        self.entry.grid(row=1, column=1, sticky=tk.W,  padx=5, pady=5)
        # Bind the Return key to the show_definition method
        self.entry.bind('<Return>', self.show_definition_from_entry)


    def display_story(self):
        self.select_file()
        self.load_file()
        if self.text: # self.txt is None, if select_file or load_file fails.
        # Add story to the widget with clickable words. Add newlines after paragraphs and add page number after 16 lines
            self.story.delete('1.0', tk.END)
            paragraphs = self.text.split('\n\n')
            line_count = 0
            page_count = 0
            for para in paragraphs:
                lines = para.split('\n')
                for line in lines:
                    words = line.split()
                    self.insert_clickable(words, self.story)
                    self.story.insert("end", "\n ")
                    line_count += 1
                    if line_count % 16 == 0:
                        page_count += 1
                        self.story.insert("end", "\n\n ---- page %d ---- \n\n" % page_count)
                self.story.insert("end", "\n ")  # new line for paragraph ends

    def insert_clickable(self, words, widget):
        # add tag 'clickable' to every word. When clicked, call the function show_definition_from_click()
        for i, word in enumerate(words):
            widget.insert("end", word + " ", "clickable")
            widget.tag_configure("clickable", foreground="black", underline=False)
            widget.tag_bind("clickable", "<Button-1>",
                            lambda event, arg=widget: self.show_definition_from_click(event, arg))

    def show_definition_from_click(self, event, widget):
        word = widget.get(tk.CURRENT, f"{tk.CURRENT} wordend").strip()
        self.show_definition(word)

    def show_definition_from_entry(self, event):
        word = self.entry.get().strip()
        self.show_definition(word)

    def show_definition(self, word, clear=True):
        if clear:
            self.definition.delete('1.0', tk.END)
        definition_label = f"Meaning of '{word}': \n"
        self.definition.insert("end", definition_label)
        if word in self.my_dict.keys():
            definition = self.my_dict[word]
            self.insert_clickable(definition, self.definition)
            level2_word = self.level2_definition_word(definition)
            if level2_word and level2_word!=word: # check if level2word is None and if it is same as word (leads to endless recursion)
                self.show_definition(level2_word, clear=False)
        else:
            self.definition.insert("end", "No definition found.")

    def level2_definition_word(self, definition):
        ''' sometimes the definition only shows that the word is a grammatical variation 
        of another base word. This function helps to isolate this base word.'''
        level2_indicators = ['inflection', 'participle', 'preterite', 'imperative', 'plural', 'singular', 'spelling', 'equivalent', 'degree', 'genitive']
        for indicator in level2_indicators:
            for sentence in definition[1:]:
                words = sentence.split()
                if indicator in words:
                    indicator_index = words.index(indicator)
                    if indicator_index < len(words) - 2:
                        word = words[indicator_index + 2]
                        word = word.replace(':', '')
                        return word
   


root = tk.Tk()
root.title('Book reader with dictionary')
root.configure(bg='gray')
# Set a custom font for the entire application
root.option_add('*Font', (14)) # add font size


app = Application(master=root)
# create a menubar
menubar = Menu(root)
root.config(menu=menubar)
# create a menu
file_menu = Menu(menubar, tearoff=False)
# add menu items to the File menu
file_menu.add_command(label='Open', command=app.display_story)
# add the File menu to the menubar
menubar.add_cascade(label="File",menu=file_menu)


try:
    from ctypes import windll

    # to improve the display resolution in MS Windows
    windll.shcore.SetProcessDpiAwareness(1)
finally:
    app.mainloop()
