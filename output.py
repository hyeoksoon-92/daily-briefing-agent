# output.py
from pathlib import Path
from datetime import date
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

BRIEFINGS_DIR = Path(__file__).parent / "briefings"
console = Console()


def save_briefing(content: str) -> Path:
    BRIEFINGS_DIR.mkdir(exist_ok=True)
    filename = f"briefing-{date.today().isoformat()}.md"
    filepath = BRIEFINGS_DIR / filename
    filepath.write_text(content, encoding="utf-8")
    return filepath


def print_briefing(content: str) -> None:
    md = Markdown(content)
    panel = Panel(
        md,
        title=f"[bold cyan]Daily Briefing — {date.today()}[/bold cyan]",
        border_style="cyan",
    )
    console.print(panel)
