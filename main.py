import os
from hashlib import md5
from getpass import getuser
import subprocess
import random
from time import sleep
import shutil
from socket import gethostname
from string import printable
from platform import processor, release, machine
userisroot=False
homefolder=os.getcwd()
userprofile=os.getenv("USERPROFILE")
if not os.path.isfile(userprofile+"\\root.txt"):
    with open(userprofile+"\\root.txt", "w") as f:
        f.write(md5(input("Set root password: ").encode()).hexdigest())
if not os.path.isfile(userprofile+"\\hostname.txt"):
    with open(userprofile+"\\hostname.txt", "w") as f:
        f.write(input("Your desktop's name: "))
with open(userprofile+"\\hostname.txt", "r") as f:
    _hostname=f.read()
def checkuser():
    return "root" if userisroot else getuser()
def checkroot():
    return "#" if userisroot else "$"
def ls():
    for file in os.listdir(os.getcwd()):
        print(file)
def whoami():
    print(checkuser())
def neofetch():
    print(f"""
    --Put your own neofetch ascii art here--
    {checkuser}@{_hostname}
    CPU: {processor()}, {machine}
    OS Release: (release()}
    """)
def ifconfig():
    print(subprocess.check_output("ipconfig" ).decode('utf-8'))
def cd(path):
    os.chdir(homefolder if path == "~" else path)
def cat(file):
    with open(file, "r") as f:
        print(f.read())
def mkdir(directory):
    os.mkdir(directory)
def touch(touchfile):
    if not os.path.isfile(touchfile):
        with open(touchfile, "r") as f:
            pass
    else:
        print(f"{touchfile} already exists")
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
    "ifconfig": "Usage: ifconfig (brings up internet / ip info)",
    "grep": "Usage: grep (keyword) (file)",
    "sethostname": "Usage: sethostname (new hostname)",
    "color": "Usage: change terminal color (color a",
    "colour": "Usage: change terminal colour (colour a)"
}
def man(cmdname):
    if cmdname in cmdusage:
        print(cmdusage[cmdname])
def sudo(sudocommand):
    with open(userprofile+"\\root.txt", "r") as c:
        correctsudo=c.read()
    inpasswd=md5(input(f"[sudo] password for {checkuser()}: ").encode()).hexdigest()
    sudoparams=sudocommand.split(" ", 1)[-1]
    sudocommand=sudocommand.split()[0]
    if inpasswd == correctsudo:
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
        print("Incorrect sudo password")
def rm(file):
    os.remove(file)
def toroot():
    global userisroot
    userisroot=True
def passwd():
    newpasswdhash=md5(input("New root passwd: ").encode()).hexdigest()
    with open(userprofile+"\\root.txt", "w") as newpass:
        newpass.write(newpasswdhash)
    print("Successfully changed sudo password")
def rmdir(_dir):
    if "y" in input("Are you sure? [Y/n]: ").lower():
        shutil.rmtree(_dir)
def su(user):
    global userisroot
    if user == checkuser():
        print("You are already logged in as: ", checkuser())
    else:
        if user == getuser():
            userisroot=False
        elif user == "root":
            sudo("root")
def sethostname(newname):
    with open(userprofile+"\\hostname.txt", "w") as f:
        f.write(newname)
    global _hostname
    _hostname = newname
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
    elif os.path.isfile(pythonargs):
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
        filename=args.split(" >> ")[1]
        towrite=args.split(" >> ")[0]
        if os.path.isfile(filename):
            if "y" in input("File already exists, are you sure you want to overwrite it? [Y/n]: ").lower():
                with open(os.path.join(os.getcwd(), filename), "w+") as echofile:
                    echofile.write(towrite)
        else:
            with open(filename, "w+") as echofile:
                echofile.write(towrite)
def strings(filename):
    with open(filename, "r", encoding="Latin-1") as stringfile:
        content=stringfile.read()
        for line in content.split("\n"):
            try:
                letters=""
                for letter in line:
                    if letter in printable[:-5]:
                        letters=letters+letter
                    input(letters+"\n")
            except KeyboardInterrupt:
                break
def runshellfile(shellfile):
    if not shellfile.endswith(".sh"):
        print("File is not a shell file, shell file extensions are .sh")
        return
    if os.path.isfile(shellfile):
        file=open(shellfile)
        content=file.read()
        file.close()
        if content == "":
            print("Empty shell file")
        else:
            for command in content.split("\n"):
                parsecmd(command)
    else:
        print("File not found in pwd")
def move(fileargs):
    source=fileargs.split(" ", 1)[0]
    destination=fileargs.split(" ", 1)[1]
    cwd=os.getcwd()
    shutil.move(source, destination)
def grep(grepargs):
    keyword=grepargs.split(" ", 1)[0]
    filename=grepargs.split(" ", 1)[1]
    with open(filename, "r") as grepfile:
        for line in grepfile.read().split("\n"):
            if keyword in line:
                input(line+"\n")
def color(_color):
    os.system(f"color {_color}")
def colour(_colour):
    os.system(f"color {_colour}")
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
    "mv": move,
    "strings": strings,
    "grep": grep,
    "rm": rm,
    "sethostname": sethostname,
    "color": color,
    "colour": colour
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
    "rmdir": rmdir,
    "passwd": passwd,
    "root": toroot
}
def parsecmd(commandin):
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
            if commandin == "clear":
                os.system("cls")
            elif command in args:
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
    except Exception as e:
        print(e)
while True:
    cmd=input(f"""\u250F\u2501({checkuser()}@{_hostname})-[{currentpath()}]
\u2517{checkroot()} """)
    if cmd=="exit":break
    if " && " not in cmd:
        parsecmd(cmd)
    else:
        for command in cmd.split(" && "):
            parsecmd(command)
    print()
