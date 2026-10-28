import mmap
import struct
import time
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich import box
import engine

order_format = 'Q d I'
order_size = struct.calcsize(order_format)
FILE_SIZE = 10 * 1024 * 1024

def generate_ui(order_count, best_bid, best_ask, elapsed_time):
    """
    Generates a live Rich terminal table summarizing engine metrics.
    Takes the total orders processed, the current best bid and ask prices,
    and the elapsed time to calculate and display real-time throughput.
    """
    
    table = Table(box=box.SIMPLE_HEAVY, expand=True)
    table.add_column("System Metric", style="cyan", justify="left")
    table.add_column("Live Value", style="magenta", justify="right")
    
    table.add_row("Total Orders Processed", f"{order_count:,}")
    table.add_row("Best Bid (Buy Price)", f"${best_bid:.2f}" if best_bid > 0 else "---")
    table.add_row("Best Ask (Sell Price)", f"${best_ask:.2f}" if best_ask < 999999 else "---")
    
    ops = order_count / elapsed_time if elapsed_time > 0 else 0
    table.add_row("Live Throughput", f"{ops:,.0f} orders/sec")

    return Panel(
        table, 
        title="[bold green]ChronosMatch HFT Engine - Zero-Copy Live Feed[/bold green]", 
        border_style="green"
    )

def run_dashboard():
    print("Waiting for data firehose to initialize...")
    time.sleep(1)
    
    try:
        with open("live_bus.dat", "r+b") as f:
            mm = mmap.mmap(f.fileno(), 0)
            offset = 0
            last_id = 0
            start_time = time.time()
            
            # Refresh the UI 10 times per second
            with Live(generate_ui(0, 0, 0, 0), refresh_per_second=10) as live:
                while True:
                    mm.seek(offset)
                    raw_bytes = mm.read(order_size)
                    order_id, price, qty = struct.unpack(order_format, raw_bytes)
                    
                    if order_id > last_id:
                        side = 1 if order_id % 2 == 0 else 2
                        engine.submit_order(order_id, side, price, qty)
                        
                        last_id = order_id
                        offset = (offset + order_size) % FILE_SIZE
                        
                        # Throttle the UI calculation so the engine stays fast
                        if order_id % 500 == 0:
                            best_bid, best_ask = engine.get_spread()
                            elapsed = time.time() - start_time
                            live.update(generate_ui(order_id, best_bid, best_ask, elapsed))
                    else:
                        pass
                        
    except KeyboardInterrupt:
        print("\nDashboard shut down safely.")
    except FileNotFoundError:
        print("\nError: live_bus.dat not found. Start writer.py first!")

if __name__ == "__main__":
    run_dashboard()