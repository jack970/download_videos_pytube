from pytube import YouTube, Playlist
from pytube.cli import on_progress
import os

class ExceptionNotFoundMethod(Exception):
	pass

class Baixar_Youtube:
	def __init__(self, url, destination, method):
		self.url = url
		self.destination = destination

		self.methods = {
			"mp3": self.download_mp3, 
			"mp4": self.download_mp4, 
			"playlist": self.download_playlist}
		
		if method in self.methods:
			metodo = self.methods[method]
			self.resultado = metodo()
		else:
			raise ExceptionNotFoundMethod("Método não encontrado!")

	def transform_mp3(self, downloaded_file):
		base, ext = os.path.splitext(downloaded_file)
		new_file = base + '.mp3'
		os.rename(downloaded_file, new_file)		
		return new_file.split('/')[-1]
	
	def download_mp3(self):
		try:
			video = YouTube(self.url, on_progress_callback=on_progress).streams.filter(only_audio=True).first()
			
			print(f"Download Iniciado: {video.title}")

			downloaded_file = video.download(self.destination)
			video_title = self.transform_mp3(downloaded_file)
			

			print(f"Baixado {video_title} com sucesso em {self.destination}") 
		except Exception as e:
			print("Ocorreu algum erro:", e)
		else:
			print("\n====== Done - Check Download Dir =======")
					
	def download_mp4(self):
		try:
			video = YouTube(self.url, on_progress_callback=on_progress).streams.get_highest_resolution()
			video.download(self.destination)
			
			print(f"Baixado {video.title} com sucesso em {self.destination}") 
		except Exception as e:
			print("Ocorreu algum erro:", e)
		else:
			print("\n====== Done - Check Download Dir =======")
			
	def download_playlist(self):
		try:
			playlist = Playlist(self.url)
			print(f"Playlist: {playlist.title}")

			for idx, video in enumerate(playlist.videos):
				video.register_on_progress_callback(on_progress)
				stream = video.streams.filter(only_audio=True).first()

				print(f"[{idx + 1}|{len(playlist.videos) + 1} VIDEO] {stream.title}")
				download_file = stream.download(self.destination)

				video_title = self.transform_mp3(download_file)
				print(f"Baixado {video_title} com sucesso em {self.destination}") 

		except Exception as e:
			print("Ocorreu algum erro:", e)	
			
		except KeyboardInterrupt:
			print("\nSaindo...")
		else:
			print(f"finalizado")
