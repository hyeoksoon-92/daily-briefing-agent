# main.py
from agent import run_agent
from output import print_briefing, save_briefing
from rich.console import Console

console = Console()


def main() -> None:
    console.print("[cyan]브리핑을 수집하는 중입니다...[/cyan]")
    briefing = run_agent()
    print_briefing(briefing)
    filepath = save_briefing(briefing)
    console.print(f"\n[green]저장 완료:[/green] {filepath}")


if __name__ == "__main__":
    main()
