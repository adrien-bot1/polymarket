from polybot.display.banner import render_banner
from polybot.display.cards import render_alert_card, render_scan_summary
from polybot.display.progress import create_progress_bar
import time

def test_ui():
    render_banner()
    
    with create_progress_bar() as progress:
        task = progress.add_task("[cyan]Scanning markets...", total=100)
        for i in range(100):
            time.sleep(0.02)
            progress.update(task, advance=1)
            
    render_scan_summary(100, 15, 2)
    
    fake_market = {
        "question": "Will the highest temperature in Seoul be 4°C on Feb 18?",
        "score": 75,
        "outcomePrices": ["0.085", "0.915"],
        "volume24hr": "3324",
        "volume": "4381",
        "external_data": {"source": "www.wunderground.com"}
    }
    
    render_alert_card(fake_market)

if __name__ == "__main__":
    test_ui()
