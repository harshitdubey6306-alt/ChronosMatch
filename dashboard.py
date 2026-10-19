from rich.live import Live
from rich.table import Table
import time
import random

def generate_table():
    # Simulate dynamic Best Bid / Best Ask prices
    best_bid = random.uniform(149.50, 150.00)
    best_ask = random.uniform(150.01, 150.50)
    spread = best_ask - best_bid
    
    # Build the UI layout
    table = Table(title="ChronosMatch Zero-Copy HFT Engine")
    table.add_column("Metric", justify="right", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")
    
    # Display the Ask (Sell) above the Bid (Buy)
    table.add_row("Best Ask (Sell)", f"${best_ask:.2f}")
    table.add_row("Best Bid (Buy)", f"${best_bid:.2f}")
    table.add_row("Spread", f"${spread:.4f}")
    
    return table

if __name__ == "__main__":
    print("Press Ctrl+C to quit.")
    # Live() automatically refreshes the terminal screen in place
    try:
        with Live(generate_table(), refresh_per_second=10) as live:
            while True:
                time.sleep(0.1)
                live.update(generate_table())
    except KeyboardInterrupt:
        print("\nDashboard closed.")