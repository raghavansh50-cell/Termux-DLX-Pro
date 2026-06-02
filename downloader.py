import yt_dlp
import os
import json
import subprocess
import pyfiglet
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt

console = Console()

class TermuxDLX:
    def __init__(self):
        self.config_file = os.path.expanduser("~/.dlx_config.json")
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {"path": "/sdcard/Download/"}
            self.save_config()

    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f)

    def show_banner(self):
        # Figlet setup
        banner_text = pyfiglet.figlet_format("DLX-PRO", font="slant")
        console.print(f"[bold magenta]{banner_text}[/bold magenta]")
        console.print(Panel("[bold white]The Ultimate Multi-Platform Downloader for Termux[/bold white]", 
                      subtitle="Created for [bold cyan]You[/bold cyan]", 
                      border_style="green"))

    def set_path(self):
        new_path = Prompt.ask("[bold cyan]Naya download path daalo[/bold cyan]", default=self.config["path"])
        if not os.path.exists(new_path):
            try:
                os.makedirs(new_path, exist_ok=True)
            except PermissionError:
                console.print("[bold red][X] Permission Denied! Try a different path.[/bold red]")
                return
        self.config["path"] = new_path
        self.save_config()
        console.print("[green]✔ Path update ho gaya![/green]")

    def get_formats(self, url):
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                formats = info.get('formats', [])
                options = []
                seen_res = set()
                # Sirf best video formats filter kar rahe hain
                for f in formats:
                    res = f.get('height')
                    if res and res not in seen_res:
                        options.append({"id": f['format_id'], "res": f"{res}p", "ext": f['ext']})
                        seen_res.add(res)
                return sorted(options, key=lambda x: int(x['res'][:-1]), reverse=True), info.get('title', 'Video')
            except Exception as e:
                console.print(f"[red]URL fetch nahi ho payi: {e}[/red]")
                return None, None

    def download(self, url):
        formats, title = self.get_formats(url)
        if not formats: return
        
        console.print(f"\n[bold yellow]Target:[/bold yellow] [white]{title}[/white]\n")
        for i, f in enumerate(formats):
            console.print(f"[bold green]({i+1})[/bold green] {f['res']} Quality [dim][{f['ext']}][/dim]")
        
        choice = IntPrompt.ask("\n[bold cyan][?] Resolution select karein[/bold cyan]", choices=[str(i+1) for i in range(len(formats))])
        selected_format = formats[choice-1]['id']

        ydl_opts = {
            'format': f'{selected_format}+bestaudio/best',
            'outtmpl': os.path.join(self.config["path"], '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                filename = ydl.prepare_filename(ydl.extract_info(url, download=False))
                subprocess.run(["termux-media-scan", filename], capture_output=True)
                console.print(f"\n[bold green]✔ DONE![/bold green] Saved in {self.config['path']}")
        except Exception as e:
            console.print(f"[bold red]Download Error: {e}[/bold red]")

    def main_menu(self):
        self.show_banner()
        console.print("\n[bold]1.[/bold] 📥 Download Now")
        console.print("[bold]2.[/bold] ⚙️ Settings (Path)")
        console.print("[bold]3.[/bold] ❌ Exit")
        
        m_choice = Prompt.ask("\n[bold yellow]Action chuno[/bold yellow]", choices=["1", "2", "3"])
        
        if m_choice == "1":
            link = Prompt.ask("[bold blue]Link paste karein[/bold blue]")
            if link: self.download(link)
        elif m_choice == "2":
            self.set_path()
        else:
            console.print("[italic red]Leaving... Bye![/italic red]")
            exit()

if __name__ == "__main__":
    app = TermuxDLX()
    while True:
        os.system('clear') # Screen saaf rakhne ke liye
        app.main_menu()
        input("\nPress Enter to return to menu...")
