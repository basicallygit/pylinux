import os
from hashlib import md5
from getpass import getuser
import subprocess
import random
from time import sleep
import shutil
from socket import gethostname
userisroot=False
homefolder=os.getcwd()
rootpasspath=os.path.join("C:\\Users\\{0}".format(getuser()),"root.txt")
if not os.path.isfile(rootpasspath):
    sudohash=input("Enter a sudo Password:\n> ")
    sudohashpswd=md5(sudohash.encode())
    sudohashpswd=sudohashpswd.hexdigest()
    with open(rootpasspath, "w") as x:
        x.write(sudohashpswd)
def checkuser():
    if userisroot:
        return "root"
    else:
        return getuser()
def checkroot():
    if userisroot:
        return "#"
    else:
        return "$"
def ls():
    try:
        cwd=os.getcwd()
        for file in os.listdir(cwd):
            print(file)
    except:
        print("Error listing files")
def whoami():
    print(checkuser())
def neofetch():
    print("""
--neofetch here--                               
""".format(checkuser()))
def ifconfig():
    print(subprocess.check_output("ipconfig" ).decode('utf-8'))
def cd(path):
    if path=="..":
        try:
            os.chdir("..")
        except:
            pass
    elif path=="~":
        os.chdir(homefolder)
    else:
        try:
            os.chdir(path)
        except:
            try:
                cwd=os.getcwd()
                fullpath=os.path.join(cwd, path)
                os.chdir(fullpath)
            except:
                print("Could not change to directory: ", path)
def cat(file):
    try:
        with open(file, "r") as f:
            content=f.read()
        print(content)
    except:
        try:
            with open(os.path.join(os.getcwd(), file), "r") as f:
                content=f.read()
            print(content)
        except:
            print("File not found / cannot open file")
def mkdir(directory):
    try:
        os.mkdir(os.path.join(os.getcwd(), directory))
    except:
        print("Could not make directory: ", directory)
def touch(touchfile):
    try:
        if not os.path.isfile(os.path.join(os.getcwd(), touchfile)):
            touchfilemake=open(touchfile, "w+")
            touchfilemake.close()
        else:
            print("File exists")
    except:
        print("Could not touch file: ", touchfile)
cmdusage={
    "cd": "Usage: cd [.. / full directory path / relative path]",
    "cat": "Usage: cat [fullpath / relative file]",
    "mkdir": "Usage: mkdir [directory name]",
    "touch": "Usage: touch [full filepath / relative filepath]",
    "sudo": "Usage: sudo [second command to run as sudo]",
    "su": "Usage: su [username / root]",
    "echo": "Usage: echo [text] (or echo [text] >> [filename])",
    "./": "Usage: ./[.sh file name]",
    "mv": "Usage: mv (move) [source file] [destination]",
    "export": "Usage: export (-v to show all exports)",
    "rm": "Usage: rm [-f for file -d for directory] [file/dir name] (sudo / root required)",
    "man": "Usage: man [command name]",
    "passwd": "Usage: passwd (change sudo password) (sudo / root required)",
    "root": "Usage: root (become root) (sudo required)",
    "ls": "Usage: ls (lists all files and directories in cwd)",
    "whoami": "Usage: whoami (shows username)",
    "neofetch": "Usage: neofetch",
    "ifconfig": "Usage: ifconfig (brings up internet / ip info)"
}
def man(cmdname):
    print(cmdusage[cmdname])
def sudo(sudocommand):
    c = open(rootpasspath)
    correctsudo = c.read()
    c.close()
    inputpasswd=input("[sudo] password for {0}: ".format(checkuser()))
    inputpasswdhash=md5(inputpasswd.encode())
    inputpasswdhash=inputpasswdhash.hexdigest()
    sudoparams=sudocommand.split(" ", 1)[-1]
    sudocommand=sudocommand.split()[0]
    if inputpasswdhash == correctsudo:
        if sudocommand in args:
            try:
                args[sudocommand](sudoparams)
            except:
                print("Expected parameters")
        elif sudocommand in noargs:
            noargs[sudocommand]()
        elif sudocommand in sudoneeded:
            if sudocommand != "rm":
                sudoneeded[sudocommand]()
            else:
                sudoneeded[sudocommand](sudoparams)
    else:
        print("Incorrect sudo passwd")
def rm(rmparams):
    rmtype=rmparams.split()[0]
    if rmtype == "-f":
        try:
            cwd=os.getcwd()
            rmpath=os.path.join(cwd, rmparams.split(" ", 1)[-1])
            os.remove(rmpath)
        except:
            print("Cannot find / remove file: ", rmparams.split(" ",1 )[-1])
    elif rmtype == "-d":
        try:
            if "y" in input("Are you sure? [Y/n]: ").lower():
                cwd=os.getcwd()
                dirpath=os.path.join(cwd, rmparams.split(" ", 1)[-1])
                os.rmdir(dirpath)
                print("Removed directory:", rmparams.split(" ", 1)[-1])
        except:
            print("Cannot find / remove directory: ", rmparams.split(" ", 1)[-1])
    else:
        print("Unknown file/directory type")
