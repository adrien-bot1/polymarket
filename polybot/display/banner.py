import pyfiglet
from rich.console import Console

console = Console()

def render_banner():
    banner_text = pyfiglet.figlet_format("PolyBot", font="slant")
    console.print(f"[bold blue]{banner_text}[/bold blue]")
    console.print("[bold yellow]↓ CLOSING WINDOW SCANNER ↓[/bold yellow]")
    console.print("low bankroll · no frozen capital · real data sources\n")
    console.print("─" * 60)
