# Vorher: prompt_for_start(self)
return input("Type START to begin the campaign or ESC to exit: ").upper().strip()
# Vorschlag:
return Prompt.ask("[bold white]Type START to begin the campaign or ESC to exit[/bold white]").upper().strip()

