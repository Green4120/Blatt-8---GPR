import time
import threading
from blatt8 import Ecosystem, Eucalyptus, MangoTree, Elderberry, Grass, Rabbit, Koala, Fox, Leopard

# Global pause flag
pause_flag = False


def toggle_pause():
    """Toggle pause state."""
    global pause_flag
    pause_flag = not pause_flag
    if pause_flag:
        print("\n--- Simulation Paused ---")
    else:
        print("\n+++ Simulation Resumed +++")


def listen_for_pause():
    """Background thread that listens for 'p' to pause/resume."""
    while True:
        key = input()
        if key.lower() == "p":
            toggle_pause()


def simulate(rounds, speed, runmode, selected_plants=None, selected_animals=None):
    """Run the ecosystem simulation with pause support."""
    global pause_flag
    pause_flag = False  # reset pause state

    # Start pause listener thread
    threading.Thread(target=listen_for_pause, daemon=True).start()

    island = Ecosystem(size=100, days=int(rounds), temperature=25)

    # Default selections
    if not selected_plants:
        selected_plants = ["Eucalyptus", "Mango Tree", "Elderberry", "Grass"]
    if not selected_animals:
        selected_animals = ["Rabbit", "Koala", "Fox", "Leopard"]

    # Map names to classes
    plant_classes = {
        "Eucalyptus": Eucalyptus,
        "Mango Tree": MangoTree,
        "Elderberry": Elderberry,
        "Grass": Grass
    }
    animal_classes = {
        "Rabbit": Rabbit,
        "Koala": Koala,
        "Fox": Fox,
        "Leopard": Leopard
    }

    # Add selected organisms
    for plant in selected_plants:
        island.add_organism(plant_classes[plant]())
    for animal in selected_animals:
        island.add_organism(animal_classes[animal]())

    # Speed delays
    delays = {"slow": 1.0, "normal": 0.5, "fast": 0.1}
    delay = delays.get(speed, 0.5)

    print("\nSimulation in progress...\n"
          "Press 'p' at any time to pause/resume.\n")

    # Simulation loop
    for day in range(int(rounds)):
        island.simulate_step()

        if runmode == "step":
            print(
                f"Day {island.day}: {len(island.flora)} plants, {len(island.fauna)} animals")
            # Pause handling
            while pause_flag:
                time.sleep(0.1)

            # Auto delay
            time.sleep(delay)

        elif runmode == "auto":
            # Pause handling
            while pause_flag:
                time.sleep(0.1)

            # Auto delay
            time.sleep(delay)

    print(f"\nSimulation complete after {rounds} days.")
    print(f"Final result: {len(island.flora)} plants, {len(island.fauna)} animals")


def ask_user_input():
    print("=== Ecosystem Simulation Configuration ===")

    # --- Number of rounds ---
    while True:
        rounds = input("Enter number of rounds (1–20): ")
        if rounds.isdigit() and 1 <= int(rounds) <= 20:
            rounds = int(rounds)
            break
        print("Invalid input. Please enter a number between 1 and 20.")

    # --- Speed mode ---
    speed_options = {"1": "slow", "2": "normal", "3": "fast"}
    print("\nChoose speed mode:")
    print("1. Slow")
    print("2. Normal")
    print("3. Fast")

    while True:
        speed_choice = input("Select speed (1–3): ")
        if speed_choice in speed_options:
            speed = speed_options[speed_choice]
            break
        print("Invalid choice. Please enter 1, 2, or 3.")

    # --- Run mode ---
    run_options = {"1": "auto", "2": "step"}
    print("\nChoose run mode:")
    print("1. Auto-run")
    print("2. Step-by-step")

    while True:
        run_choice = input("Select run mode (1–2): ")
        if run_choice in run_options:
            runmode = run_options[run_choice]
            break
        print("Invalid choice. Please enter 1 or 2.")

    print("\nConfiguration complete!")
    print(f"Rounds: {rounds}")
    print(f"Speed: {speed}")
    print(f"Run mode: {runmode}")
    return rounds, speed, runmode


if __name__ == "__main__":
    # Default run for testing
    rounds, speed, runmode = ask_user_input()
    simulate(rounds, speed, runmode)