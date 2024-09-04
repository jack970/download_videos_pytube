import os
import platform
import urllib.request
import shutil
import patoolib
import subprocess

relative_path = os.path.join('..', os.getcwd())
diretorio_temp = os.path.join(relative_path, 'temp')
# Função para baixar o binário do FFmpeg
def download_ffmpeg():
    # Definir URLs de download para diferentes sistemas operacionais
    urls = {
        'Windows': 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-full.7z',
        'Linux': 'https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-i686-static.tar.xz',
        'Darwin': 'https://evermeet.cx/ffmpeg/ffmpeg-5.1.2.zip'
    }
    
    # Determinar o sistema operacional
    system = platform.system()
    if system not in urls:
        raise Exception("Sistema operacional não suportado")
    
    url = urls[system]
    
    # Nome do arquivo temporário e do diretório binário
    file_name = url.split('/')[-1]
    bin_dir = 'bin'

    # Crie um diretório temporário para a extração
    os.makedirs(diretorio_temp, exist_ok=True)

    # Fazer o download do binário
    print(f"Baixando FFmpeg para {system}...")
    compressed_filepath = os.path.join(diretorio_temp, file_name)
    urllib.request.urlretrieve(url, compressed_filepath)
    
    # Extrair o arquivo baixado
    print("Extraindo arquivos...")
    if system == 'Windows':
        instala_7zip_windows()
        # Windows usa 7z, então o arquivo é um .7z
        patoolib.extract_archive(compressed_filepath, outdir=diretorio_temp)
    
    caminho_arquivo_especifico = os.listdir(diretorio_temp)
    if (len(caminho_arquivo_especifico) > 0):
        relative_path_unzip = os.path.join(diretorio_temp, caminho_arquivo_especifico[0], bin_dir)
        shutil.move(relative_path_unzip, os.path.join(relative_path))

    # Limpar arquivos temporários
    shutil.rmtree(diretorio_temp)
    print("FFmpeg baixado e extraído com sucesso!")

def executar_comando(comando):
    try:
        resultado = subprocess.run(comando, check=True, text=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print("Erro ao executar o comando:")
        print(e.stderr)

def instala_7zip_windows():
    caminhos_possiveis = [
        r'C:\Program Files\7-Zip\7z.exe',
        r'C:\Program Files (x86)\7-Zip\7z.exe'
    ]
    
    for caminho in caminhos_possiveis:
        if os.path.isfile(caminho):
            print(f'7-Zip encontrado em {caminho}')
            return True
        
    comando_winget = ['winget', 'install', '-e', '--id', '7zip.7zip'] # Comando para instalar o 7-Zip usando winget
    executar_comando(comando_winget) # Executar o comando

# Verificar se o binário já existe
if not os.path.isfile(os.path.join('bin', 'ffmpeg.exe')):
    download_ffmpeg()
else:
    print("O binário do FFmpeg já está presente na pasta 'bin'.")
