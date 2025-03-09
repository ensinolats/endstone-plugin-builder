import build, json, time
from argparse import ArgumentParser
from pathlib import Path
from threading import Thread
CURRENT_DIR = Path(__file__).resolve().parent
DEFAULT_DATA_DIR = Path.joinpath(CURRENT_DIR, "path.json")

def main():
    args = invokeParser()
    origin:str | None= args.get("origin")
    output_dir:str | None= args.get("destiny")
    if (output_dir): 
        data.set(output_dir)
        print(f"destiny established to {output_dir}")
    if (not origin):
        return
    origin:Path = Path(origin)
    destiny = data.get()
    if (origin.is_dir() == False):
        print("invalid proyect directory")
        return
    
    if (destiny == None):
        print("unable to find the destiny path, set it with -des")
        return
    def startBuild():
        print("building...")
        fileName:str = "noFileName"
        try:
            fileName = build.ProjectBuilder(origin).build(distribution="wheel" ,output_directory=destiny)
        except Exception as error:
            errormsg = str(error.with_traceback()).split("\n")
            if (CURRENT_DIR.joinpath("logs").is_dir() == False):
                CURRENT_DIR.mkdir("logs")
            
            logfile = generateLogFile(CURRENT_DIR.joinpath("logs"), errormsg)
            print("an error during the execution of build.ProjectBuilder has ocurred")
            print(f"more details can be found in the next log file: {logfile}")
            return
        print(f"Done.")
        print(f"file located in {fileName}")
    print("building prosses starting")
    buildProcess = Thread(target=startBuild)
    buildProcess.start()
    buildProcess.join()
    
def invokeParser() -> dict:
    parser = ArgumentParser(
        prog="builder",
        description="build your endstone programs more faster"
    )
    parser.add_argument("origin", type=str, help="your plugin folder")
    parser.add_argument("-destiny", "-des", type=str, nargs="?", help="speficies a directory to ouput files, by default uses the last input path")
    args = parser.parse_args()
    return vars(args)

    
class DestinyPathManager:
    def __init__(self, file:str = DEFAULT_DATA_DIR):
        self.dataPath = Path(file)
        self.json = {}
        if (self.dataPath.is_file()==False):
            with open(self.dataPath, "x"):
                print("file dont found! making one")
        self._load()
    def _load(self):
        with open(self.dataPath, "r+") as file:
            data:dict = {}
            try:
                data = json.load(file)
            except: pass
            self.json = data
    def set(self, path:str):
        destiny = Path(path)
        assert destiny.is_dir() == True, "must be a valid path"
        self.json["destiny_path"] = destiny.resolve().__str__()
        self._save()
    def get(self) -> Path | None:
        path = self.json.get("destiny_path")
        if (path == None): return
        return Path(self.json["destiny_path"])
    def _save(self):
        with open(self.dataPath, "w") as file:
            json.dump(self.json, file, indent=4)
def generateLogFile(destinyDir:Path, text:list[str]):
    localtime = time.localtime()
    fileId = f"{localtime.tm_year}-{localtime.tm_mon}-{localtime.tm_mday}-{localtime.tm_hour}-{localtime.tm_min}-{localtime.tm_sec}-{localtime.__hash__()}"
    ouFile = destinyDir.joinpath(f"{fileId}.log")
    with open(ouFile, "x"):
        print(f"log file generated")
    with open(ouFile, "w") as file:
        file.writelines(text)
    return ouFile
data = DestinyPathManager()
        

if (__name__ == "__main__"):
    main()