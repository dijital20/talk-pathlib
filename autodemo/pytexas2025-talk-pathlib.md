# PyTexas 2025 - Hot: `pathlib`, Not: String Paths

```python
# 
    # hot: pathlib, not: string paths
    #
    # Josh Schneider
    # dijital20@github.com @diji@mastodon.social
```

## In the beginning, there were string paths...

```python

# Let's start with string paths...
path = '~/demo/files/groceries.txt'
path

# Look at how boring that is!

import os.path  # We need this guy to even work with them

os.path.expanduser('~/demo')
os.path.abspath('./demo')

os.path.split(path)
os.path.dirname(path), os.path.basename(path)
os.path.splitext(path)

os.path.exists(path)
os.path.isdir(path)
os.path.isfile(path)

import glob
glob.glob(os.path.expanduser('~/*'))

# There's got to be a better way!
```

## Enter `pathlib`

![pathlib inheritance](../img/pathlib-inheritance.png)

```python
# ^^^ clear ^^^

import pathlib

path = pathlib.Path('~/demo/files/groceries.txt')

type(path)  # Wait, what type?
type(path).__bases__  # What are its bases?
type(path).__mro__  # What are its ancestors?

# What's a PurePath?
pure_path_members = {  # List the PurePath members
    f'{n}()' if callable(v) else n 
    for n, v in vars(pathlib.PurePath).items() 
    if not n.startswith('_')}
sorted(pure_path_members)

# What does Path add?
path_members = {  # List the Path members
    f'{n}()' if callable(v) else n
    for n, v in vars(pathlib.Path).items() 
    if not n.startswith('_')}
sorted(path_members - pure_path_members)
```

## Creating `Path` objects

```python
# ^^^ clear ^^^

from pathlib import Path

path = Path('~/demo/files/groceries.txt').expanduser()

str(path)
Path(path)

hash(path)

# Other ways to make a path

current_dir = Path.cwd()
home_dir = Path.home()
Path(__file__)

```

## `PurePath` operations

```python
# Let's mess with PurePath operations...
path

path.parts

path.parent
list(path.parents)

path.name
path.with_name('spam.txt')

path.suffix
path.suffixes
path.with_suffix('.zip')

path.stem
path.with_stem('eggs')

path.root
path.drive  # Windows only really...

parent_dir = path.parent
parent_dir.joinpath('data', 'files')
parent_dir / 'data' / 'files'
parent_dir / Path('data') / Path('files')

path.is_relative_to(home_dir)
home_dir in path.absolute().parents
Path('~/demo/files/groceries.txt').is_relative_to(home_dir)
Path('~') == home_dir
path.relative_to(home_dir)
rel_path = path.relative_to(home_dir)
rel_path.absolute()

```

## Messing with directories

```python
# Let's mess with directories...

data_dir = parent_dir / 'data'
data_dir.is_dir()
data_dir.mkdir()
data_dir.mkdir(parents=True, exist_ok=True)
data_dir.is_dir()
list(parent_dir.iterdir())
list(parent_dir.walk())
list(parent_dir.glob('*'))
list(parent_dir.rglob('*'))
data_dir.rmdir()
data_dir.is_dir()
parent_dir.rmdir()
```

## Messing with files

```python
# Let's mess with files...

path.exists()
path.touch()
parent_dir.mkdir(exist_ok=True, parents=True)
path.touch()
path.exists()
path.is_file()
list(parent_dir.rglob('*'))

# What about writing to the file?

with path.open(mode='w', encoding='UTF-8') as f:
    f.write('This is file content')
path.write_text('this is file content', encoding='UTF-8')
path.write_bytes(b'This is file content')

# And reading?

with path.open(mode='r', encoding='UTF-8') as f:
    print(f.read())
path.read_text(encoding='UTF-8')
path.read_bytes()

# What about properties, like size?

s = path.stat()
s.st_size
s.st_mode
new_path = Path('~/demo2/files/groceries.txt').expanduser()
new_path.parent.mkdir(parents=True, exist_ok=True)
path.rename(new_path)
new_path.replace(path)
new_path.unlink(missing_ok=True)

```

## Boolean methods

```python
# And now, the parade of bool methods...

path.exists()
home_dir.exists()
home_dir.is_dir()
home_dir.is_file()
home_dir.is_junction()
home_dir.is_symlink()
home_dir.is_mount()
home_dir.is_socket()
home_dir.is_fifo()
home_dir.is_block_device()
home_dir.is_char_device()
```

## Path traversal attacks and `pathlib`

```python
# ^^^ clear ^^^

# Let's talk about Security, specifically Path Traversal attacks
  # A path traversal attack is when an attacker provides input that causes you to traverse
  # outside the expected directory.

# Scenario 1: Malicious input
user_input = '../../etc/hosts'
(Path.home() / user_input).read_text()  # Whoops...

# Scenario 2: Malicious configuration
p1 = Path('~/secure').expanduser()  # Say you have a directory...
p2 = Path('~/insecure').expanduser()  # ...Meanwhile, there is another secret directory...
p2.mkdir()  # ...which exists...
p1.symlink_to(p2, target_is_directory=True)  # ...and has been nefariously symlinked the first.

# Where are you writing with this?
log_path = p1 / 'files' / 'important.txt'
log_path.absolute()

# This is what resolve is for.
log_path.resolve()
log_path.resolve(strict=True)
(Path.home() / user_input).resolve()
```

## Cleanup

```python
# Now let's cleanup...

def cleanup(*roots: Path | str):
    """Cleanup a path."""
    for root in roots:
        root = Path(root).expanduser()
        for p in [*sorted(root.rglob('*'), reverse=True), root]:
            if not p.exists():
                continue

            # Handle symlinks
            if p.is_symlink():
                print(f'Unlinking {p}')
                p.unlink()

            # Handle files
            elif p.is_file():
                print(f'Deleting file {p}')
                p.unlink()  # Delete file
            
            # Handle folders
            elif p.is_dir():
                print(f'Deleting dir {p}')
                p.rmdir()  # Delete empty dir

cleanup(
    '~/demo', 
    '~/demo2', 
    Path.home() / 'secure', 
    Path.home() / 'insecure'
    )

# So, go play with pathlib!

```