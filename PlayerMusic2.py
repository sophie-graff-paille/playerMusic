import os
import tkinter as tk
import tkinter.ttk as ttk
import fnmatch
from tkinter import *
from pygame import mixer
from tkinter import filedialog
import time
import shutil

# créer ma fenêtre
Lecteur = tk.Tk()
Lecteur.title("PlayerMusic Sophie")
Lecteur.geometry("600x610")
Lecteur.config(bg="white")

# détermine le chemin pour chercher ma musique et le format des fichiers
# dans ce lecteur, il n'ouvre que les fichiers.wav
rootpath = "musiques"
pattern = "*.wav"

mixer.init()

# récupère les infos de la durée de la chanson
def play_time():
    #temps écoulé de la chanson en cours de lecture en milliseconde
    current_time = mixer.music.get_pos() / 1000
    #temps converti au format de l'heure
    converted_current_time = time.strftime("%M:%S", time.gmtime(current_time))
    status_bar.configure(text=f"{converted_current_time}")
    #mise à jour avec after qui saisira la nouvelle position de temps à chaque seconde  
    status_bar.after(1000, play_time)

# je définis la destination avec son chemin entier
destination = "/Users/qqcoc/OneDrive/Bureau/Documents/Laplateforme/PlayerMusic/musiques/"
# ajouter des fichiers à la liste de lecture
def Addsongs(): #pour cette fonction Eli m'a aidée à comprendre les chemins ! Je n'arrivais pas à ajouter de chansons
    #il va chercher dans le fichier chansons
    song_files = filedialog.askopenfilenames(initialdir=os.path.expanduser("~/Desktop"), title="Choisissez une chanson")
    #boucle qui permet de copier la chanson choisie dans le fichier chansons
    for song_file in song_files:
        shutil.copy2(song_file, destination)
    #remet à jour la listBox
    listBox.delete(0, tk.END)
    for fichier in os.listdir(destination):

        listBox.insert(END, fichier)

# permet de choisir dans le menu la fonction supprimer un fichier. Il faut sélectionner d'abord un fichier. 
def Delsong():
    curr_song=listBox.curselection()
    listBox.delete(curr_song[0])

# fonction du bouton play
def Play():
    #permet d'afficher le label de la chanson sélectionnée
    song_name = listBox.get(listBox.curselection()[0])
    label.config(text= song_name)
    song = listBox.get(ACTIVE)
    #charge la chanson et la joue
    mixer.music.load(rootpath +"/"+ song)
    mixer.music.play(loops=0)

    #appelle la fonction play_time pour donner la longueur de la chanson
    play_time()

# arrête la lecture et remet à zéro
def Stop():
    mixer.music.stop()
    listBox.selection_clear(ACTIVE)

# détermine la chanson suivante
def Next():
    next_song = listBox.curselection()
    next_song = next_song[0]+1
    next_song_name = listBox.get(next_song)
    
    label.config(text= next_song_name)
    
    mixer.music.load(rootpath +"/"+ next_song_name)
    mixer.music.play()
    
    listBox.selection_clear(0,"end")
    listBox.activate(next_song)
    listBox.selection_set(next_song)

# détermine la chanson précédente
def Rewind():
    prec_song = listBox.curselection()
    prec_song = prec_song[0]-1
    prec_song_name = listBox.get(prec_song)
    
    label.config(text= prec_song_name)
    
    mixer.music.load(rootpath +"/"+ prec_song_name)
    mixer.music.play()
    
    listBox.selection_clear(0,"end")
    listBox.activate(prec_song)
    listBox.selection_set(prec_song)

# fonctions pause et unpause réunies dans le bouton pause
# on appuie une fois et ça met la lecture en pause
# on appuie une seconde fois et ça reprend là où la musique s'est arrêtée
def Pause():
    if ButtonPause["text"]== "pause":
        mixer.music.pause()
        ButtonPause["text"]= "play"
    else:
        mixer.music.unpause()
        ButtonPause["text"]= "pause"

# met le fichier en boucle infinie avec (-1,0,0)
# on peut choisir le nombre de fois en changeant les valeurs de cette parenthèse (1), (2), (3), etc.
# quand on appuie sur le bouton, le fichier appelé redémarre et se met en boucle
def Loop():
    mixer.music.play(-1,0,0)

# image pour mon fond avec Canvas
photo = PhotoImage(file="img/Equalizer4.png")
Canevas = Canvas(Lecteur, width=450, height=200)
item = Canevas.create_image(0,0,anchor=NW, image=photo)
Canevas.pack()

#
def Slider(x):
    slider_label.configure(text=int(my_slider.get()))

