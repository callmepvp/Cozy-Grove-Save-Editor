from colorama import Style
from settings import GREEN, RED

def print_colored(message: str, color: str) -> None:
    """
    Print `message` in the given `color` (Fore.*), then reset.
    """
    print(f"{color}{message}{Style.RESET_ALL}")


def print_success(message: str) -> None:
    """
    Prefix with ✅ and print in GREEN.
    """
    print_colored(f"{message}", GREEN)


def print_error(message: str) -> None:
    """
    Prefix with ❌ and print in RED.
    """
    print_colored(f"{message}", RED)