def toroot():
    global userisroot
    userisroot=True
def passwd():
    try:
        newpasswd=input("Enter new sudo password: ")
        newpasswdhash=md5(newpasswd.encode())
        newpasswdhash=newpasswdhash.hexdigest()
        with open(rootpasspath, "w") as newpass:
            newpass.write(newpasswdhash)
        print("Successfully changed sudo password.")
    except:
        print("Could not change sudo password")
def su(user):
    global userisroot
    if user == checkuser():
        print("You are already logged in as:", checkuser())
    else:
        if user == getuser():
            userisroot=False
        elif user == "root":
            sudo("root")
def python3(pythonargs):
    if pythonargs == "term":
        print("Python3 terminal:")
        while True:
            python3cmd = input(">>> ")
            if python3cmd == "exit()":
                break
            else:
                try:
                    exec(python3cmd)
                except Exception as error:
                    print(error)
    elif os.path.isfile(os.path.join(os.getcwd(), pythonargs)) or os.path.isfile(pythonargs):
        if pythonargs.endswith(".py") or pythonargs.endswith(".txt"):
            with open(pythonargs, "r") as pythonfile:
                try:
                    exec(pythonfile.read())
                except Exception as error:
                    print(error)
        else:
            print("File could not be executed from .py or .txt")
    else:
        try:
            exec(pythonargs)
        except Exception as error:
            print(error)
def currentpath():
    cwd=os.getcwd()
    if cwd==homefolder:
        return "~"
    elif cwd.startswith(homefolder):
        return "~"+cwd.replace(homefolder,"").replace("\\","/").replace(":","")
    else:
        return cwd.replace("\\","/").replace(":","")
def pwd():
    print(os.getcwd().replace("\\","/").replace(":",""))
def echo(args):
    if " >> " not in args:
        print(args)
    else:
        filename = args.split(" >> ")[1]
        towrite = args.split(" >> ")[0]
        if os.path.isfile(os.path.join(os.getcwd(), filename)):
            if "y" in input("File already exists, are you sure you want to overwrite it? [Y/n]: ").lower():
                with open(os.path.join(os.getcwd(), filename), "w+") as echofile:
                    echofile.write(towrite)
        else:
            with open(os.path.join(os.getcwd(), filename), "w+") as echofile:
                echofile.write(towrite)
def runshellfile(shellfile):
    if not shellfile.endswith(".sh"):
        print("File is not a shell file, shell file extensions are .sh")
        return
    if os.path.isfile(os.path.join(os.getcwd(), shellfile)):
        file=open(os.path.join(os.getcwd(), shellfile))
        content=file.read()
        file.close()
        if content == "":
            print("Empty shell file")
        else:
            for command in content.split("\n"):
                docommand(command)
    else:
        print("File not found in pwd")
def move(fileargs):
    source=fileargs.split(" ", 1)[0]
    destination=fileargs.split(" ", 1)[1]
    cwd=os.getcwd()
    try:
        shutil.move(source, destination)
    except:
        try:
            shutil.move(os.path.join(cwd, source), os.path.join(cwd, destination))
        except:
            print("Error moving file")
def reboot():
    os.system("shutdown -r -t 0")
def shutdown():
    os.system("shutdown -s -t 0")
def hostname():
    print(gethostname())
args={
    "cd": cd,
    "cat": cat,
    "mkdir": mkdir,
    "touch": touch,
    "man": man,
    "sudo": sudo,
    "su": su,
    "python3": python3,
    "echo": echo,
    "runshell": runshellfile,
    "mv": move
}
noargs={
    "ls": ls,
    "whoami": whoami,
    "neofetch": neofetch,
    "ifconfig": ifconfig,
    "pwd": pwd,
    "reboot": reboot,
    "shutdown": shutdown,
    "hostname": hostname
}
sudoneeded={
    "rm": rm,
    "passwd": passwd,
    "root": toroot
}
def docommand(commandin):
    try:
        if commandin.startswith("./"):
            command="runshell"
            params=commandin[2:]
        else:
            command=commandin.split(" ", 1)[0]
            params=commandin.split(" ", 1)[-1]

        if commandin == "":
            pass
        else:
            if command in args:
                if params == "":
                    print("Expected parameters")
                else:
                    args[command](params)
            elif command in noargs:
                noargs[command]()
            elif command in sudoneeded:
                if userisroot:
                    try:
                        if command == "root":
                            print("You are already root")
                        else:
                            if params == "":
                                print("Expected parameters")
                            else:
                                sudoneeded[command](params)
                    except:
                        print("Error running command")
                else:
                    print("Sudo privilages needed")
            elif command not in noargs or args or sudoneeded:
                print("{0} is not a recognized command".format(command))
            if commandin == "clear":
                os.system("cls")
    except:
        pass
while True:
    cmd=input("{0}@shell:{1}{2} ".format(checkuser(), currentpath(), checkroot()))
    if cmd=="exit":break
    if " && " not in cmd:
        docommand(cmd)
    else:
        for command in cmd.split(" && "):
            docommand(command)