# fenêtre dans laquelle va se trouver ma liste de musiques
listBox=tk.Listbox(Lecteur, fg="cyan", bg="black", width=64, font=("Comic Sans MS", 8), selectbackground="pink", selectforeground="black")
listBox.pack(padx=40, pady=0)

# permet de changer le volume du fichier (avec un curseur)
def Volume(event):
    # donne la valeur du Scale
    mixer.music.set_volume(Buttonsound.get())

# va donner le titre de la musique en écoute
label = tk.Label(Lecteur, text="", bg="white", fg="black", font=("Comic Sans MS", 12))
label.pack(pady=15)

# bouton curseur du volume avec au départ, une mise du son que j'ai déterminé au milieu
Buttonsound = Scale(Lecteur, from_=0, to_=1.0, resolution=0.05, fg="cyan", bg="black", orient=HORIZONTAL, command=Volume)
Buttonsound.set(0.5)
Buttonsound.pack(padx=0, pady=0)

# donne la valeur 0 pour programmer le bouton mute
def Mute():
    Buttonsound.set(0)

# frame pour mettre tous les boutons les uns à côté des autres
commands = Frame(Lecteur, bg="white", width=150)
commands.pack(padx=0, pady=0, anchor="s")

# bouton mute
mute = PhotoImage(file="img/mute.png")
ButtonMute = Button(Lecteur, text="mute", command=Mute, fg="blue", bg="black", image=mute, borderwidth=0)
ButtonMute.pack(side=LEFT, in_=commands, padx=0, pady=0)

# bouton musique précédente
rewind = PhotoImage(file="img/rewind.png")
ButtonRewind = Button(Lecteur, text="précédent", command=Rewind, fg="blue", bg="black", image=rewind, borderwidth=0)
ButtonRewind.pack(side=LEFT, in_=commands, padx=0, pady=0)

# bouton stop
stop = PhotoImage(file="img/stop.png")
ButtonStop = Button(Lecteur, text="stop", command=Stop, fg="blue", bg="black", image=stop, borderwidth=0)
ButtonStop.pack(side=LEFT, in_=commands, padx=0, pady=0)

# bouton play
play = PhotoImage(file="img/play.png")
ButtonPlay = Button(Lecteur, text="play", command=Play, fg="blue", bg="black", image=play, borderwidth=0)
ButtonPlay.pack(side=LEFT, in_=commands, padx=0, pady=0)

# bouton pause
pause = PhotoImage(file="img/pause.png")
ButtonPause = Button(Lecteur, text="pause", command=Pause, fg="blue", bg="black", image=pause, borderwidth=0)
ButtonPause.pack(side=LEFT, in_=commands, padx=0, pady=0)

# bouton suivant
next = PhotoImage(file="img/next.png")
ButtonNext = Button(Lecteur, text="suivant", command=Next, fg="blue", bg="black", image=next, borderwidth=0)
ButtonNext.pack(side=LEFT, in_=commands, padx=0, pady=0)

# bouton boucle
loop = PhotoImage(file="img/boucle.png")
ButtonLoop = Button(Lecteur, text="en boucle", command=Loop, fg="blue", bg="black", image=loop, borderwidth=0)
ButtonLoop.pack(side=LEFT, in_=commands, padx=0, pady=0)

# menu pour ajouter, supprimer un fichier, et pour fermer et quitter le lecteur
mon_menu = Menu (Lecteur, tearoff=0)
Lecteur.config(menu=mon_menu)
player_menu=Menu(mon_menu)
mon_menu.add_cascade(label="Menu PlayerMusic Sophie", menu=player_menu)
player_menu.add_command(label="Ajouter une chanson à la playlist", command=Addsongs)
player_menu.add_command(label="Supprimer un fichier", command=Delsong)
player_menu.add_command(label="Fermer PlayerMusic Sophie", command=Lecteur.destroy)

# état de la barre en bas du lecteur qui affiche les secondes écoulées pendant l'écoute d'un fichier
status_bar = Label(Lecteur, text="", bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

# os permet d'intéragir avec le système d'exploitation
# fnmatch vérifie et compare un fichier avec le modèle pattern
for root, dirs, files in os.walk(rootpath):
    for filename in fnmatch.filter(files, pattern):
        listBox.insert("end", filename)

# curseur de progression/position
my_slider = ttk.Scale(Lecteur, from_=0, to_=100, orient=HORIZONTAL, value=0, command=Slider, length=460, )
my_slider.pack(pady=10)

# étiquette du curseur de progression/position
slider_label = Label(Lecteur, text=0)
slider_label.pack(pady=2)

Lecteur.mainloop()