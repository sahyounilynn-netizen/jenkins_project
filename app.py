"""Simple greeting application used by the Lab 10 Jenkins CI/CD pipeline."""

AUTHOR = "Lynn Sahyouni"


def greet(name):
    """Return a greeting for ``name`` signed by the author."""
    return f"Hello, {name} from {AUTHOR}!"


def main():
    """Print the default greeting and return it."""
    message = greet("World")
    print(message)
    return message


if __name__ == "__main__":
    main()
