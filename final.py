import tkinter as tk
from tkinter import filedialog
from tkinter import colorchooser
import PyPDF2
from tkinter import font
from tkinter import simpledialog
import ttkbootstrap as tb
from ttkbootstrap.dialogs.dialogs import FontDialog
from ttkbootstrap.constants import*
import type_classifier
import Search_and_Replace as sar
import save
import Notebook
import file_inp
import WCMeter
import opening
#Welcome Screen
splash_root = tk.Tk()
splash_root.title("Welcome Window")
splash_root.geometry('1920x1080')
bg = tk.PhotoImage(file='bg_2.png')
splash_label = tk.Label(splash_root, image = bg)
splash_label.pack()
def main_window():
    splash_root.destroy()
    window=tb.Window(themename='cyborg')
    window.title("Text Editor")
    window.geometry('1920x1080')
    #scrollbar
    scrollbar=tb.Scrollbar(window, bootstyle='info-round') #Y-Axis Scrollbar
    xscrollbar=tb.Scrollbar(window, orient='horizontal', bootstyle='info-round') #X-Axis Scrollbar
    xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_area=tk.Text(window,wrap=tk.WORD, undo=True, yscrollcommand=scrollbar.set, xscrollcommand=xscrollbar.set,font=("Arial"))#wrap-to wrap text around widget
    scrollbar.config(command=text_area.yview)
    xscrollbar.config(command=text_area.xview)
    text_area.pack(expand=tk.YES, fill=tk.BOTH,pady=40)#expand-adjusts to window size change, fill-fills entire screen w/ widget(BOTH-x and y axis fill)
    text_area.insert(tk.END,"")#inserts text from file END-inserts text at the point where cursor was last
    #----------------------------------------------------------
    def pdf_inp(file):
        f=open(file,'rb')
        pdf_data=[]
        pdf_reader=PyPDF2.PdfReader(f)
        for p in range(len(pdf_reader.pages)):
            page=pdf_reader.pages[p]
            pdf_data.append(page.extract_text())
        text_area.insert(tk.END,"\n\n".join(pdf_data))
    #----------------------------------- 
    def openfile():
        file=opening.opening()
        text_area.delete(1.0, tk.END)
        if '.txt' in file:
            file_inp.file_inp(file,text_area)
        elif '.pdf' in file:
            pdf_inp(file)
    #------------------------------------------------------------
    def saveasfile():
        file=save.saving()
        if '.txt' in file:
            wf=open(file,'w')
            data=text_area.get(1.0,tk.END)
            wf.write(data)
            wf.close()
        else:
            pass
    #--------------------------------------------------------------
    def refresh():
        text_area.delete(1.0, tk.END)
        opening.opened=False
        text_area.configure(background='black')
        text_area.configure(font=('Arial',12))
        lf=font.Font(weight="normal",slant="roman",underline=False,overstrike=False)
        text_area.configure(font=lf)
    #--------------------------------------------------------------
    def savefile():
        try:
            if opening.opened==True:
                if '.txt' in opening.textpath:
                    wf=open(opening.textpath,'w')
                    data=text_area.get(1.0,tk.END)
                    wf.write(data)
                    wf.close()
            else:
                saveasfile()
        except:
            pass    
    #-----------------------------------------
    def italic():
        italic_font=font.Font(text_area, text_area.cget('font'))
        italic_font.configure(slant='italic')
        try:
            text_area.tag_configure('bt2', font=italic_font)
            current_tags= text_area.tag_names("sel.first")
            if "bt2" in current_tags:
                text_area.tag_remove("bt2" , "sel.first" , "sel.last")
                if "colored" in current_tags:
                    text_area.tag_configure("colored", foreground=my_color[1]) 
                    text_area.tag_add("colored", "sel.first","sel.last")
                if "cfs" in current_tags:
                    italic_font.configure(size=my_font)
                if "bt" in current_tags:
                    italic_font.configure(weight='bold')
            else:
                text_area.tag_add("bt2" , "sel.first" , "sel.last")
                if "colored" in current_tags:
                    text_area.tag_configure("colored", foreground=my_color[1]) 
                    text_area.tag_add("colored", "sel.first","sel.last")
                if "cfs" in current_tags:
                    italic_font.configure(size=my_font)
                if "bt" in current_tags:
                    italic_font.configure(weight='bold')
        except:
            pass
    #----------------------------------------
    def bold():
        bold_font=font.Font(text_area, text_area.cget('font'))
        bold_font.configure(weight='bold')
        try:
            text_area.tag_configure('bt', font=bold_font)
            current_tags= text_area.tag_names("sel.first")
            if "bt" in current_tags:
                text_area.tag_remove("bt" , "sel.first" , "sel.last")
                if "colored" in current_tags:
                    text_area.tag_configure("colored", foreground=my_color[1]) 
                    text_area.tag_add("colored", "sel.first","sel.last")
                if "cfs" in current_tags:
                    bold_font.configure(size=my_font)
                if "bt2" in current_tags:
                    bold_font.configure(slant='italic')
            else:
                text_area.tag_add("bt" , "sel.first" , "sel.last")
                if "colored" in current_tags:
                    text_area.tag_configure("colored", foreground=my_color[1]) 
                    text_area.tag_add("colored", "sel.first","sel.last")
                if "cfs" in current_tags:
                    bold_font.configure(size=my_font)
                if "bt2" in current_tags:
                    bold_font.configure(slant='italic')
        except:
            pass
    #------------------------------------------------
    def cut_text():
        selected_text = text_area.get(tk.SEL_FIRST, tk.SEL_LAST)
        text_area.delete(tk.SEL_FIRST, tk.SEL_LAST)
        window.clipboard_clear() #Clears the previously copied text
        window.clipboard_append(selected_text) #Adds selected text to clipboard
    #---------------------------------------------------------------
    def copy_text():
        selected_text = text_area.get(tk.SEL_FIRST, tk.SEL_LAST)
        window.clipboard_clear()
        window.clipboard_append(selected_text)
    #------------------------------------------------
    def paste_text():
        text_to_paste = window.clipboard_get() #Returns the prevously copied/cut text
        text_area.insert(tk.INSERT, text_to_paste) 
    #------------------------------------------------
    def underline():
        try:
            if text_area.tag_nextrange('underline_selection', 'sel.first', 'sel.last') != ():
                text_area.tag_remove('underline_selection', 'sel.first', 'sel.last')
            else:
                text_area.tag_add('underline_selection', 'sel.first', 'sel.last')
                text_area.tag_configure('underline_selection', underline=True)
        except:
            pass
    #-------------------------
    def search_replace():
        global s
        global master
        global data
        data= text_area.get(1.0, tk.END)
        s=sar.SRBox() #creating an object s of the class SRBox from the module sar
        master=tk.Tk()
        s.display(master)
        tk.Button(master,text='OK',command=cont).grid(row=3, column=2, sticky=tk.W, pady=4)
        #-----------------------
    def cont():
        a,b=s.retrieve()
        master.destroy()
        new_data=data.replace(a,b)
        font=tk.font.Font(font=text_area['font'])
        style=font.actual()['family']
        stylew=font.actual()['weight']
        styles=font.actual()['slant']
        size=font.actual()['size']
        text_area.delete(1.0,tk.END)
        text_area.insert(tk.END,new_data)
        text_area.configure(font=(style,size), weight=stylew, slant=styles)
    #-----------------------
    def open_font():
        fd=FontDialog()
        fd.show() 
        text_area.configure(font=fd.result)
    #-------------------------
    def classifier():
        string1 = tk.simpledialog.askstring("Type Classifier", "Enter Sentence", parent = window)
        info = type_classifier.message(string1)
        msg = tk.messagebox.showinfo('Sentence Type Classifier', info)
    #-----------------------
    def text_color():
        global my_color
        my_color = colorchooser.askcolor()
        try:
            if my_color:
                text_area.tag_configure("colored", foreground=my_color[1]) 
                current_tags = text_area.tag_names("sel.first")
                text_area.tag_add("colored", "sel.first","sel.last")
                text_area.configure
        except:
            pass
    #-------------------------
    def bg_color():
        my_color = colorchooser.askcolor()
        if my_color:
            text_area.configure(bg=my_color[1])
    #-------------------------
    wc=WCMeter.WordCounter(window,text_area)
    wc.pack(side=tk.RIGHT)
    #-------------------------
    def justifyc():
        text_area.tag_configure("al", justify='center')
        text_area.tag_add("al",1.0,tk.END)
    #--------------------------
    def justifyl():
        text_area.tag_configure("al", justify='left')
        text_area.tag_add("al",1.0,tk.END)
    #---------------------------
    def justifyr():
        text_area.tag_configure("al", justify='right')
        text_area.tag_add("al",1.0,tk.END)
    #----------------------------------
    nb = Notebook.Tabs()
    nb.display(window)
    #------------------------------------
    menu = tk.Menu(window)
    window.config(menu=menu)
    filemenu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label='File',font=('Arial',16), menu=filemenu)
    filemenu.add_command(label='New',font=('Arial',16), command=refresh)
    filemenu.add_command(label='Open',font=('Arial',16), command=openfile)
    filemenu.add_command(label='Save',font=('Arial',16),command=savefile)
    filemenu.add_command(label='Save As...',font=('Arial',16), command=saveasfile)
    filemenu.add_separator()
    filemenu.add_command(label='Exit',font=('Arial',16), command=window.destroy)
    #-------------------------------------
    frame = tb.Frame(window,bootstyle='info',width=200,height=5)
    frame.place(x=0,y=0)
    font_s = tb.Button(frame,text='Font Master', bootstyle='dark',command=open_font)
    font_s.grid(row=0,column=0)
    italic = tb.Button(frame,text='Italicize', bootstyle='dark', command=italic)
    italic.grid(row=0,column=1)
    textc = tb.Button(frame,text='Text color',bootstyle='dark',command=text_color)
    textc.grid(row=0,column=2)
    bgc = tb.Button(frame,text='BG color',bootstyle='dark',command=bg_color)
    bgc.grid(row=0,column=3)
    bold = tb.Button(frame,text='Bold',bootstyle='dark',command=bold)
    bold.grid(row=0,column=4)
    underline = tb.Button(frame,text='Underline',bootstyle='dark',command=underline)
    underline.grid(row=0,column=5)
    spinbox = tk.Spinbox(frame, from_= 2, to=100, font=26, width=10, foreground='white', background='black', textvariable=tk.IntVar())
    spinbox.grid(row=0,column=6)
    my_font=16
    def changeFontSize():
       nonlocal my_font
       style=font.Font(text_area, text_area.cget('font'))
       try:
          text_area.tag_add("cfs", "sel.first", "sel.last")
          my_font=int(spinbox.get())
          text_area.tag_config("cfs", font = (style, my_font))
       except:
          pass
    button = tb.Button(frame, bootstyle='dark', text="OK", command=changeFontSize)
    button.grid(row=0,column=7)
    #-------------------------------------------
    editmenu = tk.Menu(menu, tearoff=0)#tearoff-remove dotted lines
    menu.add_cascade(label='Edit', menu=editmenu)
    editmenu.add_command(label='Cut',font=('Arial',16), command=cut_text, accelerator='Ctrl+X')
    editmenu.add_command(label='Copy',font=('Arial',16), command=copy_text, accelerator='Ctrl+C')
    editmenu.add_command(label='Paste',font=('Arial',16), command=paste_text, accelerator='Ctrl+V')
    editmenu.add_command(label='Undo',font=('Arial',16), command=text_area.edit_undo, accelerator='Ctrl+Z')
    editmenu.add_command(label='Redo',font=('Arial',16), command=text_area.edit_redo,accelerator='Ctrl+Shift+Z')
    alignmenu=tk.Menu(menu,tearoff=0)
    menu.add_cascade(label='Text Alignment',menu=alignmenu)
    alignmenu.add_command(label='Center',font=('Arial',16), command=justifyc)
    alignmenu.add_command(label='Left',font=('Arial',16), command=justifyl)
    alignmenu.add_command(label='Right',font=('Arial',16), command=justifyr)
    fontmenu=tk.Menu(menu, tearoff=0)
    sentmenu=tk.Menu(menu, tearoff=0)
    menu.add_cascade(label='Tools', menu=sentmenu)
    sentmenu.add_command(label='Sentence Type Classifier',font=('Arial',16), command=classifier)
    sentmenu.add_command(label='Find and Replace',font=('Arial',16), command=search_replace)
splash_root.after(3000,main_window)
tk.mainloop()

