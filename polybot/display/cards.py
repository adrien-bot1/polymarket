from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from typing import Dict, Any, List

console = Console()

def render_alert_card(market: Dict[str, Any]):
    score = market.get("score", 0)
    color = "orange3" if score >= 50 else "yellow"
    
    title = f"[bold {color}]⚡ CLOSING WINDOW ALERT — Score: {score}/100[/bold {color}]"
    
    table = Table.grid(padding=(0, 1))
    table.add_row("🚀", f"[bold white]\"{market.get('question', 'Unknown Market')}\"[/bold white]")
    
    # Prices
    prices = market.get("outcomePrices", ["?", "?"])
    yes_price = prices[0] if len(prices) > 0 else "?"
    no_price = prices[1] if len(prices) > 1 else "?"
    table.add_row("🟢", f"YES {yes_price}  [red]NO {no_price}[/red]")
    
    # Volume
    vol_24h = market.get("volume24hr", "0")
    total_vol = market.get("volume", "0")
    table.add_row("📊", f"Vol 24h: ${float(vol_24h):,.0f}  Total: ${float(total_vol):,.0f}")
    
    # External Source
    ext = market.get("external_data", {})
    if ext:
        table.add_row("🔗", f"[blue]{ext.get('source', 'unknown source')}[/blue]")

    panel = Panel(table, title=title, border_style=color, expand=False)
    console.print(panel)

def render_scan_summary(total: int, filtered: int, alerts: int):
    console.print("\n" + "═" * 60)
    console.print(f"✅ [bold green]Scan complete[/bold green] — {total:,} markets processed")
    console.print(f"🔍 Passed filters: {filtered:,}  |  Alerts: {alerts}")
    console.print("═" * 60 + "\n")
