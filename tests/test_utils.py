import time
from utils import readable_size, format_date

def test_readable_size_bytes():
    assert readable_size(512) == "512 bytes"

def test_readable_size_kib():
    # 2048 bytes should be about 2.00 KiB
    result = readable_size(2048)
    assert "KiB" in result
    # You can check the actual conversion as well:
    assert result == "2.00 KiB"

def test_readable_size_mib():
    # 2 * 1024**2 bytes should be 2.00 MiB
    result = readable_size(2 * 1024**2)
    assert result == "2.00 MiB"

def test_format_date():
    # For a fixed timestamp like 1609459200 = 01.01.2021 00:00:00 (UTC)
    # Note: The output will depend on the local timezone.
    timestamp = 1609459200  
    formatted = format_date(timestamp)
    # Expect the Norwegian-style date format (e.g., "01.01.2021 T 00:00")
    # We'll check it begins with "01.01.2021"
    assert formatted.startswith("01.01.2021")
