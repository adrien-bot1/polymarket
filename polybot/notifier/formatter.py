from typing import List, Dict, Any

def escape_md(text: str) -> str:
    """Escape special characters for Telegram MarkdownV2."""
    # Order matters: escape backslash first
    chars = ['\\', '_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!', '?']
    for char in chars:
        text = text.replace(char, f'\\{char}')
    return text

def format_alert_msg(market: Dict[str, Any]) -> str:
    """Format a single market alert for Telegram."""
    score = market.get("score", 0)
    question = escape_md(market.get("question", "Unknown Market"))
    prices = market.get("outcomePrices", ["?", "?"])
    yes_price = escape_md(str(prices[0])) if len(prices) > 0 else "?"
    no_price = escape_md(str(prices[1])) if len(prices) > 1 else "?"
    vol_24h = float(market.get("volume24hr", 0))
    total_vol = float(market.get("volume", 0))
    
    msg = (
        f"⚡ *CLOSING WINDOW ALERT* — Score: {score}/100\n\n"
        f"🚀 *{question}*\n\n"
        f"🟢 YES: {yes_price}  |  🔴 NO: {no_price}\n"
        f"📊 Vol 24h: ${vol_24h:,.0f}  |  Total: ${total_vol:,.0f}\n"
    )
    
    ext = market.get("external_data", {})
    if ext:
        source = escape_md(ext.get("source", "unknown"))
        msg += f"🔗 Source: {source}\n"
        
    return msg

def format_summary_msg(total: int, filtered: int, alerts: int) -> str:
    """Format a scan summary for Telegram."""
    return (
        f"🤖 *PolyBot Scan Complete*\n\n"
        f"✅ Processed: {total:,} markets\n"
        f"🔍 Passed Filters: {filtered:,}\n"
        f"⚡ Alerts Found: {alerts}\n"
    )
