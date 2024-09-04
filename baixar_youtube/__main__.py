from yt_dlp import YoutubeDL
from functions import LOCATION_FFMPEG
import os

class Baixar_Youtube:
	def __init__(self, url, destination, method, progress_hook=None):
		self.url = url
		self.destination = destination
		self.method = method
		self.codec = self.method
		self.progress_hook = progress_hook

		self._video = None
		self._playlist = None

		if method not in ["mp3", "mp4", "playlist"]:
			raise ValueError("Formato Inválido!")
			
		self.set_video()

		
	@property
	def title(self):
		try:
			if self._video:
				info = self.video_info()
				if info:
					return info.get("title")
					
			elif self._playlist:
				return self._playlist.title
		
		except Exception as e:
			raise Exception(e)
	
	@property
	def thumbnail(self):
		info = self.video_info()
		if info:
			return info.get("thumbnail")
		
	@property
	def listar_formatos(self):
		info = self.video_info()
		if info:
			return info.get("formats", [])
			
	def _load_default_options(self, codec='mp3'):
		if (codec == 'mp3'):
			formato = 'bestaudio'
			out = f'%(title)s.mp3'
		else:
			formato = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]'
			out = f'%(title)s.%(ext)s'

		return {
			'format': formato,
			'extract_audio': True,
			'ffmpeg_location': LOCATION_FFMPEG,
			'progress_hooks': [self.progress_hook],
			'noprogress': True,
			'outtmpl': os.path.join(self.destination, out),  # Specify the download path
			'quiet': True
		}

	def set_video(self):
		try:
			load_default_options = self._load_default_options(codec=self.codec)
			self._video = YoutubeDL(load_default_options)

		except Exception as e:
			raise Exception(f"Ocorreu um erro {e}")
		
	def video_info(self):
		if self._video:
			return self._video.extract_info(self.url, download=False)

	def download(self):
		if self._video:
			print(f"Download Iniciado: {self.title}")
			self._video.download([self.url])
	


# import os

# url = input("Digite uma URL: ")

# video = Baixar_Youtube(url, os.getcwd(), "playlist")
# print(video.get_info_playlist())
# formats = video.listar_formatos 
# for f in formats:
# 	format_id = f.get('format_id', 'N/A')
# 	format_note = f.get('format_note', 'N/A')
# 	ext = f.get('ext', 'N/A')
# 	resolution = f.get('resolution', 'N/A')
# 	print(f"Format ID: {format_id}, Note: {format_note}, Extension: {ext}, Resolution: {resolution}")

# path = os.path.join('..', os.getcwd(), "ffmpeg.exe")
# print(path)