import sys
import os
from typing import List, Optional

from settings import CONFIG_IDS, CYAN, RED, GREEN
from utils import print_colored
from colorama import Style

# ─── Cross‐Platform getch() (no external deps) ────────────────────────────────────
try:
    # On Windows, use msvcrt
    import msvcrt

    def getch() -> str:
        ch = msvcrt.getch()
        # If special key (e.g. arrow), msvcrt.getch() returns b'\x00' or b'\xe0' first.
        if ch in (b'\x00', b'\xe0'):
            _ = msvcrt.getch()  # consume second byte and ignore
            return ''
        try:
            return ch.decode('utf-8')
        except UnicodeDecodeError:
            return ''
except ImportError:
    # On Unix (Linux/macOS), use termios + tty
    import tty
    import termios

    def getch() -> str:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


def autocomplete_prompt(prompt: str, options: List[str]) -> Optional[str]:
    """
    Let the user type to search through `options`.
    Displays up to 10 matches (case‐insensitive prefix match).
    Backspace deletes. Press ENTER to:
      • accept if buffer exactly matches one suggestion, or
      • if multiple matches exist, switch to numbered‐selection mode.
    ESC ('\x1b') or Ctrl+C ('\x03') cancels (returns None).
    """
    buffer = ""
    matches: List[str] = []
    max_suggestions = 10

    # Print instruction once, above the prompt
    instruction = (
        f"{CYAN}Type to filter. Press ENTER to accept exact match "
        "or choose from numbered list. Backspace to delete. ESC to cancel.{Style.RESET_ALL}"
    )
    print(instruction)

    def _render():
        # Clear prompt line and suggestion lines (max_suggestions)
        total_clear = max_suggestions + 1  # +1 for the prompt line
        for _ in range(total_clear):
            sys.stdout.write("\r" + " " * (os.get_terminal_size().columns) + "\n")
        # Move cursor back up to where the prompt should be
        sys.stdout.write(f"\033[{total_clear}A")

        # Recompute matches
        nonlocal matches
        matches = [opt for opt in options if opt.lower().startswith(buffer.lower())]
        matches = matches[:max_suggestions]

        # Print prompt+buffer
        sys.stdout.write("\r" + CYAN + prompt + buffer + Style.RESET_ALL)
        sys.stdout.flush()

        # Print suggestions
        for match in matches:
            sys.stdout.write("\n")
            prefix = "  "
            if buffer.lower() == match.lower():
                prefix = "➜ "
                sys.stdout.write(GREEN + prefix + match + Style.RESET_ALL)
            else:
                sys.stdout.write("  " + match)
        # Move cursor back up to the prompt line
        sys.stdout.write(f"\033[{len(matches)}A")
        sys.stdout.flush()

    # Initial render
    _render()

    while True:
        try:
            ch = getch()
        except (KeyboardInterrupt, Exception):
            # Treat Ctrl+C or any getch error as cancel
            # Clear suggestion block before returning
            sys.stdout.write("\n" * (max_suggestions + 1))
            return None

        # ESC (0x1b) or Ctrl+C (0x03) → cancel
        if ch in ('\x1b', '\x03'):
            sys.stdout.write("\n" * (max_suggestions + 1))
            return None

        # ENTER ('\r' or '\n')
        if ch in ('\r', '\n'):
            # If buffer exactly matches one suggestion, accept it
            for match in matches:
                if match.lower() == buffer.lower():
                    sys.stdout.write("\n" * (max_suggestions - len(matches) + 1))
                    return match

            # If multiple matches exist, switch to numbered selection
            if matches:
                # Clear suggestion block (so numbered list appears cleanly)
                sys.stdout.write("\n" * (max_suggestions - len(matches) + 1))

                print("\nMultiple matches found:")
                for idx, m in enumerate(matches, start=1):
                    print(f"  ({idx}) {m}")

                while True:
                    choice = input(f"\nSelect [1-{len(matches)}] or press ENTER to cancel: ").strip()
                    if choice == "":
                        return None
                    if choice.isdigit():
                        num = int(choice)
                        if 1 <= num <= len(matches):
                            return matches[num - 1]
                    print_colored("❌ Invalid selection. Enter a number from the list or press ENTER to cancel.", RED)

                # Unreachable, but required by syntax
            else:
                # No matches at all
                print_colored("\n❌ No matches found. Continue typing or press ESC to cancel.", RED)
                _render()
            continue

        # BACKSPACE ('\x7f' or '\b')
        if ch in ('\x7f', '\b'):
            if buffer:
                buffer = buffer[:-1]
                _render()
            continue

        # Printable character
        if ch.isprintable():
            buffer += ch
            _render()
            continue

        # Ignore anything else
        continue
