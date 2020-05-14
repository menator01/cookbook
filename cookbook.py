# /usr/bin/env python3.8

###### Do the imports ######
import tkinter as tk
from tkinter import ttk, messagebox
import string
from functools import partial
import webbrowser
from  modules import database as db, time_converter as tc, settings
import threading
from playsound import playsound



### Check if Recipe.db exists ###
db.Database().check_for_database()

def opensite():
    '''Docstring'''
    threading.Thread(target=playsound, args=(settings.LNK,)).start()
    webbrowser.open_new('http://recipes.phpshelf.net')

###### Intiate the window ######
class RootWindow:
    '''Docstring'''
    def __init__(self, master):
        self.master = master
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        ###### Intiate all of our main containerframes ######
        self.logo_frame()
        self.letter_frame()
        self.container_frame()
        self.title_frame()
        self.recipe_frame()
        self.footer_frame()

        ###### Initate the widgets ######
        Child(self.logoframe, self.footerframe, self.titleframe, self.recipeframe)
        Child2().lettermenu(self.letterframe, self.titleframe, self.recipeframe)
        Child3().titlemenu(self.titleframe, self.recipeframe)
        Child4().recipe(self.recipeframe)

    ###### This sets all the container frames ######
    ###### Need to create a class for generic ######
    ###### frames to eliminate repetitive code #####
    def logo_frame(self):
        '''logo frame'''
        self.logoframe = ttk.Frame(self.master, border=5, relief='ridge')
        self.logoframe.grid(column=0, row=0, sticky='new')
        self.logoframe.grid_columnconfigure(0, weight=3)

    def letter_frame(self):
        '''letterframe'''
        self.letterframe = ttk.Frame(self.master, border=5, relief='ridge')
        self.letterframe.grid(column=0, row=1, sticky='new')
        for i in range(26):
            self.letterframe.grid_columnconfigure(i, weight=3)

    def container_frame(self):
        '''Container frame will hold two frames. Title frame and recipe frame'''
        self.containerframe = ttk.Frame(self.master)
        self.containerframe.grid(column=0, row=2, sticky='nw')
        self.containerframe.grid_columnconfigure(0, weight=3)

    def title_frame(self):
        '''Title Frame'''
        style = ttk.Style()
        style.configure('Title.TLabel', background='gray86')
        self.titleframe = ttk.Frame(self.containerframe, style='Title.TLabel', \
        border=5, relief='ridge')
        self.titleframe.grid(column=0, row=0, sticky='nw')
        self.titleframe.grid_columnconfigure(0, weight=3)

    def recipe_frame(self):
        '''Recipe Frame'''
        self.recipeframe = ttk.Frame(self.containerframe, border=5, relief='ridge')
        self.recipeframe.grid(column=1, row=0, sticky='new')
        self.recipeframe.grid_columnconfigure(0, weight=3)

    def footer_frame(self):
        '''footer'''
        self.footerframe = ttk.Frame(self.master, border=5, relief='ridge')
        self.footerframe.grid(column=0, row=3, sticky='new')
        self.footerframe.grid_columnconfigure(0, weight=3)

###### This class defines and displays header and footer ######
class Child:
    '''logo'''
    def __init__(self, logoframe, footerframe, titleframe, recipeframe):
        self.my_logo(logoframe)
        self.my_footer(footerframe, titleframe, recipeframe)

    def my_logo(self, logoframe):
        '''doc'''
        imgfile = tk.PhotoImage(file=settings.IMG)
        self.logo = ttk.Label(logoframe, image=imgfile)
        self.logo.image = imgfile
        self.logo.grid(column=0, row=0)

    def my_footer(self, footerframe, titleframe, recipeframe):
        '''footer'''
        style = ttk.Style()
        style.map('Footer.TLabel', \
        foreground=[('pressed', 'firebrick'), ('active', 'red')], \
        background=[('pressed', '!disabled', 'gray86'), ('active', 'gray86')] \
        )
        style.configure('Footer.TLabel', foreground='blue', \
        font=('Times', 12, 'normal', 'underline'))
        footer = ttk.Button(footerframe, text='Register for Johnny\'s CookBook', \
        style='Footer.TLabel', cursor='hand2', command=partial(opensite))
        footer.grid(column=0, row=0, ipady=3, padx=10, sticky='nw')

        new_window = AddRecipe(titleframe, recipeframe).my_form
        form = ttk.Button(footerframe, text='Add Recipe', style='Footer.TLabel', cursor='hand2', \
        command=partial(new_window))
        form.grid(column=1, row=0, padx=10)


###### Class produces the letter menu ######
class Child2:
    '''doc'''
    def __init__(self):
        pass

    def lettermenu(self, letterframe, titleframe, recipeframe):
        '''lettermenu'''
        letters = string.ascii_uppercase
        i = 0
        style = ttk.Style()
        style.configure('Btn.TButton', width=3)
        for letter in letters:
            button = ttk.Button(letterframe, text=letter, style='Btn.TButton', \
            command=partial(Child3().titlemenu, titleframe, recipeframe, letter=letter))
            button.grid(column=i, row=0, sticky='new')
            i += 1


