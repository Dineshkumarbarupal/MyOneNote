"""MyOneNote - entry point."""

import eel


@eel.expose
def say_hello(name: str) -> str:
    """Python function callable from JavaScript through Eel."""
    return f"Namaste, {name}! MyOneNote me aapka swagat hai."


def main() -> None:
    eel.init("web")
    eel.start("index.html", size=(1100, 720))


if __name__ == "__main__":
    main()
