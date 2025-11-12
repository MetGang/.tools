import os
from pathlib import Path

def main() -> None:
    for p in map(Path, sorted(os.listdir())):
        if not p.is_file():
            continue
        print(p)
        parts = str(p).split(' - ')
        n = input('> S')
        if n == '':
            continue
        parts[1] = 'S' + n + ' ' + parts[1]
        p.rename(' - '.join(parts))

if __name__ == '__main__':
    main()
