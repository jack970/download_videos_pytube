from pytube import YouTube, Playlist, exceptions as PytubeExceptions
from yt_dlp import YoutubeDL
import os

class Baixar_Youtube:
	def __init__(self, url, destination, method, progress_hook):
		self.url = url
		self.destination = destination
		self.method = method
		self.progress_hook = progress_hook

		self._video = None
		self._playlist = None

		self.methods = {
			"mp3": self.mp3, 
			"mp4": self.mp4,
			"playlist": self.playlist
		}

		self.ydl_options = {
			'quiet': True,
			'progress_hooks': [self.progress_hook],
			'noprogress': True,
			'outtmpl': os.path.join(self.destination, '%(title)s.%(ext)s'),  # Specify the download path
		}
		
		if method in self.methods:
			metodo = self.methods[method]
			self.resultado = metodo()
		else:
			raise Exception("Método não encontrado!")
		
	@property
	def title(self):
		try:
			if self._video and self.method == "mp3":
				return self._video.title
			
			elif self._video and self.method == "mp4":
				info = self.mp4_info()
				if info:
					return info.get("title")
					
			elif self._playlist:
				return self._playlist.title
		
		except Exception as e:
			raise Exception(e)
	
	@property
	def thumbnail(self):
		if self._video and self.method == "mp3":
			return self._video.thumbnail_url
		
		elif self._video and self.method == "mp4":
			info = self.mp4_info()
			if info:
				return info.get("thumbnail")

	def transform_mp3(self, downloaded_file):
		base, ext = os.path.splitext(downloaded_file)
		new_file = base + '.mp3'
		os.rename(downloaded_file, new_file)		
		return new_file.split('/')[-1]
	
	def mp3(self):
		try:
			self._video = YouTube(self.url)
		
		except PytubeExceptions.RegexMatchError:
			raise Exception(f"Erro no formato da URL:\n{self.url}")
		
		except PytubeExceptions.ExtractError:
			raise Exception(f"Um erro de Extração ocorreu com o vídeo:\n{self.url}")
		
		except PytubeExceptions.VideoUnavailable:
			raise Exception(f"O Vídeo está indisponível:\n{self.url}")
		
		except Exception as e:
			raise Exception(e)
		
	def mp4(self):
		try:
			self._video = YoutubeDL(self.ydl_options)

		except Exception as e:
			raise Exception(f"Ocorreu um erro {e}")
		
	def mp4_info(self):
		if self._video:
			return self._video.extract_info(self.url, download=False)
			
	def playlist(self):
		try:
			self._playlist = Playlist(self.url)
			
		except Exception as e:
			raise Exception(e)

	def download(self):
		if self._video:
			if self.method == "mp3":
				print(f"Download Iniciado: {self.title}")

				video = self._video.streams.filter(only_audio=True).first()

				if video:
					video_downloaded = video.download(self.destination)
					video_title = self.transform_mp3(video_downloaded)
					print(f"Baixado {video_title} com sucesso em {self.destination}") 


# import os

# url = input("Digite uma URL: ")

# video = Baixar_Youtube(url, os.getcwd(), "mp3")
# print(video.title)