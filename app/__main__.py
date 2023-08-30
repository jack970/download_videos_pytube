from PIL import Image
import customtkinter, os, requests, io, threading, tkinter.filedialog as tk_filedialog
from baixar_youtube import Baixar_Youtube
from resource_path import resourcePath

LOGO = resourcePath("logo.png")
ICON = resourcePath("logo.ico")

class App(customtkinter.CTk):
    customtkinter.set_appearance_mode("Dark")

    LOGO_IMAGE = customtkinter.CTkImage(Image.open(LOGO), size=(200, 200))
    PATH_DOWNLOADS = os.path.join(os.path.expanduser("~"), "Downloads")

    def __init__(self):
        super().__init__()
        self.resizable(width=False, height=False)
        self.iconbitmap(ICON)
        self.geometry("400x550")
        self.title("Youtube Downloader")

        self.logo_image = self.LOGO_IMAGE
        self.path_download = self.PATH_DOWNLOADS

        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(6, weight=1)

        self.options = ["MP3", "MP4", "Playlist"]

        self.label_bar_url = customtkinter.CTkLabel(self, text="URL:", width=2)
        self.label_bar_url.grid(row=1, column=1, padx=10, sticky="w")

        self.entry_bar_url = customtkinter.CTkEntry(self, width=350)
        self.entry_bar_url.grid(row=1, columnspan=4, padx=10, pady=10, stick="e")

        self.variable_path_download = customtkinter.StringVar(value=self.path_download)
        self.entry_path_download = customtkinter.CTkEntry(self, width=200, textvariable=self.variable_path_download, state="disabled")
        self.entry_path_download.grid(row=2, columnspan=3, padx=10, pady=10, stick="new")

        self.button_save_path_download = customtkinter.CTkButton(self, text="Salvar Pasta", command=self.open_directory_save)
        self.button_save_path_download.grid(row=2, column=3, padx=10, pady=10, sticky="ne")

        self.grid_columnconfigure(1, weight=1)

        self.option_selected = customtkinter.StringVar(value="mp4")

        for idx, item in enumerate(self.options):
            self.radiobutton_frame = customtkinter.CTkRadioButton(self, text=item, value=item.lower(), variable=self.option_selected)
            self.radiobutton_frame.grid(row=3, column=idx + 1, padx=(20, 20), pady=(10, 0), sticky="n")
        
        self.image_video = customtkinter.CTkLabel(self, text="", image=self.logo_image)
        self.image_video.grid(row=4, columnspan=4, pady=30, sticky="nsew")

        self.title_video = customtkinter.CTkLabel(self, text="")
        self.title_video.grid(row=5, columnspan=4)

        self.descrition_video = customtkinter.CTkLabel(self, text="")
        self.descrition_video.grid(row=6, columnspan=4)

        self.text_progress_bar = customtkinter.CTkLabel(self, text='0%')
        self.text_progress_bar.grid(row=7, columnspan=4, pady=0, padx=20, sticky='n')

        self.progress_bar = customtkinter.CTkProgressBar(master=self, orientation='horizontal', mode='determinate')
        self.progress_bar.grid(row=8, columnspan=4, pady=10, padx=20, sticky="sew")
        self.progress_bar.set(0)

        self.button_download = customtkinter.CTkButton(self, text="Baixar | Fazer Download", command=self.command_download)
        self.button_download.grid(row=9, columnspan=4, padx=10, pady=10, sticky="sew")
    
    def open_directory_save(self):
        directory = tk_filedialog.askdirectory(initialdir=self.path_download, mustexist=True)
        self.variable_path_download.set(value=directory)

        if not directory:
            self.variable_path_download.set(value=self.path_download)
        
    def load_thumbnail(self, url):
        u = requests.get(url)
        image_open = Image.open(io.BytesIO(u.content))
        return customtkinter.CTkImage(image_open, size=(200, 200))
    
    def on_progress(self, stream=None, chunk=None, bytes_remaining=None):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining

        percentage_of_completion = bytes_downloaded / total_size * 100
        per = str(int(percentage_of_completion))
        
        self.text_progress_bar.configure(text=per + '%')
        self.text_progress_bar.update()
        
        self.progress_bar.set(float(percentage_of_completion) / 100)

    def command_download(self):
        entry_text, option_selected, path_download = self.entry_bar_url.get(), self.option_selected.get(), self.entry_path_download.get()

        if len(entry_text) > 0:
            try:
                video = Baixar_Youtube(entry_text, path_download, option_selected)

                if option_selected != "playlist":
                    self.download_thread_video(video)

                else:
                    self.download_thread_playlist(video)

            except Exception as e:
                self.title_video.configure(text=f"Ocorreu um erro:\n{e}", text_color="red")
        else:
            self.title_video.configure(text=f"Insira uma URL!", text_color="red", font=('Helvatical bold',20))

    def download_thread_video(self, video):
        threading.Thread(target=self.download_video, args=(video,)).start()

    def download_thread_playlist(self, playlist):
        playlist_threading = threading.Thread(target=self.download_video_playlist, args=(playlist,))
        playlist_threading.start()

        if not playlist_threading.is_alive(): print("Download finalizado!")

    def download_video(self, video):
        video._video.register_on_progress_callback(self.on_progress)
        self.title_video.configure(text=video.title, text_color="white")

        video_thumbnail = self.load_thumbnail(video.thumbnail)
        self.image_video.configure(image=video_thumbnail)

        video.download()

    def download_video_playlist(self, playlist):
        path_download = self.entry_path_download.get()

        try:
            self.title_video.configure(text=playlist.title, text_color="white")

            videos = playlist._playlist.videos
            for idx, video in enumerate(videos):
                self.text_progress_bar.configure(text="0%")
                self.progress_bar.set(0)

                self.descrition_video.configure(text=f"[ {idx + 1} de {len(videos) + 1} ]\n{video.title}")
                video_thumbnail = self.load_thumbnail(video.thumbnail_url)
                self.image_video.configure(image=video_thumbnail)
                
                video.register_on_progress_callback(self.on_progress)
                video = video.streams.filter(only_audio=True).first()

                download_file = video.download(path_download)
                playlist.transform_mp3(download_file)

        except Exception as e:
            self.title_video.configure(text=f"Ocorreu um erro:\n{e}", text_color="red")
