from instaloader import Instaloader, Profile
#from win10toast import ToastNotifier
#from PIL import ImageTk, Image
#from tkinter import *
import platform
import datetime
import sys, os
import requests
import time

username, password, target = "<your_ig_username>", "<your_ig_password>", "<target_ig_username>"

def check_platform():
    if os.name=="posix":
        return "/"
    elif os.name=="nt":
        return "\\"

def internet(url='http://www.google.com/', timeout=3):
    try:
        #r = requests.get(url, timeout=timeout)
        print ("Internet connection...", end="")
        r = requests.head(url, timeout=timeout)
        print ("OK!")
        return True
    except requests.ConnectionError as ex:
        print("FAIL!")
        return False

def notifier(mode, target=0):
    pass
    """
    toast = ToastNotifier()

    if mode==0:
        toast.show_toast("TRACKER", "Internet connection fault...", icon_path='config\\icon.ico',duration=5)
    elif mode==1:
        toast.show_toast("TRACKER", "Can't found this profile: " + target, icon_path='config\\icon.ico',duration=5)
    elif mode==2:
        toast.show_toast("TRACKER", "Profile Editing Detected: " + target, icon_path='config\\icon.ico',duration=5)
    """

def setup():
    try:
        print ("config...", end="")
        os.system("mkdir config")
        print ("OK!")
        print ("reports...", end="")
        os.system("mkdir config"+check_platform()+"reports")
        print ("OK!")
        print ("track.cfg...", end="")
        with open("config"+check_platform()+"track.cfg", "w") as file:
            file.write("<follows>:<followers>:<bio>:<profile_image>")
        print ("OK!")
        print ("file.cfg...", end="")
        with open("config"+check_platform()+"file.cfg", "w") as file:
            file.write("0")
        print ("OK!")
    except:
        print ("FAIL!")

def login(username, password, target):
    loader = Instaloader()
    try:
        loader.login(username, password)
    except FileNotFoundError:
        loader.context.log("Session file does not exist yet - Logging in.")
    if not loader.context.is_logged_in:
        loader.interactive_login(username)
        loader.save_session_to_file()

    try:
        profile = Profile.from_username(loader.context, target)
    except:
        notifier(1, target)
        with open("config"+check_platform()+"TARGET_ERROR.dat", "w") as file:
            sys.exit(1)
    return profile


def get_followers(profile):
    returnThis = list()
    followers = profile.get_followers()
    for follower in followers:
        if follower.username not in returnThis:
            returnThis.append(follower.username)
    returnThis.sort()
    return returnThis


def get_follows(profile):
    returnThis = list()
    follows = profile.get_followees()
    for follow in follows:
        if follow.username not in returnThis:
            returnThis.append(follow.username)
    returnThis.sort()
    return returnThis


def get_bio(profile):
    bio = profile.biography
    return bio


def download_profile_pic(profile):
    loader = Instaloader()
    loader.download_profilepic(profile, )

"""
def resize_image(root):
    image = Image.open(r"{}"+check_platform()+"{}".format(target,os.listdir(target)[-1]))
    image = image.resize((100, 100), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(image)
    Label(root, image=img).place(x=180, y=10)
"""

def report(follows, followers, bio, pp, target):
    with open(f"config{check_platform()}track.cfg", "r") as file:
        old_report = file.read()
    new_report = "{}:{}:{}:{}".format(str(len(follows)), str(len(followers)), str(bio), str(pp))

    if old_report != new_report:
        notifier(2, target)
        file1_read = None
        with open(f"config{check_platform()}file.cfg", "r") as file1:
            file1_read = file1.read()
            with open("config"+check_platform()+"reports"+check_platform()+"report({}){}.dat".format(str(int(file1_read) + 1),
                                                        str(datetime.datetime.now().day) + datetime.datetime.strftime(
                                                            datetime.datetime.now(), '%B') + str(
                                                            datetime.datetime.now().year) + "_" + datetime.datetime.now().strftime(
                                                            "%H_%M_%S")), "w") as file2:
                file2.write(
                    "Follows:" + str(follows) + "\nFollowers:" + str(followers) + "\nBio:" + str(bio) + "\nPp:" +
                    str(pp) + "\n{}".format(new_report))
        with open(f"config{check_platform()}file.cfg", "w") as file1:
            file1.write(str(int(file1_read) + 1))
        with open(f"config{check_platform()}track.cfg", "w") as file2:
            file2.write(new_report)

        #visible_panel()
"""
def passed():
    pass


def visible_panel():
    root = Tk()

    root.geometry('300x160')
    root.configure(background='#FFFFFF')
    root.title('WRSP')

    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)#----
    filemenu.add_command(label="Anahtar Al", command=passed)
    filemenu.add_separator()
    filemenu.add_command(label="Geliştiriciler", command=passed)

    menubar.add_cascade(label="Hakkında", menu=filemenu)###

    helpmenu = Menu(menubar, tearoff=0)#----
    helpmenu.add_command(label="Kullanım", command=passed)
    helpmenu.add_command(label="Güvenli mi?", command=passed)
    helpmenu.add_separator()
    helpmenu.add_command(label="İletişim", command=passed)

    menubar.add_cascade(label="Yardım", menu=helpmenu)###

    root.config(menu=menubar)

    Label(root, text='@' + target, bg='#FFFFFF', font=('arial', 12, 'normal')).place(x=10, y=10)
    Label(root, text='Takip:' + str(len(followers)), bg='#FFFFFF', font=('arial', 12, 'normal')).place(x=10, y=50)
    Label(root, text='Takipçi:' + str(len(follows)), bg='#FFFFFF', font=('arial', 12, 'normal')).place(x=10, y=90)
    #resize_image(root=root)

    #root.mainloop()
"""

if __name__ == "__main__":
    print (f"Platform...{platform.system()}")
    if len(sys.argv)!=1:
            if sys.argv[1]=="-s" or sys.argv[1]=="--setup":
                setup()
    else:
        if internet():
            print ("Profile Found...", end="")
            try:
                profile = login(username=username, password=password, target=target)
                print ("OK!")
            except:
                print ("FAIL!")
                time.sleep(1)
            followers = get_followers(profile=profile)
            follows = get_follows(profile=profile)
            bio = get_bio(profile=profile)
            download_profile_pic(profile=profile)
            print ("Report...",end="")
            try:
                report(follows=follows, followers=followers, bio=bio, pp=os.listdir(target)[-1], target=target)
                print ("OK!")
            except:
                print ("FAIL!")
                time.sleep(1)
        else:
            pass
            #notifier(0)
    time.sleep(2)
