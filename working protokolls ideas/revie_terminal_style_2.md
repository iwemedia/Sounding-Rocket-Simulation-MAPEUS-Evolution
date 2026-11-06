from rich.prompt import Prompt
# wenn promt verwendet werden soll


# render_mission_briefing(self) (Am Ende der Methode)
# Vorher:
self.console.print("\n[bold blink green]▲ PRESS ENTER TO PROCEED...")
input()  # Wartet unsichtbar

# prompt_workbench_action(self)
# Vorher:
self.console.print("\n [bold white]Enter an [EXP-Code]...", end="")
return input().strip().lower()

# Vorher:
slot_prompt = f"-> Choose target workbench slot (1 to {total_capacity}): "
return input(slot_prompt).strip()


# • Stelle 5: In den Phasen-Übergängen
# (render_phase_one_complete, render_phase_two_success, render_weather_nominal_window,
# render_final_mission_report)
# • Überall dort steht am Ende ein einfaches input(),
#  um das Spiel anzuhalten, bis der Spieler Enter drückt.
# Das kann so bleiben, aber ein einheitliches Prompt.ask("...")
# fängt Fehleingaben schöner ab.


# ❌ ALTER CODE:
def render_module_removal_success(self, instance_id: str):
    print(f"\n[OK] Removed experiment module: {instance_id}")
    time.sleep(1)

def render_module_removal_warning(self, instance_id: str):
    print(f"\n[WARN] Nothing to remove. No active module found with ID: '{instance_id}'")
    time.sleep(1)

def render_generic_command_error(self):
    print("\n[ERROR] Invalid Exp-Code or Command! Please try again.")
    time.sleep(1.5)


# 🚀 OPTIMIERTER CODE-VORSCHLAG:
def render_module_removal_success(self, instance_id: str):
    self.console.print(f"\n[bold green][OK][/bold green] Removed experiment module: [bold yellow]{instance_id}[/bold yellow]")
    time.sleep(1)

def render_module_removal_warning(self, instance_id: str):
    self.console.print(f"\n[bold yellow][WARN][/bold yellow] Nothing to remove. No active module found with ID: '{instance_id}'")
    time.sleep(1)

def render_generic_command_error(self):
    self.console.print("\n[bold red][ERROR][/bold red] Invalid Exp-Code or Command! Please try again.")
    time.sleep(1.5)


# ❌ ALTER CODE:
def render_despin_input_error(self):
    print("\n[INPUT ERROR] Use a decimal dot (.) instead of a comma (,).\n")

def render_despin_physics_error(self, error_message: str):
    print(f"\n[PHYSICS ERROR] {error_message}")
    input("Press any key to continue...")

def render_despin_wrong_answer_warning(self):
    print(f"\n(CALCULATION WRONG - Try AGAIN!)\n")

def render_despin_numeric_error(self):
    print("\nPlease enter a valid decimal number.\n")


# 🚀 OPTIMIERTER CODE-VORSCHLAG:
def render_despin_input_error(self):
    self.console.print("\n[bold red][INPUT ERROR][/bold red] Use a decimal dot (.) instead of a comma (,).\n")

def render_despin_physics_error(self, error_message: str):
    self.console.print(f"\n[bold red][PHYSICS ERROR][/bold red] {error_message}")
    # Hier nutzen wir Prompt.ask, damit auch das Abfangen des Enters im Rich-Style läuft
    from rich.prompt import Prompt
    Prompt.ask("\nPress ENTER to continue")

def render_despin_wrong_answer_warning(self):
    self.console.print("\n[bold yellow][CALCULATION WRONG][/bold yellow] Incorrect approximation. Try again!\n")

def render_despin_numeric_error(self):
    self.console.print("\n[bold red][ERROR][/bold red] Please enter a valid decimal number.\n")


# ❌ ALTER CODE:
def render_error_recovery_menu(self, error_message: str) -> str:
    print("\n" + "!" * 70)
    print(f"[ALERT] STRUCTURAL BOUNDARY SAFETY ENGINE GUARD TRIGGERED:")
    print(f"-> {error_message}")
    print("!" * 70)
    print("The application intercepted an assembly error. Choose a recovery option:")
    print(" Option: Return straight to the workbench editing grid to manually modify layout.")
    print(" Option: Clear the entire active workbench layout to reset blueprint from scratch.")
    print(" Option: Terminate deployment operations and safely abort ground console control systems.")

    return input("\nEnter recovery option (1/2/3): ").strip()


# 🚀 OPTIMIERTER CODE-VORSCHLAG:
def render_error_recovery_menu(self, error_message: str) -> str:
    self.console.print("\n" + "!" * 70, style="bold red")
    self.console.print(f"[ALERT] STRUCTURAL BOUNDARY SAFETY ENGINE GUARD TRIGGERED:", style="bold red")
    self.console.print(f"-> {error_message}", style="bold yellow")
    self.console.print("!" * 70 + "\n", style="bold red")

    self.console.print("The application intercepted an assembly error. Choose a recovery option:")
    self.console.print(" [bold white][/bold white] Return to the workbench editing grid to manually modify layout.")
    self.console.print(" [bold white][/bold white] Clear the entire active workbench layout to reset blueprint.")
    self.console.print(" [bold white][/bold white] Terminate deployment operations and safely abort ground console.")

    # Choices sorgt dafür, dass nur '1', '2' oder '3' akzeptiert werden
    from rich.prompt import Prompt
    return Prompt.ask("\nEnter recovery option", choices=["1", "2", "3"]).strip()


Deine nächsten Schritte:

1. Gehe in deiner terminal_view.py zu den jeweiligen Methoden.
2. Ersetze das print(...) durch self.console.print(...).
3. Setze optionale Farb-Tags (wie [bold green]...[/bold green]) ein, um wichtige Wörter hervorzuheben.
Lass mich wissen, wenn du den Text durchgegangen bist. Möchtest du danach auch eine ähnliche 
Markdown-Übersicht für die verbleibenden input()-Stellen haben?
