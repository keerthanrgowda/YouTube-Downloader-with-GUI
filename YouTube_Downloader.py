# Coded by MercyMist
# Project: YouTube Downloader with GUI (Video and Audio)

from tkinter import *
from tkinter import ttk
from pytube import *
from PIL import Image, ImageTk
import requests
import io
import os

class Youtube:
    def __init__(self, window):
        self.window = window
        self.window.title('YouTube Video Downloader | MercyMist')
        self.window.geometry('500x420+300+50')
        self.window.resizable(False, False)
        self.window.config(bg = 'white')
        
        title = Label(self.window, text = 'YouTube Video Downloader', font = ('times new roman', 15), bg = '#262626', fg = 'white').pack(side = TOP, fill = X)

        self.var_url = StringVar()
        url = Label(self.window, text = 'Enter Video URL', font = ('times new roman', 13), bg = 'white').place(x = 10, y = 50)
        url_entry = Entry(self.window, font = ('times new roman', 13), text = self.var_url, bg = 'lightyellow').place(x = 160, y = 50, width = 300)
        filetype = Label(self.window, text = 'File Type', font = ('times new roman', 13), bg = 'white').place(x = 10, y = 90)

        self.var_filetype = StringVar()
        self.var_filetype.set('Video')
        video_radio = Radiobutton(self.window, text = 'Video', variable = self.var_filetype, value = 'Video', font = ('times new roman', 13), bg = 'white').place(x = 160, y = 90)
        audio_radio = Radiobutton(self.window, text = 'Audio', variable = self.var_filetype, value = 'Audio', font = ('times new roman', 13), bg = 'white').place(x = 260, y = 90)

        search = Button(self.window, text = 'Search', command = self.search, font = ('times new roman', 13), bg = 'lightblue').place(x = 360, y = 90, height = 30, width = 100)

        frame1 = Frame(self.window, bd = 2, relief = RIDGE, bg = 'lightyellow')
        frame1.place(x = 10, y = 130, width = 480, height = 180)

        self.video_title = Label(frame1, text = 'Video Title Here..', font = ('times new roman', 12), bg = 'lightgrey', anchor = 'w')
        self.video_title.place(x = 0, y = 0, relwidth = 1)

        self.video_thumbnail = Label(frame1, text = 'Video \n Thumbnail', font = ('times new roman', 15), bg = 'lightgrey', bd = 2, relief = RIDGE)
        self.video_thumbnail.place(x = 5, y = 30, width = 180, height = 140)

        desc = Label(frame1, text = 'Video Description', font = ('times new roman', 12), bg = 'lightyellow')
        desc.place(x = 190, y = 30)

        self.video_desc = Text(frame1, font = ('times new roman', 12), bg = 'lightyellow')
        self.video_desc.place(x = 190, y = 60, width = 280, height = 110)

        self.video_size = Label(self.window, text = 'Total Size: 0MB', font = ('times new roman', 13), bg = 'white')
        self.video_size.place(x = 10, y = 320)

        self.download_percentage = Label(self.window, text = 'Downloading: 0%', font = ('times new roman', 13), bg = 'white')
        self.download_percentage.place(x = 155, y = 320)

        clear_button = Button(self.window, text = 'Clear', command = self.clear, font = ('times new roman', 13), bg = 'grey').place(x = 320, y = 320, height = 30, width = 70)

        self.download_button = Button(self.window, text = 'Download', state = DISABLED, command = self.download, font = ('times new roman', 13), bg = 'lightgreen')
        self.download_button.place(x = 400, y = 320, height = 30, width = 90)

        self.progress_bar = ttk.Progressbar(self.window, orient = HORIZONTAL, length = 590, mode = 'determinate')
        self.progress_bar.place(x = 10, y = 360, width = 480, height = 20)

        self.message = Label(self.window, text = '', font = ('times new roman', 12), bg = 'white')
        self.message.place(x = 0, y = 385, relwidth = 1)

        # Specifying Directories for Downloaded Files
        if os.path.exists('Video Files') == False:
            os.mkdir('Video Files')
        if os.path.exists('Audio Files') == False:
            os.mkdir('Audio Files')

    # Functions

    def search(self):
        if self.var_url.get() == '':
            self.message.config(text = 'URL Required!', fg = 'red')
        else:
            yt = YouTube(self.var_url.get())

            # Convert Image URL into Image
            response = requests.get(yt.thumbnail_url)
            img_byte = io.BytesIO(response.content)
            self.img = Image.open(img_byte)
            self.img = self.img.resize((180, 140), Image.ANTIALIAS)
            self.img = ImageTk.PhotoImage(self.img)

            # Fetch File Size as per Type
            if self.var_filetype.get() == 'Video':
                select = yt.streams.filter(progressive = 'True').first()
            else:
                select = yt.streams.filter(only_audio = 'True').first()
            
            self.size_inBytes = select.filesize
            size_inMB = self.size_inBytes / 1024000
            self.mb = str(round(size_inMB, 2)) + 'MB'

            # Linking to GUI Elements
            self.video_title.config(text = yt.title)
            self.video_thumbnail.config(image = self.img)
            self.video_desc.delete('1.0', END)
            self.video_desc.insert(END, yt.description[:200])
            self.video_size.config(text = f'Total Size: {self.mb}')
            self.download_button.config(state = NORMAL)

    def download(self):
        yt = YouTube(self.var_url.get(), on_progress_callback = self.progressBar)

        if self.var_filetype.get() == 'Video':
            select = yt.streams.filter(progressive = 'True').first()
            select.download('Video Files/')
        else:
            select = yt.streams.filter(only_audio = 'True').first()
            select.download('Audio Files/')

    def progressBar(self, streams, chunk, bytes_remaining):
        percentage = (float(abs(bytes_remaining - self.size_inBytes) / self.size_inBytes)) * float(100)
        self.progress_bar['value'] = percentage
        self.progress_bar.update()
        self.download_percentage.config(text = f'Downloading: {str(round(percentage, 2))}%')

        if round(percentage, 2) == 100:
            self.message.config(text = 'Download Complete!', fg = 'green')
            self.download_button.config(state = DISABLED)

    def clear(self):
        self.var_filetype.set('Video')
        self.var_url.set('')
        self.video_title.config(text = 'Video Title Here..')
        self.video_thumbnail.config(image = '')
        self.video_desc.delete('1.0', END)
        self.progress_bar['value'] = 0
        self.download_button.config(state = DISABLED)
        self.message.config(text = '')
        self.video_size.config(text = 'Total Size: 0MB')
        self.download_percentage.config(text = 'Downloading: 0%')

window = Tk()
obj = Youtube(window)
window.mainloop()
