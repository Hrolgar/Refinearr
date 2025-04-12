import logging

class ColorFormatter(logging.Formatter):
    """
    Custom formatter that adds a service name to the log record and optionally colors the whole log message.
    """
    # ANSI escape codes for colors, but make it light so we can see it on white or black background.
    COLORS = {
        'red': "\033[31m",
        'green': "\033[32m",
        'yellow': "\033[33m",
        'blue': "\033[34m",
        'magenta': "\033[35m",
        'cyan': "\033[36m",
        'white': "\033[37m",
        'black': "\033[30m",
        'light_red': "\033[91m",
        'light_green': "\033[92m",
        'light_yellow': "\033[93m",
        'light_blue': "\033[94m",
        'light_magenta': "\033[95m",
    }
    RESET = "\033[0m"

    def __init__(self, fmt=None, datefmt=None, service_name="", color: str = None):
        """
        Initialize the formatter.
        :param fmt: Format string for log messages.
        :param datefmt: Date format string.
        :param service_name: Optional service name to include.
        :param color: Optional color name (e.g. 'red', 'blue') for the whole message.
        """
        if fmt is None:
            # Include the service name in the message if provided.
            if service_name:
                fmt = '%(asctime)s - %(levelname)s - {} - %(message)s'.format(service_name)
            else:
                fmt = '%(asctime)s - %(levelname)s - %(message)s'
        super().__init__(fmt, datefmt)
        self.service_name = service_name
        # Retrieve the color code if provided.
        self.color_code = self.COLORS.get(color.lower(), "") if color else ""
        self.reset_code = self.RESET if self.color_code else ""

    def format(self, record):
        original = super().format(record)
        if self.color_code:
            # Wrap the entire formatted message in the selected color.
            return f"{self.color_code}{original}{self.reset_code}"
        else:
            return original
