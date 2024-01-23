import customtkinter
import speech_recognition as sr

def voice_window():
    def retry():
        global speech
        speech = speech_to_text()
        label1_text= 'Did you say '+ speech+' ?'
        voice_label1 = customtkinter.CTkLabel(voice_frame,text=label1_text)
        voice_label1.grid(row=1,column=0,sticky='we',padx=10,pady=5,columnspan=2)
    def confirm():
        print(speech)
        voice_window.destroy()
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
                    print(f'Searching for {MyText}')
                    #MyText = ''.join([i for i in MyText.split()])
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
    voice_frame = customtkinter.CTkFrame(voice_window,width=400,height=400)
    voice_frame.grid(padx=40,pady=30,row=0,column=0,rowspan=4,columnspan=2,ipady=10)
    voice_symbol = customtkinter.CTkLabel(voice_frame,text=u'\U0001F399',font=('calibre',120)).grid(row=0,column=0,columnspan=2)
    global speech
    speech=speech_to_text()
    voice_label1 = customtkinter.CTkLabel(voice_frame,text='Did you say '+speech+'?')
    voice_label1.grid(row=1,column=0,sticky='we',padx=10,pady=5,columnspan=2)
    voice_button1 = customtkinter.CTkButton(voice_frame,text='Confirm',command=confirm).grid(row=2,column=0,sticky='e',padx=10,pady=10)
    voice_button2 =customtkinter.CTkButton(voice_frame,text='Try again',command=retry).grid(row=2,column=1,sticky='e',padx=10,pady=10)

    voice_window.mainloop()
voice_window()