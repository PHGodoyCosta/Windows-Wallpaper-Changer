import ctypes
import os
import requests
from uuid import uuid4
import json
from pathlib import Path

class WallPaperChanger:
    def __init__(self):
        self.pathImagens = str(Path.home() / "OneDrive" / "Documentos" / "Wallpapers" / "Imagens")
        self.logPath = str(Path.home() / "OneDrive" / "Documentos" / "Wallpapers" / "log.json")
        #self.pathImagens = str(Path.home() / "Documents" / "Wallpapers" / "Imagens")
        #self.logPath = str(Path.home() / "Documents" / "Wallpapers" / "log.json")
        #self.logPath = Path.home() / "Documents" / "projeto marcos" / "log.json"

    def getLog(self):
        if not os.path.isfile(self.logPath):
            with open(self.logPath, "w+") as f:
                f.write(json.loads('''{"actualWallpaper": ""}'''))

        log = open(self.logPath, "r+").read()
        logObj = json.loads(log)
        if logObj["actualWallpaper"]:
            return logObj["actualWallpaper"]
        return False
    
    def saveLog(self, image):
        log = {
            "actualWallpaper": image
        }

        with open(self.logPath, "w+") as f:
            f.write(json.dumps(log))
    
    def fix_directories(self):
        if not os.path.isdir(self.pathImagens):
            os.mkdir(self.pathImagens)
            req = requests.get("https://i.pinimg.com/736x/a4/2c/42/a42c42ed4b96fa2ad9ebe799d8093c01.jpg") #https://i.pinimg.com/736x/fa/b4/e0/fab4e0169aaae09348c3132b84df74ef.jpg
            with open(str(os.path.join(self.pathImagens, "0.jpg")), "wb") as f:
                f.write(req.content)

        if not os.path.isfile(self.logPath):
            with open(self.logPath, "w") as f:
                json.dump({
                    "actualWallpaper": "0.jpg"
                }, f)
    def clean_names(self):
        arquivos = os.listdir(self.pathImagens)
        for i in range(0, len(arquivos)):
            arquivo = arquivos[i]
            extension = arquivo.split(".")[len(arquivo.split(".")) - 1]
            os.rename(str(os.path.join(self.pathImagens, arquivo)), str(os.path.join(self.pathImagens, f"{str(uuid4())}.{extension}")))
    
    def fix_image_order(self):
        self.clean_names()
        arquivos = os.listdir(self.pathImagens)
        for i in range(0, len(arquivos)):
            arquivo = arquivos[i]
            extension = arquivo.split(".")[len(arquivo.split(".")) - 1]
            os.rename(str(os.path.join(self.pathImagens, arquivo)), str(os.path.join(self.pathImagens, f"{i}.{extension}")))
    
    def try_correct_order(self):
        arquivos = os.listdir(self.pathImagens)
        names_in_numbers = []

        for arquivo in arquivos:
            name = arquivo.split(".")[0]
            if name.isnumeric():
                names_in_numbers.append(int(name))

        for i in range(0, len(arquivos)):
            arquivo = arquivos[i]
            name = arquivo.split(".")[0]
            if not name.isnumeric():
                return False
            
            name = int(name)
            if not i in names_in_numbers:
                return False
        return True

    def fix_image_directory(self):
        arquivos = os.listdir(self.pathImagens)
        biggest = self.getBiggestNumber()
        #print(arquivos)
        #print(biggest)

        # if biggest > 0:
        count = biggest
        for arquivo in arquivos:
            name = arquivo.split(".")[0]
            extension = arquivo.split(".")[len(arquivo.split(".")) - 1]
            if not name.isnumeric():
                os.rename(str(os.path.join(self.pathImagens, arquivo)), str(os.path.join(self.pathImagens, f"{count + 1}.{extension}")))
                count += 1

    def getBiggestNumber(self):
        arquivos = os.listdir(self.pathImagens)
        numerics = []
        for arquivo in arquivos:
            name = arquivo.split(".")[0]
            if name.isnumeric():
                numerics.append(int(name))
        
        if numerics:
            return max(numerics)
        return -1
    
    def get_images_list(self):
        arquivos = os.listdir(self.pathImagens)
        return arquivos
    
    def get_number_list(self):
        list = self.get_images_list()
        number_list = []
        for i in list:
            number_list.append(self.convert_image_in_number(i))
        return number_list
    
    def convert_image_in_number(self, image):
        num = str(image).split(".")[0]
        return int(num)

    def mudar_papel_de_parede(self, caminho_imagem):
        path = str(os.path.join(self.pathImagens, caminho_imagem))
        print(f"Mudando papel de parede: {path}")

        ctypes.windll.user32.SystemParametersInfoW(20, 0, str(path), 3)


if __name__ == "__main__":
    starter = WallPaperChanger()
    print(starter.try_correct_order())
    if not starter.try_correct_order():
        starter.fix_image_order()
    starter.fix_directories()
    # starter.fix_image_directory()
    biggest = starter.getBiggestNumber()
    print(biggest)
    list_of_images = starter.get_images_list()
    number_list = starter.get_number_list()
    actual_image = starter.getLog()
    actual_number_image = starter.convert_image_in_number(actual_image)
    if actual_number_image + 1 in number_list:
        print("Proximo")
        file = list_of_images[number_list.index(actual_number_image + 1)]
    else:
        print("volta 0")
        file = list_of_images[0]

    starter.mudar_papel_de_parede(file)
    starter.saveLog(file)
