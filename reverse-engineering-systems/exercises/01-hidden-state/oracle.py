"""Public runner. Internal rules intentionally live outside the learner prompt."""
from reveal.machine import Machine


def main():
    machine = Machine()
    while True:
        try:
            command = input()
        except EOFError:
            break
        print(machine.query(command), flush=True)


if __name__ == "__main__":
    main()
