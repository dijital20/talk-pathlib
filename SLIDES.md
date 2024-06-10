---
marp: true
paginate: true
theme: uncover
style: |
    table {
        margin-top: 1em;
        align: center;
    }

    section h1 {
        font-size: 2.5em;
    }

    section.bigcode {
        padding: 1em;
    }

    section.bigcode img {
        margin: 2em;
    }

    section.bigcode pre {
        font-size: 2em;
        padding: 10px;
    }

    section.bigcode h2 {
        text-align: center;
        font-size: 2.5em;
    }
    
---

<!-- 
_class: invert
_footer: ""
_paginate: false
-->

# Hot: `pathlib`, Not: String Paths

Josh Schneider

[@diji@mastodon.social](https://mastodon.social/@diji) - [dijital20@github.com](https://github.com/dijital20)

<!-- 
class: bigcode
 -->

---

## In the beginning, there were string paths...

<!-- 
footer: In the beginning, there were string paths...
_footer: ""
_class: invert bigcode
 -->

---

```py
path = '~/foo/bar/baz.txt'
```

---

```py
import os.path

os.path.abspath(path)  
# '/Users/diji/foo/bar/baz.txt'

os.path.split(path)  
# ('foo/bar', 'baz.txt')
```

---

```py
os.path.exists(path)  
# True

os.path.isdir(path)  
# False

os.path.isfile(path)  
# True
```

---

## Enter `pathlib`

<!-- 
footer: Enter `pathlib`
_footer: ""
_class: invert bigcode
 -->

---

```py
from pathlib import Path

path = Path('~/foo/bar/baz.txt')
```

---

![bg fit](./img/pathlib-inheritance.png)

---

```py
# Current working dir
current_dir = Path.cwd()

# Home dir
home = Path.home()

# Current module
current_module = Path(__file__)
```

---

## Let's play with (pure) paths...

<!-- 
footer: Let's play with (pure) paths...
_footer: ""
_class: invert bigcode
 -->

---

```py
path.name
# 'baz.txt'

path.stem
# 'baz'

path.suffix
# '.txt'
```

---

```py
path.parent
# PosixPath('~/foo/bar')

list(path.parents)
# [
#   PosixPath('~/foo/bar'), 
#   PosixPath('~/foo'), 
#   PosixPath('~'),
#   PosixPath('.')
# ]
```

---

```py
path.expanduser()
# PosixPath('/Users/diji/foo/bar/baz.txt')
# Expands ~

path.absolute()
# PosixPath('/Users/diji/foo/bar/baz.txt')
# Gets absolute based on current working dir

path.resolve()
# PosixPath('/Users/diji/foo/bar/baz.txt')
# Follows symlinks to the source
```

---

```py
path.exists()
# True

path.is_dir()
# False

path.is_file()
# True

path.is_junction()
# False

path.is_symlink()
# False
```

---

![bg fit right](./img/theyre-the-same-picture.jpg)

```py
dir = path.parent

data_dir = dir.joinpath('data')
# PosixPath('~/foo/bar/data')

data_dir = dir / 'data'
# PosixPath('~/foo/bar/data')
```

---

## Let's mess with directories...

<!-- 
footer: Let's mess with directories...
_footer: ""
_class: invert bigcode
 -->

---

```py
data_dir.mkdir(parents=True, exist_ok=True)
# Path, including parents, created... 
#  with no error if it already exists
```

---

```py
list(dir.walk())
# [PosixPath('~/foo/bar/data')]
# Walk the structure, returning each Path object
#  New in Python 3.12!

list(dir.glob('*'))
# [PosixPath('~/foo/bar/data')]
# Get all of the Path objects in the current folder

list(dir.rglob('*'))
# [PosixPath('~/foo/bar/data')]
# Get all of the Path objects in the current folder
#  and subfolders
```

---

```py
data_dir.rmdir()
# Delete it (but only if it is empty)!
```

---

## How about files now...

<!-- 
footer: How about files now...
_footer: ""
_class: invert bigcode
 -->

---

```py
path.touch()
# Create the file with no contents.

list(dir.rglob('*'))
# [PosixPath('~/foo/bar/baz.txt')]
```

---

```py

path.read_text(encoding='UTF-8')
# ''

path.read_bytes()
# b''

with path.open(mode='r', encoding='UTF-8') as f:
    f.read()
# ''
```
---

```py
path.write_text(
    'this is file content', encoding='UTF-8'
)

path.write_bytes(b'This is file content')

with path.open(mode='r', encoding='UTF-8') as f:
    f.write('This is file content')
```

---

```py
s = path.stat()

s.st_size
# 20

s.st_mode
# 33188
```

---

```py
new_path = Path('~/foo2/bar/baz.txt')
new_path.parent.mkdir(parents=True, exist_ok=True)

path.rename(new_path)
# PosixPath('~/foo2/bar/baz.txt')

new_path.replace(path)
# PosixPath('~/foo/bar/baz.txt')

new_path.unlink()
# Delete file
```

---

```py
for p in dir.walk(topdown=False):
    if p.is_file():
        p.unlink()  # Delete file
    
    elif p.is_dir():
        p.rmdir()  # Delete empty dir

list(dir.rglob('*'))
# []
```

---

## Documentation

[Pathlib - Object-oriented filesystem paths](https://docs.python.org/3/library/pathlib.html)

<!-- 
footer: More information...
_footer: ""
_class: invert bigcode
 -->
