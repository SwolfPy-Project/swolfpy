

import sys
from model import *
from tkinter import Frame, Tk, BOTH, Text, Menu, END
from tkinter import filedialog
from tkinter import ttk
from tkinter import simpledialog
from filehandler import *



try:
    from Tkinter import *
except ImportError:
    from tkinter import *

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

import basiclca_support

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = Tk()
    basiclca_support.set_Tk_var()
    top = New_Toplevel (root)
    basiclca_support.init(root, top)
    root.mainloop()

w = None
def create_New_Toplevel(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = Toplevel (root)
    basiclca_support.set_Tk_var()
    top = New_Toplevel (w)
    basiclca_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_New_Toplevel():
    global w
    w.destroy()
    w = None


class New_Toplevel:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85' 
        _ana2color = '#d9d9d9' # X11 color: 'gray85' 
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("857x715+525+112")
        top.title("LCA")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")



        self.Button1 = Button(top)
        self.Button1.place(relx=0.91, rely=0.951, height=24, width=49)
        self.Button1.configure(activebackground="#d9d9d9")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Update''')

        self.menubar = Menu(top,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)

        self.file = Menu(top,tearoff=0)
        self.menubar.add_cascade(menu=self.file,
                activebackground="#d9d9d9",
                activeforeground="#000000",
                background="#d9d9d9",
                font="TkMenuFont",
                foreground="#000000",
                label="File")
        self.file.add_command(
                activebackground="#d8d8d8",
                activeforeground="#000000",
                background="#d9d9d9",
                font="TkMenuFont",
                foreground="#000000",
                label="Open Model Files...",
				command=self.onOpenModelFile)
        self.file.add_command(
                activebackground="#d8d8d8",
                activeforeground="#000000",
                background="#d9d9d9",
                font="TkMenuFont",
                foreground="#000000",
                label="Open Model Description File...",
				command=self.onOpenModelDescriptionFile)
        self.file.add_command(
                activebackground="#d8d8d8",
                activeforeground="#000000",
                background="#d9d9d9",
                font="TkMenuFont",
                foreground="#000000",
                label="Exit")
        self.add = Menu(top,tearoff=0)
        self.menubar.add_cascade(menu=self.add,
                activebackground="#d9d9d9",
                activeforeground="#000000",
                background="#d9d9d9",
                font="TkMenuFont",
                foreground="#000000",
                label="Add")
        self.add.add_command(
                activebackground="#d8d8d8",
                activeforeground="#000000",
                background="#d9d9d9",
                font="TkMenuFont",
                foreground="#000000",
                label="Model",
				command=self.onAddModel)


        self.style.configure('TNotebook.Tab', background=_bgcolor)
        self.style.configure('TNotebook.Tab', foreground=_fgcolor)
        self.style.map('TNotebook.Tab', background=
            [('selected', _compcolor), ('active',_ana2color)])
        self.TNotebook1 = ttk.Notebook(top)
        self.TNotebook1.place(relx=0.035, rely=0.042, relheight=0.848
                , relwidth=0.915)
        self.TNotebook1.configure(width=784)
        self.TNotebook1.configure(takefocus="")
        self.TNotebook1_t0 = Frame(self.TNotebook1)
        self.TNotebook1.add(self.TNotebook1_t0, padding=3)
        self.TNotebook1.tab(0, text="Model 1",compound="left",underline="-1",)
        self.TNotebook1_t0.configure(background="#d9d9d9")
        self.TNotebook1_t0.configure(highlightbackground="#d9d9d9")
        self.TNotebook1_t0.configure(highlightcolor="black")
        self.notebook_index = 1


        self.Label10 = Label(self.TNotebook1_t0)
        self.Label10.place(relx=0.077, rely=0.103, height=21, width=54)
        self.Label10.configure(background="#d9d9d9")
        self.Label10.configure(disabledforeground="#a3a3a3")
        self.Label10.configure(foreground="#000000")
        self.Label10.configure(text='''Variable''')
        self.Label10.configure(width=120)

        self.Label11 = Label(self.TNotebook1_t0)
        self.Label11.place(relx=0.346, rely=0.103, height=21, width=35)
        self.Label11.configure(background="#d9d9d9")
        self.Label11.configure(disabledforeground="#a3a3a3")
        self.Label11.configure(foreground="#000000")
        self.Label11.configure(text='''Value''')

        self.Label12 = Label(self.TNotebook1_t0)
        self.Label12.place(relx=0.667, rely=0.103, height=21, width=28)
        self.Label12.configure(background="#d9d9d9")
        self.Label12.configure(disabledforeground="#a3a3a3")
        self.Label12.configure(foreground="#000000")
        self.Label12.configure(text='''Unit''')

        self.Label13 = Label(self.TNotebook1_t0)
        self.Label13.place(relx=0.09, rely=0.155, height=21, width=23)
        self.Label13.configure(background="#d9d9d9")
        self.Label13.configure(disabledforeground="#a3a3a3")
        self.Label13.configure(foreground="#000000")
        self.Label13.configure(text='''Var''')

        self.Spinbox3 = Spinbox(self.TNotebook1_t0, from_=1.0, to=100.0)
        self.Spinbox3.place(relx=0.301, rely=0.155, relheight=0.033
                , relwidth=0.173)
        self.Spinbox3.configure(activebackground="#f9f9f9")
        self.Spinbox3.configure(background="white")
        self.Spinbox3.configure(buttonbackground="#d9d9d9")
        self.Spinbox3.configure(disabledforeground="#a3a3a3")
        self.Spinbox3.configure(foreground="black")
        self.Spinbox3.configure(from_="1.0")
        self.Spinbox3.configure(highlightbackground="black")
        self.Spinbox3.configure(highlightcolor="black")
        self.Spinbox3.configure(insertbackground="black")
        self.Spinbox3.configure(selectbackground="#c4c4c4")
        self.Spinbox3.configure(selectforeground="black")
        self.Spinbox3.configure(textvariable=basiclca_support.spinbox)
        self.Spinbox3.configure(to="100.0")

        self.Label14 = Label(self.TNotebook1_t0)
        self.Label14.place(relx=0.667, rely=0.155, height=21, width=27)
        self.Label14.configure(background="#d9d9d9")
        self.Label14.configure(disabledforeground="#a3a3a3")
        self.Label14.configure(foreground="#000000")
        self.Label14.configure(text='''m/s''')

    def onAddModel(self):
        #application_window = ttk.Tk()
        answer = simpledialog.askstring("Input", "Type model name")

        self.TNotebook1_t1 = Frame(self.TNotebook1)
        self.TNotebook1.add(self.TNotebook1_t1, padding=3)
        if not answer:
            string = 'Model ' + str(self.notebook_index+1)
            self.TNotebook1.tab(self.notebook_index, text=string,compound="left",underline="-1",)
            self.TNotebook1_t1.configure(background="#d9d9d9")
            self.TNotebook1_t1.configure(highlightbackground="#d9d9d9")
            self.TNotebook1_t1.configure(highlightcolor="black")        
        else:
            self.TNotebook1.tab(self.notebook_index, text=answer,compound="left",underline="-1",)
            self.TNotebook1_t1.configure(background="#d9d9d9")
            self.TNotebook1_t1.configure(highlightbackground="#d9d9d9")
            self.TNotebook1_t1.configure(highlightcolor="black")
        self.notebook_index += 1
		
		
        self.Label10 = Label(self.TNotebook1_t1)
        self.Label10.place(relx=0.15, rely=0.103, height=21, width=100) #0.077
        self.Label10.configure(background="#d9d9d9")
        self.Label10.configure(disabledforeground="#a3a3a3")
        self.Label10.configure(foreground="#000000")
        self.Label10.configure(text='''Specify Model File''')
        self.Label10.configure(width=300)
		
        self.TCombobox1 = ttk.Combobox(self.TNotebook1_t1, postcommand = self.updateFilesCbox)
        self.TCombobox1.place(relx=0.3, rely=0.103, relheight=0.047
                , relwidth=0.5)
        
        self.TCombobox1.configure(takefocus="")
		
        self.Label11 = Label(self.TNotebook1_t1)
        self.Label11.place(relx=0.10, rely=0.2, height=21, width=100) #0.077
        self.Label11.configure(background="#d9d9d9")
        self.Label11.configure(disabledforeground="#a3a3a3")
        self.Label11.configure(foreground="#000000")
        self.Label11.configure(text='''Waste Streams Out''')
        self.Label11.configure(width=300)


		
        self.Label12 = Label(self.TNotebook1_t1)
        self.Label12.place(relx=0.15, rely=0.25, height=21, width=100) 
        self.Label12.configure(background="#d9d9d9")
        self.Label12.configure(disabledforeground="#a3a3a3")
        self.Label12.configure(foreground="#000000")
        self.Label12.configure(text='''Residual''')
        self.Label12.configure(width=300)
		
        self.TCombobox2 = ttk.Combobox(self.TNotebook1_t1, postcommand = self.updateModelCbox)
        self.TCombobox2.place(relx=0.3, rely=0.25, relheight=0.047
                , relwidth=0.2)
        self.TCombobox2.configure(takefocus="")


        self.Label13 = Label(self.TNotebook1_t1)
        self.Label13.place(relx=0.15, rely=0.3, height=21, width=100) 
        self.Label13.configure(background="#d9d9d9")
        self.Label13.configure(disabledforeground="#a3a3a3")
        self.Label13.configure(foreground="#000000")
        self.Label13.configure(text='''Aluminium''')
        self.Label13.configure(width=300)
		
        self.TCombobox3 = ttk.Combobox(self.TNotebook1_t1, postcommand = self.updateModelCbox)
        self.TCombobox3.place(relx=0.3, rely=0.3, relheight=0.047
                , relwidth=0.2)
        self.TCombobox3.configure(takefocus="")		
		
        self.Label14 = Label(self.TNotebook1_t1)
        self.Label14.place(relx=0.15, rely=0.35, height=21, width=100) 
        self.Label14.configure(background="#d9d9d9")
        self.Label14.configure(disabledforeground="#a3a3a3")
        self.Label14.configure(foreground="#000000")
        self.Label14.configure(text='''Paper''')
        self.Label14.configure(width=300)
		
        self.TCombobox4 = ttk.Combobox(self.TNotebook1_t1, postcommand = self.updateModelCbox)
        self.TCombobox4.place(relx=0.3, rely=0.35, relheight=0.047
                , relwidth=0.2)
        self.TCombobox4.configure(takefocus="")
		
    def updateModelCbox(self):
        tab_names = []
        for i in self.TNotebook1.tabs():
            tab_names.append(self.TNotebook1.tab(i, "text"))
        self.TCombobox2['values'] = tab_names		
        self.TCombobox3['values'] = tab_names
        self.TCombobox4['values'] = tab_names		
		

	

    def updateFilesCbox(self):
        try:
            self.model_files
        except:
            self.TCombobox1['values'] = {}
        else:
            self.TCombobox1['values'] = self.model_files.getFileList()


		

	
    def onOpenModelFile(self):
        #ftypes = [('CSV files', '*.csv'), ('All files', '*')]
        #dlg = filedialog.Open(self, filetypes = ftypes)
        #fl = dlg.show()
        
        #if fl != '':
            #text = self.readFile(fl)
        #    m = Model(fl)

        filez =  filedialog.askopenfilenames(initialdir = ".",title = "Select files",filetypes = (("CSV files","*.csv"),("All files","*.*")))
        #self.model = Model(root.filename)
        self.model_files=File_Handler (root.tk.splitlist(filez))
        
		
        #for i in range(1,6):
		#	#setting labels
        #    self.Label13 = Label(self.TNotebook1_t0)
        #    self.Label13.place(relx=0.09, rely=0.155*i, height=21, width=120)
        #    self.Label13.configure(background="#d9d9d9")
        #    self.Label13.configure(disabledforeground="#a3a3a3")
        #    self.Label13.configure(foreground="#000000")
        #    self.Label13.configure(text=self.model.data[i][0])
		#	
		#	#setting spinners
        #    self.Spinbox3 = Spinbox(self.TNotebook1_t0, from_=1.0, to=100.0)
        #    self.Spinbox3.place(relx=0.301, rely=0.155*i, relheight=0.033
        #            , relwidth=0.173)
        #    self.Spinbox3.configure(activebackground="#f9f9f9")
        #    self.Spinbox3.configure(background="white")
        #    self.Spinbox3.configure(buttonbackground="#d9d9d9")
        #    self.Spinbox3.configure(disabledforeground="#a3a3a3")
        #    self.Spinbox3.configure(foreground="black")
        #    
        #
        #    self.Spinbox3.configure(format="%.2f")
        #    self.Spinbox3.configure(highlightbackground="black")
        #    self.Spinbox3.configure(highlightcolor="black")
        #    self.Spinbox3.configure(insertbackground="black")
        #    self.Spinbox3.configure(selectbackground="#c4c4c4")
        #    self.Spinbox3.configure(selectforeground="black")
        #    self.Spinbox3.delete(0,"end")			
        #    self.Spinbox3.insert(0,self.model.data[i][1])			

    def onOpenModelDescriptionFile(self):
        file =  filedialog.askopenfilename(initialdir = ".",title = "Select file",filetypes = (("CSV files","*.csv"),("All files","*.*")))
        self.model_description_file=File_Handler (file)
		
        self.Label15 = Label()		
        self.Label15.place(relx=0.4, rely=0.005, height=21, width=500)
        self.Label15.configure(background="#d9d9d9")
        self.Label15.configure(disabledforeground="#a3a3a3")
        self.Label15.configure(foreground="#000000")
        text='Model Description File: ' + self.model_description_file.getFileList()
        self.Label15.configure(text=text)
        #self.Label15.configure(width=120)



if __name__ == '__main__':
    vp_start_gui()



