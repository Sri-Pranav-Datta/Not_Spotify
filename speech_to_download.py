from pytube import YouTube
import urllib.request,re,pydub,glob,os
import speech_recognition as sr,customtkinter

def yt_url_finder(search_for):
    html = urllib.request.urlopen(
        'https://www.youtube.com/results?search_query=' + search_for)
    video_ids = re.findall(r'watch\?v=(\S{11})', html.read().decode())
    vid_url = 'https://www.youtube.com/watch?v=' + video_ids[0]
    return vid_url

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
                MyText = ''.join([i for i in MyText.split()])
                return MyText
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("unknown error occurred")

def downloader():
    screen = customtkinter.CTk()
    screen.geometry(f"{300}x{580}")

    url = yt_url_finder(speech_to_text())
    video = YouTube(url)
    print('Title: ', video.title)
    print("This should only take a few seconds.....")
    title = video.title
    out_path = video.streams.filter(only_audio=True).first().download(output_path='Songs\\',filename=title[:title.find('|')]+'.webM')
    print(video.title, "was downloaded into this project file's location")

    webm_files = glob.glob('Songs\\*.webm')
    all_files = [webm_files]

    for files in all_files:
        for file in files:
            mp3_file = os.path.splitext(file)[0] + '.mp3'
            sound = pydub.AudioSegment.from_file(file)
            print("Converting: ", file)
            sound.export(mp3_file, format="mp3")
            os.remove(file)
            print("Conversion Complete")

downloader()