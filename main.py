from manager import TaskManager
import sys


def main() -> None:
    args = sys.argv[1:]
    manager = TaskManager()
    manager.commands(args)
    manager.save_to_json()


if __name__ == "__main__":
    main()