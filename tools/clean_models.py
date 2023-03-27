import os
import sys

import vulture


def remove_unused_classes(filename: str, dirs: list, max_iters=1) -> int:
    """
    Removes all the unused classes in the given filename.
    """
    total_removed_count = 0

    filename = os.path.abspath(filename)

    for i in range(0, max_iters):
        remove_count = 0

        v = vulture.Vulture()
        v.scavenge(dirs)

        with open(filename, "r") as f:
            lines = f.readlines()

        for item in reversed(v.get_unused_code()):
            if item.typ == 'class' and str(item.filename) == filename:
                remove_count += 1
                for j in range(item.first_lineno - 1, len(lines)):
                    if j >= item.last_lineno and len(lines[j].strip()) == 0:
                        break
                    lines[j] = ""

        with open(filename, "w") as f:
            for line in lines:
                f.write(line)

        total_removed_count += remove_count

        if remove_count == 0:
            break

    format_file(filename)
    return total_removed_count


def format_file(filename: str):
    """
    Formats the given file and optimize the imports.
    """
    os.system(f"black --quiet {filename}")
    os.system(f"autoflake --in-place --remove-all-unused-imports {filename}")
    os.system(f"isort {filename}")


if __name__ == '__main__':
    filename = sys.argv[1]
    print(f"Removing unused class in '{filename}'...")
    remove_count = remove_unused_classes(filename, ['.'], 10)
    print(f"  {remove_count} unused classes removed!")