###### This class retrieves and displays recipe titles ######
class Child3:
    '''doc'''
    def __init__(self):
        pass

    def titlemenu(self, titleframe, recipeframe, letter=db.Database().first_recipe()[0]):
        '''title menu'''

        ###### Query the database for recipe titles from our letter menu defaults to a ######
        threading.Thread(target=playsound, args=(settings.BTN,)).start()
        data = db.Database().title_query(letter=letter)

        ###### Create the canvas and scrollbar ######
        canvas = tk.Canvas(titleframe, highlightcolor='gray87')
        scrollbar = ttk.Scrollbar(titleframe, orient='vertical', command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        ###### If there are not any results returned, display message ######
        if not data:
            threading.Thread(target=playsound, args=(settings.ALERT,)).start()
            msg = messagebox.showerror(title='No listing', \
            message='Sorry, there have not been any recipes added starting with ' + letter)
            if msg == 'ok':
                return True
        else:
            ###### Setup our look for the recipe menu ######
            style = ttk.Style()
            style.map('L.TLabel', \
            background=[('pressed', '!disabled', 'gray87'), ('active', '#ffffee')], \
            foreground=[('pressed', 'red'), ('active', 'red')])

            style.configure('L.TLabel', relief='flat', padding=2, foreground='blue')

            ###### Loop through and display the return results from the database ######

            for recipe_id, title in data:
                title = ttk.Button(scrollable_frame, text=title.title(), \
                style='L.TLabel', cursor='hand2', \
                command=partial(Child4().recipe, recipeframe, recipe_id=recipe_id))
                title.grid(column=0, row=recipe_id, sticky='nw')

            scrollbar.grid(column=0, row=0, sticky='nsw')
            canvas.grid(column=1, row=0, sticky='nsw', padx=8)


class Child4:
    '''Docstring'''
    def __init__(self):
        pass

    def recipe(self, recipeframe, recipe_id=db.Database().first_recipe()[1]):
        '''Docstring'''

        threading.Thread(target=playsound, args=(settings.LNK,)).start()

        data = db.Database().id_query(recipe_id)

        canvas = tk.Canvas(recipeframe, width=600)
        canvas.configure(border=5, highlightcolor='gray87')

        scrollbar = ttk.Scrollbar(recipeframe, orient='vertical', command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        style = ttk.Style()
        ### Title
        style.configure('Title.TLabel', \
        font=('Sans', 12, 'bold', 'underline'), \
        foreground='blue4', padding=5, relief='raised')
        title = ttk.Label(scrollable_frame, text=f'{data[1].title()}', \
        style='Title.TLabel', width=54)
        title.grid(columnspan=2, column=0, row=0, sticky='new')

        style2 = ttk.Style()
        style2.configure('Time.TLabel', \
        foreground='blue3', relief='raised', padding=5)

        times = ttk.Label(scrollable_frame, \
        text=f' Prep Time: {tc.time_converter(data[4])}  \
        Cook Time: {tc.time_converter(data[5])} \
         Total Time: {tc.time_converter((data[4]+data[5]))}', style='Time.TLabel')
        times.grid(columnspan=2, column=0, row=1, sticky='new')

        ### Mini Headers for ingredients and instructions
        style3 = ttk.Style()
        style3.configure('MiniHeader.TLabel', \
        font=('Sans', 10, 'bold', 'underline', \
        'italic'), foreground='blue4', relief='raised', padding=5)

        mini_header1 = ttk.Label(scrollable_frame, \
        text=' Ingredients', style='MiniHeader.TLabel')
        mini_header1.grid(column=0, row=2, sticky='new')

        mini_header2 = ttk.Label(scrollable_frame, \
        text=' Instructions', style='MiniHeader.TLabel')
        mini_header2.grid(column=1, row=2, sticky='new')

        style4 = ttk.Style()
        style4.configure('Recipe.TLabel', \
        padding=8, border=8, relief='flat', wraplength=291)

        ingredients = ttk.Label(scrollable_frame, \
        text=data[2].title(), style='Recipe.TLabel')
        ingredients.grid(column=0, row=3, sticky='nw')

        instructions = ttk.Label(scrollable_frame, \
        text=data[3].title(), style='Recipe.TLabel')
        instructions.grid(column=1, row=3, sticky='nw')

        scrollbar.grid(column=0, row=0, sticky='nsw')
        canvas.grid(column=1, row=0, sticky='nsw')

class AddRecipe:
    '''doc'''
    def __init__(self, titleframe, recipeframe):
        self.titleframe = titleframe
        self.recipeframe = recipeframe

    def my_form(self):
        '''docstring'''
        threading.Thread(target=playsound, args=(settings.WINDOW_OPEN,)).start()
        self.top = tk.Toplevel()
        self.top.configure(border=8, relief='ridge')
        self.top.resizable(width=False, height=False)
        self.top.title('Add a Recipe')
        frame = tk.Frame(self.top)
        frame.grid(column=0, row=0, padx=25, pady=25, sticky='new')

        header_style = ttk.Style()
        header_style.configure('Header.TLabel', font=('Sans', 18, 'bold'), padding=0)
        header = ttk.Label(frame, text='Add a Recipe', style='Header.TLabel')
        header.grid(columnspan=2, column=0, row=0)

        title_frame = ttk.Frame(frame, border=5, relief='ridge', padding=8)
        title_frame.grid(columnspan=2, column=0, row=1, ipadx=2)

        title = ttk.Label(title_frame, text='Title:')
        title.grid(column=0, row=0, sticky='nw')
        title_entry = tk.Entry(title_frame, width=100)
        title_entry.grid(column=0, row=1)

        ingredients_frame = ttk.Frame(frame, border=5, relief='ridge', padding=8)
        ingredients_frame.grid(column=0, row=2, sticky='nw')

        ingredients = ttk.Label(ingredients_frame, text='Ingredients:')
        ingredients.grid(columnspan=2, column=0, row=0, sticky='nw')
        ingredients_entry = tk.Text(ingredients_frame, width=46, height=20)

        ingr_scrollbar = tk.Scrollbar(ingredients_frame)
        ingr_scrollbar.configure(command=ingredients_entry.yview)
        ingr_scrollbar.grid(column=0, row=1, sticky='ns')

        ingredients_entry.grid(column=1, row=1, sticky='nw')

        instruction_frame = ttk.Frame(frame, border=5, relief='ridge', padding=8)
        instruction_frame.grid(column=1, row=2, sticky='nw')

        instructions = ttk.Label(instruction_frame, text='Instructions:')
        instructions.grid(columnspan=2, column=0, row=0, sticky='nw')
        instructions_entry = tk.Text(instruction_frame, width=47, height=20)

        instr_scrollbar = tk.Scrollbar(instruction_frame)
        instr_scrollbar.configure(command=instructions_entry.yview)
        instr_scrollbar.grid(column=0, row=1, sticky='ns')

        instructions_entry.grid(column=1, row=1, sticky='nw')

        # ### Bottom frame ###
        btm_frame_style = ttk.Style()
        btm_frame_style.configure('BFrame.TFrame')
        bottom_frame = ttk.Frame(frame, border=5, relief='ridge', padding=8, \
        style='BFrame.TFrame')
        bottom_frame.grid(columnspan=2, column=0, row=3, sticky='new')

        prep = tk.Label(bottom_frame, text='Prep. Time in min.')
        prep.grid(column=0, row=0, sticky='w', padx=10)
        prep_time = tk.Spinbox(bottom_frame, from_=0, to=320, width=5)
        prep_time.grid(column=1, row=0, sticky='w')

        cook = ttk.Label(bottom_frame, text='Cook Time in min.')
        cook.grid(column=2, row=0, padx=10)
        cook_time = tk.Spinbox(bottom_frame, from_=0, to=320, width=5)
        cook_time.grid(column=3, row=0)

        spacer = ttk.Frame(bottom_frame, width=300)
        spacer.grid(column=4, row=1)


        btn_style = ttk.Style()
        btn_style.configure('Submit.TButton')
        submit_btn = ttk.Button(bottom_frame, text='Submit Recipe', style='Submit.TButton', \
        command=partial(self.submit_values, title_entry, ingredients_entry, \
        instructions_entry, prep_time, cook_time))
        submit_btn.grid(column=5, row=0)

    def submit_values(self, title, ingredients, instructions, prep_time, cook_time):
        '''Docstring'''
        if not title.get() or not ingredients.get('1.0', 'end-1c') or not \
        instructions.get('1.0', 'end-1c'):
            threading.Thread(target=playsound, args=(settings.ALERT,)).start()
            messagebox.showerror(title='Input Error', \
            message='Required fields: Title, Ingredients, and Instructions')
        else:
            title = title.get()
            ingredients = ingredients.get('1.0', 'end-1c')
            instructions = instructions.get('1.0', 'end-1c')
            prep_time = prep_time.get()
            cook_time = cook_time.get()

            q = db.Database().enter_recipe(title, ingredients, instructions, prep_time, cook_time)

            threading.Thread(target=playsound, args=(settings.BTN,)).start()
            msg = messagebox.askyesno(title='Add Recipe', message='Add another recipe?')
            if msg is True:
                threading.Thread(target=playsound, args=(settings.WINDOW_OPEN,)).start()
                self.top.destroy()
                self.my_form()
            if msg is False:
                threading.Thread(target=playsound, args=(settings.WINDOW_CLOSE,)).start()
                self.top.destroy()
                first_letter = title[0]
                Child3().titlemenu(self.titleframe, self.recipeframe, letter=first_letter)
                Child4().recipe(self.recipeframe, recipe_id=q)





def main():
    '''Docstring'''
    root = tk.Tk()
    root.title('Johnny\'s CookBook')
    img = tk.PhotoImage(file=settings.IMG)
    root.configure(width=img.width())
    root.resizable(width=False, height=False)
    root.iconphoto(True, tk.PhotoImage(file=settings.ICOIMG))
    RootWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()
