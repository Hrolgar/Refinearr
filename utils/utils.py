import time

def readable_size(num_bytes):
    """Converts a size in bytes into a human-readable format (GiB, MiB, etc.)."""
    if num_bytes >= 1024**3:
        return f"{num_bytes / 1024**3:.2f} GiB"
    elif num_bytes >= 1024**2:
        return f"{num_bytes / 1024**2:.2f} MiB"
    elif num_bytes >= 1024:
        return f"{num_bytes / 1024:.2f} KiB"
    else:
        return f"{num_bytes} bytes"


def format_date(timestamp):
    """Formats a Unix timestamp into 'dd.mm.yyyy T HH:MM' format (Norwegian style)."""
    return time.strftime('%d.%m.%Y T %H:%M', time.localtime(timestamp))

def print_torrent_details(torrent):
    name = torrent.get('name', 'Unknown Name')
    torrent_hash = torrent.get('hash', 'N/A')
    added_on = format_date(torrent.get('added_on'))
    last_activity = format_date(torrent.get('last_activity'))
    size = readable_size(torrent.get('size', 0))

    # Define the border and width for the details box
    width = 100
    border = "═" * (width - 2)
    # ANSI escape codes for purple (you can choose any color you like)
    color_purple = "\033[95m"
    color_reset = "\033[0m"
    
    # Build each line with padding to ensure alignment.
    line_format = f"║ {{:<18}}: {{:<{width - 23}}}║"

    print(f"{color_purple}╔{border}╗{color_reset}")
    title = "Torrent Details"
    # Center the title within the box width minus two border characters
    print(f"{color_purple}║{title:^{width-2}}║{color_reset}")
    print(f"{color_purple}╠{border}╣{color_reset}")
    
    print(line_format.format("Name", name))
    print(line_format.format("Hash", torrent_hash))
    print(line_format.format("Added on", added_on))
    print(line_format.format("Last activity", last_activity))
    print(line_format.format("Size", size))
    
    print(f"{color_purple}╚{border}╝{color_reset}")