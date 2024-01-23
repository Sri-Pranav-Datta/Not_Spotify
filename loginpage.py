import customtkinter,tkinter,os,pickle,urllib.request, io
from PIL import Image
customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

root = customtkinter.CTk()  # create CTk window like you do with the Tk window
root.title("Not Spotify")
root.iconbitmap("icon.ico")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
width = 600
height = 410
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry(('%dx%d+%d+%d')%(width,height,x+550,y+50))
img = customtkinter.CTkImage(light_image=Image.open("bg.png"),
                                  dark_image=Image.open("bg.png"),
                                  size=(600,410))
lab = customtkinter.CTkLabel(root,text='',image=img)
lab.grid(row=0,column=0)
frame = customtkinter.CTkFrame(root,fg_color='#bfcbd7',bg_color='#bfcbd7')
frame.grid(padx=80,pady=88,row=0,column=0,sticky='s')
lab1 = customtkinter.CTkLabel(frame,text='LOGIN',corner_radius=8,fg_color='#bfcbd7',bg_color='#bfcbd7',text_color='black')
lab1.grid(row=0,column=1,columnspan=2,sticky='nw',pady=8)
lab2 = customtkinter.CTkLabel(frame,text='Username :',corner_radius=8,fg_color='#bfcbd7',bg_color='#bfcbd7',text_color='black')
lab2.grid(row=1,column=0)
lab3 = customtkinter.CTkLabel(frame,text='Password :',corner_radius=8,fg_color='#bfcbd7',bg_color='#bfcbd7',text_color='black')
lab3.grid(row=2,column=0)
entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="Enter",bg_color='#bfcbd7',border_color='#bfcbd7')
entry1.grid(row=1,column=1,columnspan =3)
entry2 = customtkinter.CTkEntry(master=frame, placeholder_text="Enter",bg_color='#bfcbd7',border_color='#bfcbd7',show="*")
entry2.grid(row=2,column=1,columnspan =3)
but1 = customtkinter.CTkButton(frame,text='Confirm',width=5)
but1.grid(row=3,column=2,columnspan =3,padx=4,sticky='e',pady=8)

root.mainloop()