from tkinter import *
import pygame,os
import time
import tkinter.ttk as ttk
from mutagen.mp3 import MP3

root=Tk()
root.title("controls")
root.geometry("400x300")

pygame.mixer.init()

playlist=os.listdir(r"C:\Users\chpra\OneDrive\Desktop\Project\programms\Songs")

mstate=0


song_no=int(0)
song_no2=(song_no)
current_song=(playlist[song_no])

def Play_time():
    current_time=pygame.mixer.music.get_pos()/1000
    converted_time=time.strftime('%M:%S',time.gmtime(current_time))
    status_bar.config(text=converted_time)
    #getting song length
    song_mut=MP3(current_song)
    global song_length
    song_length=song_mut.info.length
    converted_song_duration=time.strftime('%M:%S',time.gmtime(song_length))
    seek.config(value=current_time)
    seek.after(1000,Play_time)
    song_position.config(text=converted_time)
    song_position.after(1000,Play_time)
    song_duration.config(text=converted_song_duration)
    

    

def Play_music():
     global mstate
     if mstate == 0:  # music not started
         pygame.mixer.music.play()
         play_pause_button.configure(text = "Pause")
         play_pause_button.configure(image=pause_button_img)
         mstate =  1
         Play_time()
         return
        
     elif mstate == 1:  # music playing
         pygame.mixer.music.pause()
         play_pause_button.configure(text = "Resume")
         play_pause_button.configure(image=play_button_img)
     else:  # music paused
         pygame.mixer.music.unpause()
         play_pause_button.configure(text = "Pause")
         play_pause_button.configure(image=pause_button_img)
     mstate = 3-mstate  # swap pause state
     Play_time()


def Play_next():
    global song_no
    global song_no2
    global current_song
    pygame.mixer.music.stop()
    song_no=int(song_no2 + 1)
    song_no2=int(song_no)
    current_song=(playlist[song_no])
    pygame.mixer.music.load(current_song)
    pygame.mixer.music.play()

def Play_previous():
    global song_no
    global song_no2
    global current_song
    pygame.mixer.music.stop()
    song_no=int(song_no2 - 1)
    song_no2=int(song_no)
    current_song=(playlist[song_no])
    pygame.mixer.music.load(current_song)
    pygame.mixer.music.play()


songs=Listbox(root,bg="grey",fg="black",width=50)
songs.pack(pady=20)
#button images
fwd_button_img=PhotoImage(file="pictures\\next_Custom.png")
back_button_img=PhotoImage(file="pictures\\back_Custom.png")
play_button_img=PhotoImage(file="pictures\\play_Custom.png")
pause_button_img=PhotoImage(file="pictures\\pause_Custom.png")

#controls frame
controls_frame=Frame(root)
controls_frame.pack()
#creating buttons
fwd_button=Button(controls_frame,image=fwd_button_img,borderwidth=0,command=Play_next)
back_button=Button(controls_frame,image=back_button_img,borderwidth=0,command=Play_previous)
play_pause_button=Button(controls_frame,text="Play",image=play_button_img,borderwidth=0,command=Play_music)

fwd_button.grid(row=0,column=2)
back_button.grid(row=0,column=0)
play_pause_button.grid(row=0,column=1)

#creating the seek frame
seek_frame=Frame(root)
seek_frame.pack()
seek=ttk.Scale(seek_frame,from_=0,to=100,orient=HORIZONTAL,length=300)
seek.grid(row=0,column=1)
song_position=Label(seek_frame,text="",bd=1,fg="black")
song_position.grid(row=0,column=0)
song_duration=Label(seek_frame,text="",bd=1,fg="black")
song_duration.grid(row=0,column=2)

#status bar
status_bar=Label(root,text='',bd=1,relief=GROOVE,anchor=E)
status_bar.pack(fill=X,side=BOTTOM,ipady=2)
pygame.mixer.music.load(current_song)

root.mainloop()