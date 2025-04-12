# import logging
#
# class ColorFormatter(logging.Formatter):
#     """
#     Custom formatter that adds a service name to the log record, and optionally colors the log level.
#     """
#     # Predefined ANSI escape codes for some colors. Add or modify as desired.
#     COLORS = {
#         'red': "\033[31m",
#         'green': "\033[32m",
#         'yellow': "\033[33m",
#         'blue': "\033[34m",
#         'magenta': "\033[35m",
#         'cyan': "\033[36m",
#         'white': "\033[37m",
#         'black': "\033[30m",
#         'light_red': "\033[91m",
#     }
#     RESET = "\033[0m"
#
#     def __init__(self, fmt=None, datefmt=None, service_name="", color: str = None):
#         """
#         Initialize the formatter.
#
#         :param fmt: Format string for log messages.
#         :param datefmt: Date format string.
#         :param service_name: Optional service name to include in log messages.
#         :param color: Optional color for the log level name. Should be one of the COLORS keys.
#         """
#         if fmt is None:
#             # Append service name after level name if provided.
#             if service_name:
#                 fmt = '%(asctime)s - %(levelname)s - {} - %(message)s'.format(service_name)
#             else:
#                 fmt = '%(asctime)s - %(levelname)s - %(message)s'
#         super().__init__(fmt, datefmt)
#         self.service_name = service_name
#         self.color_code = self.COLORS.get(color.lower(), "") if color else ""
#         self.reset_code = self.RESET if self.color_code else ""
#
#     def format(self, record):
#         # Inject the service name in case you want it available elsewhere.
#         record.service_name = self.service_name
#         # Wrap the levelname in color codes if set.
#         if self.color_code:
#             record.levelname = f"{self.color_code}{record.levelname}{self.reset_code}"
#         return super().format(record)
