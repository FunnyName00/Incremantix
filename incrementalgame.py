import tkinter as tk
from tkinter import Toplevel, ttk


# Initialiser la variable
score = 0
clic_progress = 0
clics = 1
clics_objective = 10
progress_value = 0

generators = 0
cost_generator = 10
generator_reward = 1
generator_rate = 0

supergenerators = 0
cost_supergenerator = 5000
supergenerator_reward = 100
supergenerator_rate = 0




def format_nombre(n):
    return f"{n:,}".replace(",", ".")

def maj_affichage():
    global score, cost_generator, cost_supergenerator
    if score < cost_generator:
        bouton_buy.config(bg='grey')
    else:
        bouton_buy.config(bg='SystemButtonFace')

    if score < cost_supergenerator:
        bouton_buy_super.config(bg='grey')
    else:
        bouton_buy_super.config(bg='SystemButtonFace')
    

    label_score.config(text=f"Points : {format_nombre(score)} \n Auto rate : {int(generator_rate+supergenerator_rate)}/s")
    bouton.config(text=f"+ {clics}")

    
    label_generators.config(text=f'Generator number : {format_nombre(generators)} \n Rate : {int(generator_rate)}/s')  
    label_cost_generator.config(text=f'Cost of generator : {format_nombre(cost_generator)}')
    
    label_supergenerators.config(text=f'Super generator number : {format_nombre(supergenerators)} \n Rate : {int(supergenerator_rate)}/s')
    label_cost_supergenerator.config(text=f'Cost of super generator : {format_nombre(cost_supergenerator)}')




def incrementer():
    global score, clic_progress, clics, clics_objective, progress_value
    score += clics

    clic_progress += 1
    progress_value = int((clic_progress/clics_objective) * 100)
    
    if progress_value >= 100:
        if clics < 100 and 2:
            clics = int(clics*2)
        if clics == 1:
            clics += 1

        if clics >= 100:
            clics +=10 
        clic_progress = 0
        progress_value = 0
        clics_objective = int(clics_objective*1.2) 
        #print(clics, ":",clics_objective)

    clic_progression['value'] = progress_value
    maj_affichage()


def buy_generator():
    global score, generators, cost_generator
    if score >= cost_generator:
        score -= cost_generator
        generators +=1 
        cost_generator = int(cost_generator*1.5)
        maj_affichage()


    
def generator():
    global score, generators, generator_reward, generator_rate
    score += generators*generator_reward

    maj_affichage()
    generator_rate = (generators/(1/(generators+1)))
    root.after(int(1000/(generators+1)), generator)



def buy_supergenerator():
    global score, supergenerators, cost_supergenerator
    if score >= cost_supergenerator:
        score -= cost_supergenerator
        supergenerators +=1 
        cost_supergenerator = int(cost_supergenerator*1.5)
        maj_affichage()

def supergenerator():
    global score, supergenerator_reward, supergenerators, supergenerator_rate
    score += supergenerators*supergenerator_reward

    maj_affichage()
    supergenerator_rate = (supergenerators*supergenerator_reward/(1/(supergenerators+1)))
    root.after(int(1000/(supergenerators+1)), supergenerator)


def save():
    global score, generators, cost_generator, supergenerators, cost_supergenerator, clic_progress, clics, clics_objective, progress_value
    with open("save.txt", "w") as file:
        file.write(f'{score} {generators} {cost_generator} {supergenerators} {cost_supergenerator} {clic_progress} {clics} {clics_objective} {progress_value}')
        winsaved = Toplevel(root, height=50, width= 50)
        label_saved = tk.Label(winsaved, text='Game saved', font=('Arial', 16))
        label_saved.pack(pady=20)
        

def load():
    global score, generators, cost_generator, supergenerators, cost_supergenerator, clic_progress, clics, clics_objective, progress_value
    with open("save.txt", "r") as file:
        
        txt = file.read()
        txt = txt.split()
        score = int(txt[0])
        generators = int(txt[1])
        cost_generator = int(txt [2])
        supergenerators = int(txt[3])
        cost_supergenerator = int(txt[4])
        clic_progress = int(txt[5])
        clics = int(txt[6])
        clics_objective = int(txt[7])
        progress_value = int(txt[8])
    winloaded = Toplevel(root, height=50, width= 50)
    label_loaded = tk.Label(winloaded, text='Game loaded', font=('Arial', 16))
    label_loaded.pack(pady=20)






# Créer la fenêtre principale
root = tk.Tk()
root.title("Incremental Game")
root.config(background=("ghost white"))

#WIDGETS
label_score = tk.Label(root, text=f'Points : {format_nombre(score)}', font=('Arial', 16))
label_score.pack(pady=20)

bouton = tk.Button(root, text=f"+ {clics}", command=incrementer, font=("Arial", 14))
bouton.pack(pady=10)


clic_progression = ttk.Progressbar(root, orient="horizontal", length=100, mode="determinate")
clic_progression.pack(pady=5)

label_generators = tk.Label(root, text=f'Generator number : {format_nombre(generators)} \n Rate : {generators} / {(1.5/(generators+1))}s', font=('Arial', 16))
bouton_buy = tk.Button(root, text="Buy a generator", command= buy_generator, font=('Arial',14))
label_cost_generator = tk.Label(root, text=f'Cost of 1 generator : {format_nombre(cost_generator)}', font=('Arial', 12))


label_generators.pack(pady=10)
bouton_buy.pack(pady=5)
label_cost_generator.pack(pady=0)

label_supergenerators = tk.Label(root, text=f'Super generator number : {format_nombre(supergenerators)}', font=('Arial', 16))
bouton_buy_super = tk.Button(root, text="Buy a super generator", command= buy_supergenerator, font=('Arial',14))
label_cost_supergenerator = tk.Label(root, text=f'Cost of 1 super generator : {format_nombre(cost_supergenerator)}', font=('Arial', 12))

label_supergenerators.pack(pady=20)
bouton_buy_super.pack(pady=5)
label_cost_supergenerator.pack(pady=0)

bouton_save = tk.Button(root, text=f'Save', command= save, font=("Arial", 14))
bouton_save.pack(pady=10)

bouton_load = tk.Button(root, text=f'Load', command= load, font=('Arial', 14))
bouton_load.pack(pady=10)



generator()
supergenerator()
# Lancer la boucle principale
root.mainloop()
