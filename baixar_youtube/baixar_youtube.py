from pytube import YouTube, Playlist, exceptions as PytubeExceptions
import os

class ExceptionNotFoundMethod(Exception):
	pass

class Baixar_Youtube:
	def __init__(self, url, destination, method):
		self.url = url
		self.destination = destination
		self.method = method

		self._video = None
		self._playlist = None

		self.methods = {
			"mp3": self.mp3, 
			"mp4": self.mp4, 
			"playlist": self.playlist}
		
		if method in self.methods:
			metodo = self.methods[method]
			self.resultado = metodo()
		else:
			raise ExceptionNotFoundMethod("Método não encontrado!")
		
	@property
	def title(self):
		if self.method == "mp3" or self.method == "mp4":
			return self._video.title
		return self._playlist.title
	
	@property
	def thumbnail(self):
		if self.method == "mp3" or self.method == "mp4":
			return self._video.thumbnail_url

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
			self._video = YouTube(self.url)

		except PytubeExceptions.RegexMatchError:
			raise Exception(f"Erro no formato da URL:\n{self.url}")
		
		except PytubeExceptions.ExtractError:
			raise Exception(f"Um erro de Extração ocorreu com o vídeo:\n{self.url}")
		
		except PytubeExceptions.VideoUnavailable:
			raise Exception(f"O Vídeo está indisponível:\n{self.url}")
		
		except Exception as e:
			raise Exception(e)
		
			
	def playlist(self):
		try:
			self._playlist = Playlist(self.url)
		except Exception as e:
			raise Exception(e)
		
		except KeyboardInterrupt:
			print("\nSaindo...")

	def download(self):
		if self.method == "mp3":
			print(f"Download Iniciado: {self.title}")

			downloaded_file = self._video.streams.filter(only_audio=True).first().download(self.destination)
			video_title = self.transform_mp3(downloaded_file)

			print(f"Baixado {video_title} com sucesso em {self.destination}") 
		
		elif self.method == "mp4":
			video = self._video.streams.get_highest_resolution()
			video.download(self.destination)
			
			print(f"Baixado {self._video.title} com sucesso em {self.destination}") 


# import os

# url = input("Digite uma URL: ")

# video = Baixar_Youtube(url, os.getcwd(), "playlist")
# print(video.title)
# print(video.thumbnail)