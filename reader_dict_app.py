import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import json


class Application(tk.Frame):
    def __init__(self, filepath, master=None):
        super().__init__(master)
        self.text = None
        self.my_dict = None
        self.filepath = filepath
        self.definition = None
        self.story = None
        self.entry = None
        self.master = master
        self.pack()
        self.load_data()
        self.create_widgets()

    def load_data(self):
        with open("dictionary/kaikki_formatted.json", 'r', encoding='utf8') as file:
            self.my_dict = json.load(file)
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
        self.story.pack(side=tk.TOP, expand=True, fill=tk.BOTH, padx=5, pady=5)

        # Create a Text widget to display definition of words
        self.definition = tk.Text(self, width=70, height=7, wrap='word', bg='#b1c0a2', fg='gray', padx=50, pady=0,
                                  font=custom_font)
        self.definition.pack(side=tk.BOTTOM, expand=False, fill=tk.BOTH, padx=5, pady=5)
        # Create an Entry widget for user input
        self.entry = tk.Entry(self, font=custom_font)
        self.entry.pack(side=tk.BOTTOM, expand=False, fill=tk.BOTH, padx=5, pady=5)
        # Bind the Return key to the show_definition method
        self.entry.bind('<Return>', self.show_definition_from_entry)

        # Add story to the widget with clickable words. Add newlines after paragraphs and add page number after 16 lines
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

    def show_definition(self, word):
        self.definition.delete('1.0', tk.END)
        definition_label = f"Meaning of '{word}': \n"
        self.definition.insert("end", definition_label)
        if word in self.my_dict.keys():
            definition = self.my_dict[word]
            self.insert_clickable(definition, self.definition)
        else:
            self.definition.insert("end", "No definition found.")


root = tk.Tk()
root.title('Book reader with dictionary')
root.configure(bg='gray')

file_path = 'books/Josefine Mutzenbacher.txt'
app = Application(file_path, master=root)
try:
    from ctypes import windll

    # to improve the display resolution in MS Windows
    windll.shcore.SetProcessDpiAwareness(1)
finally:
    app.mainloop()
