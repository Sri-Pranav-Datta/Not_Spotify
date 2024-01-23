import customtkinter,tkinter,os,pickle,urllib.request, io
from PIL import Image
from pytube import YouTube

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1100}x{580}")

        #Top frame stuff
        self.topframe = customtkinter.CTkFrame(self,width=1060,height=120,corner_radius=30)
        self.topframe.grid(row=0,column=0,rowspan=2,columnspan=2,sticky='WE',padx=20,pady=10)
        self.search_bar = customtkinter.CTkEntry(self.topframe,width=200,height=32,placeholder_text=u"\U0001F50D "+'Search here...')
        self.search_bar.grid(row=0,column=0,padx=20,pady=25,sticky='E',rowspan=2)
        self.voicesearch_button = customtkinter.CTkButton(self.topframe,corner_radius=8,width=5,height=5,text=u'\U0001F399',font=('calibre',30),fg_color='transparent',border_color='black')
        self.voicesearch_button.grid(row=0,column=1,padx =5,pady= 40,sticky='nw',rowspan=2)
        self.username_Label = customtkinter.CTkLabel(self.topframe,text='Username ')
        self.username_Label.grid(row=0,column=2,padx=13,ipady=5,sticky='se')
        self.signout_button = customtkinter.CTkButton(self.topframe,corner_radius=40,width=15,text='signout',fg_color='transparent')
        self.signout_button.grid(row=1,column=2,padx=13,pady=8,sticky='ne')

        userpic = customtkinter.CTkImage(light_image=Image.open("output.png"),
                                  dark_image=Image.open("output.png"),
                                  size=(75,75))

        self.userpic_label = customtkinter.CTkLabel(self.topframe,image=userpic,text='')
        self.userpic_label.grid(row=0,column=3,padx =15,pady= 25,rowspan=2,sticky='w')

        #Song controls stuff
        self.leftframe = customtkinter.CTkFrame(self,width=500,height=390,corner_radius=30)
        self.leftframe.grid(row=2,column=0,rowspan=2,columnspan=2,sticky='ES',padx=25,pady=10)
        #song pic
        self.yt = YouTube('https://www.youtube.com/watch?v=50VNCymT-Cs')
        self.raw_data = urllib.request.urlopen(self.yt.thumbnail_url).read()
        self.songimage = customtkinter.CTkImage(light_image=Image.open(io.BytesIO(self.raw_data)),dark_image=Image.open(io.BytesIO(self.raw_data)),size=(350,290))
        self.songpic = customtkinter.CTkLabel(self,text='',image=self.songimage,width=370,height=320,corner_radius=30)
        self.songpic.grid(row=2,column=0,padx=15,pady=20,ipady=10)
        
        #RightFrame
        self.rightframe = customtkinter.CTkFrame(self,width=500,height=540,corner_radius=30)
        self.rightframe.grid(row=0,column=4,rowspan=6,padx=15,pady=20,sticky='w',ipadx=10,ipady=20)
        self.scrollbar = customtkinter.CTkScrollbar(self.rightframe,orientation=tkinter.VERTICAL)
        self.scrollbar.grid(row=0,column=5, rowspan=6, sticky='ns',padx=5,pady=5)

        self.list = tkinter.Listbox(self.rightframe, selectmode=tkinter.SINGLE,font=('Times', 20),
                                    yscrollcommand=self.scrollbar.set,width=60,height=50,selectbackground='sky blue',background='grey')
        self.list.config(height=22)
        self.list.grid(row=0,rowspan=6,column=4,padx=50,pady=25,sticky='s')
        self.scrollbar.configure(command=self.list.yview)
        
        def retrieve_songs(self):
                self.songlist = []
                directory='C:\Users\chpra\OneDrive\Desktop\Project\programms'
                for root_, dirs, files in os.walk(directory):
                        for file in files:
                            if os.path.splitext(file)[1] == '.mp3':
                                path = (root_ + '/' + file).replace('\\','/')
                                self.songlist.append(path)

                with open('songs.pickle', 'wb') as f:
                    pickle.dump(self.songlist, f)
                self.playlist = self.songlist
                self.list.delete(0, tkinter.END)
                self.enumerate_songs()
        
        retrieve_songs(self)
    
    def enumerate_songs(self):
            for index, song in enumerate(self.playlist):
                self.list.insert(index, os.path.basename(song))

app = App()
app.mainloop()
