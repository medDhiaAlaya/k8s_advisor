from pyfiglet import Figlet
from rich.console import Console
from rich.panel import Panel

console = Console()

def display_banner():
    figlet = Figlet(font='slant')  # You can change the font if you want
    banner_text = figlet.renderText("CloudHustler")
    class_text = figlet.renderText("Arctic10")

    combined_banner = f"[cyan]{banner_text}[/cyan]\n[blue]{class_text}[/blue]"
    console.print(Panel.fit(combined_banner, border_style="bold magenta"))
