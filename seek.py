import customtkinter,os,tkinter,pickle,time
from PIL import Image
from pygame import mixer
from mutagen.mp3 import MP3

root=customtkinter.CTk()
root.title("SEEK")

mixer.init()
leftframe = customtkinter.CTkFrame(root,width=500,height=600,corner_radius=30)
leftframe.grid(row=2,column=0,rowspan=2,columnspan=4,sticky='WES',padx=25,pady=10)
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
pause=False

def play_time():
    global current_time
    current_time=mixer.music.get_pos()/1000
    converted_time=time.strftime('%M:%S',time.gmtime(current_time))

    #getting song length
    song_mut=MP3(playlist[current])
    global song_length
    song_length=song_mut.info.length
    seek.configure(to=song_length)
    converted_song_duration=time.strftime('%M:%S',time.gmtime(song_length))
    #setting end value of seek
    seek.set(int(current_time))
    seek.after(1000,play_time)
    
    if int(seek.get())==int(song_length):
        nextsong()


def slider(x):
    mixer.music.load(playlist[current])
    mixer.music.play(loops=0,start=int(seek.get()))

def playsong(event=None):
            global pause
            pause=False
            play_button.configure(image=pause_button_img)
            if event is not None:
                global current
                current= list.curselection()[0]
                mixer.music.load(playlist[current])
                mixer.music.play()
            play_time()
            

            
def pausesong():
            global pause
            global current
            pause= not pause
            if pause==True:
                play_button.configure(image=play_button_img)
                mixer.music.pause()
            else:
                play_button.configure(image=pause_button_img)
                mixer.music.unpause()
def prevsong():
            global pause
            global current
            list.selection_clear(0,customtkinter.END)
            pause=False
            play_button.configure(image=pause_button_img)
            list.itemconfigure(current, bg='grey')
            current-=1
            list.itemconfigure(current, bg='#bfcbd7')
            mixer.music.load(playlist[current])
            mixer.music.play()
def nextsong():
            global pause
            global current
            list.selection_clear(0,customtkinter.END)
            play_button.configure(image=pause_button_img)
            list.itemconfigure(current, bg='grey')
            current+=1
            list.itemconfigure(current, bg='#bfcbd7')
            list.activate(current)
            mixer.music.load(playlist[current])
            mixer.music.play()

def volume_control(value):
            volume=volume_slider.get()
            mixer.music.set_volume(value/1000)
            pass

volume_slider = customtkinter.CTkSlider(leftframe,orientation=customtkinter.VERTICAL, from_ = 0, to = 100,command=volume_control)
volume_slider.grid(row=0,column=4,padx=10,pady=10,sticky='w')
play_button = customtkinter.CTkButton(leftframe,image=play_button_img,fg_color='transparent',text='',width=30,command=pausesong)
play_button.grid(row=0,column=1,padx=5,pady=10)
back_button = customtkinter.CTkButton(leftframe,image=back_button_img,fg_color='transparent',text='',width=30,command=prevsong)
back_button.grid(row=0,column=0,padx=5,pady=10,sticky='e')
fwd_button = customtkinter.CTkButton(leftframe,image=fwd_button_img,fg_color='transparent',text='',width=30,command=nextsong)
fwd_button.grid(row=0,column=2,padx=5,pady=10,sticky='w')
pause_button = customtkinter.CTkButton(leftframe,image=pause_button_img,fg_color='transparent',text='',width=30)
seek=customtkinter.CTkSlider(leftframe,from_=0,to=100,orientation=customtkinter.HORIZONTAL,command=slider)
seek.grid(row=0,column=3)
seek.set(0)
#RightFrame
rightframe = customtkinter.CTkFrame(root,width=500,height=540,corner_radius=30)
rightframe.grid(row=0,column=4,rowspan=6,padx=15,pady=20,sticky='w',ipadx=10,ipady=20)
scrollbar = customtkinter.CTkScrollbar(rightframe,orientation=tkinter.VERTICAL)
scrollbar.grid(row=0,column=5, rowspan=6, sticky='ns',padx=5,pady=5)

list = tkinter.Listbox(rightframe, selectmode=tkinter.BROWSE,font=('Times', 22),
                                    yscrollcommand=scrollbar.set,width=60,height=50,selectbackground='#bfcbd7',background='grey')
list.config(height=18)
list.bind('<Double-1>', playsong)
list.grid(row=0,rowspan=6,column=4,padx=50,pady=25,sticky='s')
scrollbar.configure(command=list.yview)

def enumerate_songs():
            for index, song in enumerate(playlist):
                list.insert(index, os.path.basename(song)[:-4])

def retrieve_songs():
                songlist = []
                directory='Songs'
                for root_, dirs, files in os.walk(directory):
                        for file in files:
                            if os.path.splitext(file)[1] == '.mp3':
                                path = (root_ + '/' + file).replace('\\','/')
                                songlist.append(path)

                with open('songs.pickle', 'wb') as f:
                    pickle.dump(songlist, f)
                global playlist
                playlist = songlist
                list.delete(0, tkinter.END)
                enumerate_songs()
        


retrieve_songs()
root.mainloop()
