# PyOhio 2024 - Hot: `pathlib`, Not: String Paths

```python
# 
    # hot: pathlib, not: string paths
    #
    # Josh Schneider
    # dijital20@github.com @diji@mastodon.social
    #
    # PyTexas Conference Organizer
    # https://pytexas.org/2025
    #
    # PyTexas Virtual Meetup Organizer and Host
    # https://pytexas.org/meetup

```

## In the beginning, there were string paths...

```python

# Let's start with string paths...
path = '~/foo/bar/baz.txt'
path

# Look at how boring that is!

import os.path  # We need this guy to even work with them

os.path.abspath(path)

path = os.path.expanduser(path)
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

```python
import pathlib

path = pathlib.Path('~/foo/bar/baz.txt')

type(path)  # Wait, what type?
type(path).__mro__  # What are its ancestors?

pure_path_members = {
    f'{n}()' if callable(v) else n 
    for n, v in vars(pathlib.PurePath).items() 
    if not n.startswith('_')}

path_members = {
    f'{n}()' if callable(v) else n
    for n, v in vars(pathlib.Path).items() 
    if not n.startswith('_')}

sorted(pure_path_members)
sorted(path_members - pure_path_members)
```

## Making `Path` objects

```python
from pathlib import Path

path = Path('~/foo/bar/baz.txt').expanduser()

str(path)
Path(path)

hash(path)

# Other ways to make a path

current_dir = Path.cwd()
home_dir = Path.home()
Path(__file__)
```

## `PurePath` and `Path`

```python
# Let's mess with PurePath operations...
# Paths have parts and parents

path
path.parts
path.parent
list(path.parents)

# The last segment of a path has parts of its own

path.name
path.stem
path.suffix
path.suffixes

# More attributes
path.root
path.drive

# With methods to change them

path.with_name("spam.txt")
path.with_stem("eggs")
path.with_suffix(".zip")

# Let's mutate the path some
rel_path = path.relative_to(home_dir)
rel_path.absolute()
rel_path.resolve()

# More path operations...

parent_dir = path.parent
data_dir = parent_dir.joinpath("data")
data_dir = parent_dir / "data"

path.is_relative_to(home_dir)
home_dir in path.absolute().parents
Path('~/foo/bar/baz.txt').is_relative_to(home_dir)

Path('~') == home_dir

path.relative_to(home_dir)
```

## Messing with directories

```python
# Let's mess with directories...

data_dir.is_dir()
data_dir.mkdir()
data_dir.mkdir(parents=True, exist_ok=True)
data_dir.is_dir()
list(parent_dir.iterdir())
list(parent_dir.walk())
list(parent_dir.glob("*"))
list(parent_dir.rglob("*"))
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
list(parent_dir.rglob("*"))

# What about writing to the file?

with path.open(mode="w", encoding="UTF-8") as f:
    f.write("This is file content")
path.write_text("this is file content", encoding="UTF-8")
path.write_bytes(b"This is file content")

# And reading?

with path.open(mode="r", encoding="UTF-8") as f:
    print(f.read())
path.read_text(encoding="UTF-8")
path.read_bytes()

# What about properties, like size?

s = path.stat()
s.st_size
s.st_mode
new_path = Path("~/foo2/bar/baz.txt")
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

## Cleanup

```python
# Now let's cleanup...

def cleanup(root: Path):
    """Cleanup a path."""
    for p in [*sorted(root.rglob("*"), reverse=True), root]:
        
        # Handle files
        if p.is_file():
            print(f"Deleting file {p}")
            p.unlink()  # Delete file
        
        # Handle folders
        elif p.is_dir():
            print(f"Deleting dir {p}")
            p.rmdir()  # Delete empty dir

cleanup(parent_dir)
list(parent_dir.rglob("*"))
parent_dir.exists()

# So, go play with pathlib!
```
