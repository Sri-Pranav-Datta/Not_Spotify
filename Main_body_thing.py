import customtkinter,tkinter,os,pickle,urllib.request,re,pydub,glob
from PIL import Image
from pytube import YouTube
import speech_recognition as sr
import login_screen
from pygame import mixer

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
        customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

        mixer.init()
        self.current = 0
        
        self.title("Not Spotify")
        self.iconbitmap("icon.ico")
        width= 1100 ; height = 580
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width/2) - (width/2) + 150
        y = (screen_height/2) - (height/2) +200
        self.geometry(('%dx%d+%d+%d')%(width,height,x,y))

        def yt_url_finder(search_for):
            html = urllib.request.urlopen(
                'https://www.youtube.com/results?search_query=' + search_for)
            video_ids = re.findall(r'watch\?v=(\S{11})', html.read().decode())
            vid_url = 'https://www.youtube.com/watch?v=' + video_ids[0]
            return vid_url

        def downloader(key):
            url = yt_url_finder(key)
            video = YouTube(url)
            print('Title: ', video.title)
            print("This should only take a few seconds.....")
            title = video.title
            k= ['[','(','Offical','Video','video','offical',"Lyric",'lyric','|','/','M/V']
            l=title.split(' ')
            print(l)
            for i in l:
                if i in k or i[0] in k:
                    del l[l.index(i):]

            title=' '.join(l)
            out_path = video.streams.filter(only_audio=True).first().download(output_path='Songs/',filename=title+'.webM')
            print(video.title, "was downloaded into this project file's location")

            webm_files = glob.glob('Songs/*.webm')
            all_files = [webm_files]

            for files in all_files:
                for file in files:
                    mp3_file = os.path.splitext(file)[0] + '.mp3'
                    sound = pydub.AudioSegment.from_file(file)
                    print("Converting: ", file)
                    sound.export(mp3_file, format="mp3")
                    os.remove(file)
                    print("Conversion Complete")
                    retrieve_songs(self)
        
        def voice_window():
            
            def retry():
                global speech
                speech = speech_to_text()
                label1_text= 'Did you say '+ speech[0]+' ?'
                voice_label1 = customtkinter.CTkLabel(voice_frame,text=label1_text)
                voice_label1.grid(row=1,column=0,sticky='we',padx=10,pady=5,columnspan=2)
            def confirm():
                global download_this
                download_this= speech[-1]
                app.listening_label.grid_forget()
                voice_window.destroy()
                downloader(download_this)
            
            def speech_to_text():
                r = sr.Recognizer()
                while True:
                    try:
                        with sr.Microphone() as source2:
                            print('Listening...')
                            r.adjust_for_ambient_noise(source2, duration=0.2)
                            audio2 = r.listen(source2)
                            MyText = r.recognize_google(audio2)
                            MyText = MyText.lower()
                            print(f'Did you say {MyText}')
                            MyText = (MyText,''.join([i for i in MyText.split()]))
                            return MyText
                    except sr.RequestError as e:
                        print("Could not request results; {0}".format(e))
                    except sr.UnknownValueError:
                        print("unknown error occurred")

            voice_window = customtkinter.CTk()
            width= 400 ; height = 300
            screen_width = voice_window.winfo_screenwidth()
            screen_height = voice_window.winfo_screenheight()
            x = (screen_width/2) - (width/2) +500
            y = (screen_height/2) - (height/2) +150
            voice_window.geometry(('%dx%d+%d+%d')%(width,height,x,y))
            voice_window.iconbitmap("icon.ico")
            global voice_frame
            voice_frame = customtkinter.CTkFrame(voice_window,width=400,height=400)
            voice_frame.grid(padx=40,pady=30,row=0,column=0,rowspan=4,columnspan=2,ipady=10)
            voice_symbol = customtkinter.CTkLabel(voice_frame,text=u'\U0001F399',font=('calibre',120)).grid(row=0,column=0,columnspan=2)
            global speech
            speech=speech_to_text()
            global voice_label1
            voice_label1 = customtkinter.CTkLabel(voice_frame,text='Did you say '+speech[0]+'?')
            voice_label1.grid(row=1,column=0,sticky='we',padx=10,pady=5,columnspan=2)
            voice_button1 = customtkinter.CTkButton(voice_frame,text='Confirm',command=confirm).grid(row=2,column=0,sticky='e',padx=10,pady=10)
            voice_button2 =customtkinter.CTkButton(voice_frame,text='Try again',command=retry).grid(row=2,column=1,sticky='e',padx=10,pady=10)

            voice_window.mainloop()

        def voice_action():
            self.listening_label.grid(row=1,column=2)
            voice_window()
        
        search_item= customtkinter.StringVar()
        search_item.set(u"\U0001F50D "+'Search here...')

        def y():
            global download_this
            download_this = ''.join([i for i in search_item.get().split()])
            downloader(download_this)
            self.search_bar.delete(0,tkinter.END)
        
        def click(*args):
            self.search_bar.delete(0, 'end')
        def signout():
            self.destroy()
            #shutil.rmtree(f'{login_screen.username}')
            login_screen.login_screen()
        
        #Top frame stuff
        self.topframe = customtkinter.CTkFrame(self,width=1060,height=120,corner_radius=30)
        self.topframe.grid(row=0,column=0,rowspan=2,columnspan=2,sticky='WE',padx=20,pady=10,ipadx=5)
        self.search_bar = customtkinter.CTkEntry(self.topframe,textvariable=search_item,width=200,height=32,placeholder_text=u"\U0001F50D "+'Search here...')
        self.search_bar.bind("<Button-1>", click)
        self.search_bar.grid(row=0,column=1,padx=10,pady=25,sticky='w',rowspan=2)
        self.search_button =  customtkinter.CTkButton(self.topframe,corner_radius=8,width=5,height=5,text=u"\U0001F50D ",font=('calibre',30)
        ,fg_color='transparent',border_color='black',command=y)
        self.search_button.grid(row=0,column=0,padx =5,pady= 40,sticky='e',rowspan=2)
        self.voicesearch_button = customtkinter.CTkButton(self.topframe,corner_radius=8,width=5,height=5,text=u'\U0001F399',font=('calibre',30)
        ,fg_color='transparent',border_color='black',command=voice_action)
        self.voicesearch_button.grid(row=0,column=2,padx =5,pady= 40,sticky='nw',rowspan=2)
        self.listening_label = customtkinter.CTkLabel(self.topframe,text='Listening... ')
        self.username_Label = customtkinter.CTkLabel(self.topframe,text=login_screen.username)
        self.username_Label.grid(row=0,column=3,padx=13,sticky='wse')
        self.signout_button = customtkinter.CTkButton(self.topframe,corner_radius=40,width=15,text='signout',fg_color='transparent',command=signout)
        self.signout_button.grid(row=1,column=3,padx=13,pady=8,sticky='ne')

        userpic = customtkinter.CTkImage(light_image=Image.open(f"{login_screen.username}/{login_screen.username}.png"),
                                  dark_image=Image.open(f"{login_screen.username}/{login_screen.username}.png"),
                                  size=(75,75))
        
        self.userpic_label = customtkinter.CTkLabel(self.topframe,image=userpic,text='')
        self.userpic_label.grid(row=0,column=4,padx =10,pady= 25,rowspan=2,sticky='w')

        #Song controls stuff
        self.leftframe = customtkinter.CTkFrame(self,width=500,height=390,corner_radius=30)
        self.leftframe.grid(row=2,column=0,rowspan=2,columnspan=4,sticky='WES',padx=25,pady=10)
        fwd_button_img = customtkinter.CTkImage(light_image=Image.open(f"pictures\\next_Custom.png"),
                                  dark_image=Image.open(f"pictures\\next_Custom.png"),
                                  size=(30,30))
        back_button_img = customtkinter.CTkImage(light_image=Image.open(f"pictures\\back_Custom.png"),
                                  dark_image=Image.open(f"pictures\\back_Custom.png"),
                                  size=(30,30))
        play_button_img = customtkinter.CTkImage(light_image=Image.open(f"pictures\\play_Custom.png"),
                                  dark_image=Image.open(f"pictures\\play_Custom.png"),
                                  size=(30,30))
        pause_button_img = customtkinter.CTkImage(light_image=Image.open(f"pictures\\pause_Custom.png"),
                                  dark_image=Image.open(f"pictures\\pause_Custom.png"),
                                  size=(30,30))
        self.pause=False

        def playtime(self):
            self.current_time=mixer.music.get_pos()/1000
            

        def playsong(event=None):
            self.pause=False
            self.play_button.configure(image=pause_button_img)
            if event is not None:
                self.current= self.list.curselection()[0]
                mixer.music.load(self.playlist[self.current])
                mixer.music.play()
        def pausesong():
            self.pause= not self.pause
            if self.pause==True:
                self.play_button.configure(image=play_button_img)
                mixer.music.pause()
            else:
                self.play_button.configure(image=pause_button_img)
                mixer.music.unpause()
        def prevsong():
            self.list.selection_clear(0,customtkinter.END)
            self.pause=False
            self.play_button.configure(image=pause_button_img)
            self.list.itemconfigure(self.current, bg='grey')
            self.current-=1
            self.list.itemconfigure(self.current, bg='#bfcbd7')
            mixer.music.load(self.playlist[self.current])
            mixer.music.play()
        def nextsong():
            self.list.selection_clear(0,customtkinter.END)
            self.play_button.configure(image=pause_button_img)
            self.list.itemconfigure(self.current, bg='grey')
            self.current+=1
            self.list.itemconfigure(self.current, bg='#bfcbd7')
            self.list.activate(self.current)
            mixer.music.load(self.playlist[self.current])
            mixer.music.play()

        def volume_control(value):
            volume=self.volume_slider.get()
            mixer.music.set_volume(value/1000)
            pass

        self.volume_slider = customtkinter.CTkSlider(self.leftframe,orientation=customtkinter.VERTICAL, from_ = 0, to = 100,command=volume_control)
        self.volume_slider.grid(row=2,column=4,padx=10,pady=10,sticky='w')
        self.play_button = customtkinter.CTkButton(self.leftframe,image=play_button_img,fg_color='transparent',text='',width=30,command=pausesong)
        self.play_button.grid(row=2,column=1,padx=5,pady=10)
        self.back_button = customtkinter.CTkButton(self.leftframe,image=back_button_img,fg_color='transparent',text='',width=30,command=prevsong)
        self.back_button.grid(row=2,column=0,padx=5,pady=10,sticky='e')
        self.fwd_button = customtkinter.CTkButton(self.leftframe,image=fwd_button_img,fg_color='transparent',text='',width=30,command=nextsong)
        self.fwd_button.grid(row=2,column=2,padx=5,pady=10,sticky='w')
        self.pause_button = customtkinter.CTkButton(self.leftframe,image=pause_button_img,fg_color='transparent',text='',width=30)
        
        #song pic
        #self.yt = YouTube(yt_url_finder(''))
        #self.raw_data = urllib.request.urlopen(self.yt.thumbnail_url).read()
        #self.songimage = customtkinter.CTkImage(light_image=Image.open(io.BytesIO(self.raw_data)),dark_image=Image.open(io.BytesIO(self.raw_data)),size=(350,290))
        #self.songpic = customtkinter.CTkLabel(self,text='',image=self.songimage,width=370,height=320,corner_radius=30)
        #self.songpic.grid(row=2,column=0,padx=15,pady=20,ipady=10)


        #RightFrame
        self.rightframe = customtkinter.CTkFrame(self,width=500,height=540,corner_radius=30)
        self.rightframe.grid(row=0,column=4,rowspan=6,padx=15,pady=20,sticky='w',ipadx=10,ipady=20)
        self.scrollbar = customtkinter.CTkScrollbar(self.rightframe,orientation=tkinter.VERTICAL)
        self.scrollbar.grid(row=0,column=5, rowspan=6, sticky='ns',padx=5,pady=5)

        self.list = tkinter.Listbox(self.rightframe, selectmode=tkinter.BROWSE,font=('Times', 22),
                                    yscrollcommand=self.scrollbar.set,width=60,height=50,selectbackground='#bfcbd7',background='grey')
        self.list.config(height=18)
        self.list.bind('<Double-1>', playsong)
        self.list.grid(row=0,rowspan=6,column=4,padx=50,pady=25,sticky='s')
        self.scrollbar.configure(command=self.list.yview)
        
        def retrieve_songs(self):
                self.songlist = []
                directory='Songs'
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
                self.list.insert(index, os.path.basename(song)[:-4])
                

login_screen.login_screen()
app = App()
app.mainloop()
