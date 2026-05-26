import random

WORLD_MIN = -15
WORLD_MAX = 15

START_X = 0
START_Y = 0

START_ENERGY = 30

# ===== UKRYTA BAZA (losowa w każdej grze) =====
BASE_X = random.randint(WORLD_MIN, WORLD_MAX)
BASE_Y = random.randint(WORLD_MIN, WORLD_MAX)


def clamp(v, min_v, max_v):
    return max(min_v, min(max_v, v))


# ===== ZDARZENIA LOSOWE =====
def random_event():
    roll = random.randint(1, 100)

    if roll < 12:
        return ("BURZA PIASKOWA", -6, "Silna burza zabiera paliwo")
    elif roll < 20:
        return ("STACJA ENERGII", +8, "Znaleziono źródło energii")
    elif roll < 25:
        return ("AWARIA", -4, "Usterka systemu")
    return None


# ===== ZDARZENIA ŚWIATA =====
def world_event(x, y):
    events = {
        (3, 3): ("RUINY", "block"),
        (5, 5): ("REAKTOR", "energy", +6),
        (-4, 2): ("PIASEK", "energy", -2),
        (7, -3): ("ZAKŁÓCENIA", "energy", -3)
    }
    return events.get((x, y))


# ===== GRA =====
def run_game():
    name = input("Nazwa łazika: ")

    x, y = START_X, START_Y
    energy = START_ENERGY

    step = 0
    history = []

    print("\n=== EKSPEDYCJA ===")
    print(f"Łazik: {name}")
    print(f"Start: ({x},{y})")
    print("Cel: NIEZNANY (musisz go odkryć)")
    print(f"Paliwo: {energy}")
    print("====================\n")

    while True:
        print(f"\nKROK {step}")
        print(f"{name} | ({x},{y}) | Paliwo: {energy}")

        move = input("Ruch (w/a/s/d): ").lower()

        prev_x, prev_y = x, y
        prev_energy = energy

        # ===== RUCH =====
        if move == "w":
            y += 1
        elif move == "s":
            y -= 1
        elif move == "a":
            x -= 1
        elif move == "d":
            x += 1

        x = clamp(x, WORLD_MIN, WORLD_MAX)
        y = clamp(y, WORLD_MIN, WORLD_MAX)

        # koszt ruchu
        energy -= 1

        # ===== BAZA (UKRYTA) =====
        if (x, y) == (BASE_X, BASE_Y):
            result = "SUKCES"
            reason = "Odnaleziono bazę"
            break

        # ===== ŚWIAT =====
        event = world_event(x, y)
        if event:
            if len(event) == 3:
                name_ev, type_ev, value = event
            else:
                name_ev, type_ev = event
                value = 0

            print(f"[ODKRYCIE] {name_ev}")

            if type_ev == "energy":
                energy += value
            elif type_ev == "block":
                x, y = prev_x, prev_y

        # ===== LOSOWE =====
        rand = random_event()
        if rand:
            name_ev, value, desc = rand
            print(f"[LOSOWE] {name_ev}: {desc}")
            energy += value

        print(f"Ruch: ({prev_x},{prev_y}) -> ({x},{y})")
        print(f"Paliwo: {prev_energy} -> {energy}")

        history.append((step, x, y, energy))
        step += 1

        # ===== KONIEC =====
        if energy <= 0:
            result = "PORAŻKA"
            reason = "Brak paliwa"
            break

    # ===== RAPORT =====
    print("\n=== RAPORT KOŃCOWY ===")
    print(f"Łazik: {name}")
    print(f"Końcowa pozycja: ({x},{y})")
    print(f"Kroki: {step}")
    print(f"Paliwo: {energy}")
    print(f"Wynik: {result}")
    print(f"Powód: {reason}")

    print("\nOstatnie kroki:")
    for h in history[-5:]:
        print(h)

    again = input("\nZagrać ponownie? (t/n): ").lower()
    if again == "t":
        run_game()


if __name__ == "__main__":
    run_game()