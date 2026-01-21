import tkinter as tk
from tkinter import *

window = Tk()
window.title("Ecosystem Simulator")

window.geometry("1920x1080")
window.config(bg="#8dfc76")


# Add a label
label0 = Label(window, text="Welcome to the Ecosystem Simulator!", font=(
    "Jokerman", 50), bg="black", fg="white", border=10, relief="raised")
label0.pack(padx=50, pady=30)

label1 = Label(window, text="Do you want to use the default configuration?", font=(
    "Arial", 30), bg="white", fg="black", border=10, relief="raised")

# Add a button to start


def Start():
    button0.pack_forget()
    label1.pack(pady=30)
    for rb in radio_buttons:
        rb.pack(pady=10)


button0 = Button(window, text="Start", font=("Arial", 30))
button0.config(bg="white", fg="black", border=10, relief="groove",
               activebackground="red", activeforeground="white", command=Start)
button0.pack(padx=30, pady=200)

# Add a button to start the actual simulation
button1 = Button(window, text="Press to start the Simulation",
                 font=("Arial", 30))
button1.config(bg="white", fg="black", border=5, relief="groove",
               activebackground="red", activeforeground="white")

# Add radio buttons for user choices


def create_radiobuttons(parent, choices, variable, command):
    buttons = []
    for index, text in enumerate(choices):
        rb = Radiobutton(parent, text=text, variable=variable, value=index, font=(
            "Arial", 25), bg="white", fg="black", border=2, relief="ridge", command=command)
        buttons.append(rb)
    return buttons


x = IntVar(value=-1)

choices = ["Yes", "No"]


def select_choice():
    label1.pack_forget()
    for rb in radio_buttons:
        rb.pack_forget()

    if x.get() == 0:
        print("User selected Yes")
        # start simulation with default config
    else:
        print("User selected No")
        ask_user_inputs()


radio_buttons = create_radiobuttons(window, choices, x, select_choice)


# store all UI elements here
all_input = []


def submit_all():
    rounds = rounds_var.get()
    speed = speed_var.get()
    runmode = run_var.get()

    print("Rounds:", rounds)
    print("Speed:", speed)
    print("Run mode:", runmode)

    # Hide everything
    for w in all_input:
        w.pack_forget()

    # Now you can start the simulation
    # simulate(rounds, speed, runmode)


def ask_user_inputs():

    # --- Number of rounds (Slider) ---
    rounds_label = Label(
        window, text="Number of rounds (1–100):",
        font=("Arial", 25), bg="white", border=5, relief="solid"
    )
    rounds_label.pack(pady=(20, 5))
    all_input.append(rounds_label)

    global rounds_var
    rounds_var = IntVar(value=10)   # default value

    rounds_slider = Scale(window, from_=1, to=100, orient=HORIZONTAL,
                          length=400, font=("Arial", 18), bg="#00eeff", troughcolor="white",
                          highlightthickness=0, variable=rounds_var, border=5, relief="sunken",
                          resolution=1)

    rounds_slider.pack(pady=(0, 20))
    all_input.append(rounds_slider)

    # --- Initial plants and animals ---
    row_frame = Frame(window, bg="#8dfc76")
    row_frame.pack(pady=5)
    all_input.append(row_frame)

    # Innitial plants
    # Left column (plants)
    plant_frame = Frame(row_frame, bg="#8dfc76")
    plant_frame.pack(side="left", padx=40)

    plant_label = Label(plant_frame, text="Select initial plants:",
                        font=("Arial", 25), bg="white", border=5, relief="solid")
    plant_label.pack(anchor="w", pady=(0, 5))

    plant_list = Listbox(plant_frame, font=("Arial", 20), bg="white",
                         border=5, relief="groove", selectmode=MULTIPLE, height=4,
                         exportselection=False)

    plants = ["Eucalyptus", "Mango Tree", "Elderberry", "Grass"]
    for p, plant in enumerate(plants, start=1):
        plant_list.insert(p, plant)

    plant_list.pack(anchor="w", pady=(0, 10))
    all_input.append(plant_list)

    # Innitial animals
    # Right column (animals)
    animal_frame = Frame(row_frame, bg="#8dfc76")
    animal_frame.pack(side="left", padx=40)

    animal_label = Label(animal_frame, text="Select initial animals:",
                         font=("Arial", 25), bg="white", border=5, relief="solid")
    animal_label.pack(anchor="e", pady=(0, 5))
    animal_list = Listbox(animal_frame, font=("Arial", 20), bg="white", border=5, relief="groove", selectmode=MULTIPLE, height=4,
                          exportselection=False)
    animals = ["Rabbit", "Koala", "Fox", "Leopard"]
    for a, animal in enumerate(animals, start=1):
        animal_list.insert(a, animal)

    animal_list.pack(anchor="e", pady=(0, 10))
    all_input.append(animal_list)

    # --- Speed mode ---
    speed_frame = Frame(window, bg="#8dfc76")
    speed_frame.pack(pady=10)
    all_input.append(speed_frame)

    speed_label = Label(speed_frame, text="Speed mode:",
                        font=("Arial", 25), bg="white", border=5, relief="solid")
    speed_label.pack()

    global speed_var
    speed_var = StringVar(value="none")  # default speed

    for text, value in [("Slow", "slow"), ("Normal", "normal"), ("Fast", "fast")]:
        rb = Radiobutton(speed_frame, text=text, variable=speed_var, value=value,
                         font=("Arial", 20), bg="white", border=3, relief="ridge")
        rb.pack(anchor="w")
        all_input.append(rb)

    # --- Run mode ---
    run_frame = Frame(window, bg="#8dfc76")
    run_frame.pack(pady=10)
    all_input.append(run_frame)

    run_label = Label(run_frame, text="Run mode:",
                      font=("Arial", 25), bg="white", border=5, relief="solid")
    run_label.pack()

    global run_var
    run_var = StringVar(value="none")  # default run mode

    for text, value in [("Auto-run", "auto"), ("Step-by-step", "step")]:
        rb = Radiobutton(run_frame, text=text, variable=run_var, value=value,
                         font=("Arial", 20), bg="white", border=3, relief="ridge")
        rb.pack(anchor="w")
        all_input.append(rb)

    # --- Submit button ---
    submit = Button(window, text="Submit", font=(
        "Arial", 20), border=1, relief="groove", command=submit_all)
    submit.pack(expand=True)
    all_input.append(submit)


window.mainloop()
