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

<!-- 
    Speaker Notes:
    Of course, `os.path` has functions to managing string paths, but annoyingly, you have to pass the paths all over the
    place and keep up with the changes.

    For instance, `abspath` here to get the absolute version of a path or `split` to split the last segment from the 
    rest of the path.
 -->

---

```py
os.path.exists(path)  
# True

os.path.isdir(path)  
# False

os.path.isfile(path)  
# True
```

<!-- 
    Speaker notes:
    We also have a number of boolean functions, which can answer questions about a path, but again, you have to pass
    the paths all over the place.
 -->

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

<!-- 
    Speaker notes:
    In `pathlib`, we have `Path` objects, which represent a path. These objects have methods and attributes relevant
    to that path, making it so you don't have to pass the paths all over the place.
 -->

---

![bg fit](./img/pathlib-inheritance.png)

<!-- 
    Speaker notes:
    There's actually 2 classes at play here... `Path` and `PurePath`. `Path` is a subclass of `PurePath`, so it has all
    of its powers and then some. In most cases, you will use `Path`, but in cases where you are only worried about
    operations on the path itself (and not what it points to), you can use `PurePath.

    When you create a `Path` or `PurePath` object, you actually get back an object relevant to the OS that you are
    executing on:

    Windows: `PureWindowsPath` and `WindowsPath`
    Linux and Mac OS: `PurePosixPath` and `PosixPath`

    This allows your code to remain platform agnostic. Each set of classes knows how to handle the paths on its 
    platforms (such as path separators, how operations are performed, etc.).
 -->

---

```py
# Current working dir
current_dir = Path.cwd()

# Home dir
home = Path.home()

# Current module
current_module = Path(__file__)
```

<!-- 
    Speaker notes:
    `Path` provides some other classmethods for initializing objects from certain locations. Also, you can use `Path`
    with `__file__` to get a path to the current module.
 -->

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

<!-- 
    Speaker notes:
    `Path` objects have attributes for getting useful parts of a path.

    `Path.name` can get the name of the last segment of the path.
    `Path.stem` gives you the name of that last segment without the file extension.
    `Path.suffix` gives you the file name's extension without the name.
 -->

---

```py
path.with_name('spam.txt')
# PosixPath('~/foo/bar/spam.txt')

path.with_stem('eggs')
# PosixPath('~/foo/bar/eggs.txt')

path.with_suffix('.zip')
# PosixPath('~/foo/bar/baz.zip')
```

<!-- 
    Speaker notes:
    Just like we have attributes for `name`, `stem`, and `suffix`, we have "with methods" to change just those parts
    of the path.
 -->

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

<!-- 
    Speaker notes:
    `Path.parent` can give you a path object for the path containing the last segment. Since it returns a path object,
    this can be chained. `path.parent` gives you the containing folder, `path.parent.parent` giving you the grandfather
    folder, and `path.parent.name` to give you the name of the containing folder.

    `Path.parents` can give you a list of all of the ancestor paths, so that you don't need to add repeated `.parent`
    calls.
 -->

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

path = path.resolve()
```

<!-- 
    Speaker notes:
    `Path` also provides some methods for giving you transformed paths. For instance, `expanduser()` will expand the 
    `~` to the user's home folder (this works on Windows too for giving you %USERPROFILE%).

    `Path.absolute()` will give you an absolute path if the path is a relative paths, but does not resolve symlinks.

    `Path.resolve()` does that `absolute()` does, but also resolves symbolic links, returning you a "canonical" path
    to the item in question. Adding `strict=True` to a `resolve()` call will cause it to raise an exception if the path
    does not exist.

    For good security, you should ALWAYS call `resolve()` on path objects before using them.
 -->

---

```py
path.exists()
path.is_dir()
path.is_file()
path.is_junction()
path.is_symlink()
path.is_mount()
path.is_socket()
path.is_fifo()
path.is_block_device()
path.is_char_device()
```

<!-- 
    Speaker notes:
    `Path` objects also have boolean methods for telling you things about the path in question. This can help determine
    information about the path so that you can use it appropriately.
 -->

---

![bg fit right](./img/theyre-the-same-picture.jpg)

```py
parent_dir = path.parent

data_dir = parent_dir.joinpath('data')
# PosixPath('~/foo/bar/data')

data_dir = parent_dir / 'data'
# PosixPath('~/foo/bar/data')
```

<!-- 
    Speaker notes:
    `Path` objects also give you novel ways to create new paths from path objects. Like we mentioned, you can use 
    `.parent` to get the parent path. You can use `joinpath` to extend the path by a path segment as a string, or better
    use the `/` operator to combine paths. While it seems a little unorthodox to use the / operator, it makes sense
    when you see paths written in this manner.
 -->

---

```py
path.is_relative_to(home)
# True

home in path.absolute().parents
# True

path.relative_to(home)
# PosixPath('foo/bar')
```

<!-- 
    Speaker notes:
    The `is_relative_to()` method tests if the path is relative to another path... whether they share ancestry.
    This method was added in Python 3.9, but looks like it is being deprecated in 3.12 for removal in 3.14. 
    
    You can use the parents to get the set of parent path structures, and test for membership. Since `parents` works off
    of the `Path` without talking to the filesystem, you may want to either `absolute()` or `resolve()` the path first.

    You can use `relative_to()` to get a relative path. This will raise an exception if the paths are not relative to 
    each other.
 -->

---

## Let's mess with directories...

<!-- 
footer: Let's mess with directories...
_footer: ""
_class: invert bigcode
 -->

---

```py
data_dir.is_dir()
# False

data_dir.mkdir(parents=True, exist_ok=True)
# Path, including parents, created... 
#  with no error if it already exists

data_dir.is_dir()
# True
```

<!-- 
    Speaker notes:
    The `mkdir()` method can create a directory for the current path. What's very cool are the options:
    - `parents=True` will tell it to create any ancestor paths that do not exist in between.
    - `exist_ok=True` will tell it to not throw an error if the path already exists as a directory.
    These two options handle 90% of the errors you would get from this operation, and make it very easy to use.
 -->

---

```py
list(parent_dir.iterdir())
# [PosixPath('~/foo/bar/data')]
# Get all of the Path objects in the current folder.

list(parent_dir.walk())
# [PosixPath('~/foo/bar/data')]
# Walk the structure, returning each Path object
#  New in Python 3.12!

list(parent_dir.glob('*'))
# [PosixPath('~/foo/bar/data')]
# Get all of the Path objects in the current folder

list(parent_dir.rglob('*'))
# [PosixPath('~/foo/bar/data')]
# Get all of the Path objects in the current folder
#  and subfolders
```

<!-- 
    Speaker notes:
    The `walk()` method is new in Python 3.12, and gives us an alternative to `os.walk`. This walks the path structure
    returning each item encountered (whether file, folder, symlink, junction, etc.) along the way. Passing 
    `topdown=False` will cause it to process bottom-up, returning the deepest objects first and the most shallow last.
    More on that shortly.

    `glob()` and `rglob()` return path objects that match the glob pattern. `glob()` returns only things in the current
    path, while `rglob()` combs recursively through subdirectories. Each item is returned as a `Path` object.
 -->

---

```py
data_dir.rmdir()
# Delete it (but only if it is empty)!
```

<!-- 
    Speaker notes:
    Finally, we have `rmdir()`, which deletes the directory. This will raise an exception if the directory is not empty,
    so make sure you clean things out of the directory first.
 -->

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

<!-- 
    Speaker notes:
    If you've worked on POSIX operating systems, then you know the `touch` command. The `touch()` method does the same
    thing... creates an empty file.
 -->

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

<!-- 
    Speaker notes:
    `Path` provides some simple methods for reading file contents. You can use the `read_text()` method to read the
    file's contents to a string, or `read_bytes()` to read the file's contents as a bytes object. These are convenient
    if you want to get all of the file's contents at once.

    `Path` also provides `open()`, which works just like the built-in `open()` function, except since you are calling
    it off the path, you don't need to pass the path in. This makes it easy and convenient to open files.
 -->

---

```py
path.write_text(
    'this is file content', encoding='UTF-8'
)

path.write_bytes(b'This is file content')

with path.open(mode='w', encoding='UTF-8') as f:
    f.write('This is file content')
```

<!-- 
    Speaker notes:
    Just like we did for reading, we have convienent methods to write. `write_text()` writes a string to file, while
    `write_bytes` writes bytes to the file, and `open()` is still there to open the file yourself.
 -->

---

```py
s = path.stat()

s.st_size
# 20

s.st_mode
# 33188
```

<!-- 
    Speaker notes:
    The `stat()` method gets statistics about the file, such as the timestamps (created, modified, etc.), size, mode, 
    etc. This is convenient for getting the size of a file very quickly.
 -->

---

```py
new_path = Path('~/foo2/bar/baz.txt')
new_path.parent.mkdir(parents=True, exist_ok=True)

path.rename(new_path)
# PosixPath('~/foo2/bar/baz.txt')
# This will error if the destination already exists.

new_path.replace(path)
# PosixPath('~/foo/bar/baz.txt')
# This will not error, it will just overwrite.

new_path.unlink(missing_ok=True)
# Delete file
```

<!-- 
    Speaker notes:
    We can also easily rename or replace files. `rename()` renames the item referenced by the calling `Path` object
    with the one passed to the function.
 -->

---

```py
for p in [*parent_dir.walk(topdown=False), parent_dir]:
    if p.is_file():
        p.unlink()  # Delete file
    
    elif p.is_dir():
        p.rmdir()  # Delete empty dir

list(parent_dir.rglob('*'))
# []

parent_dir.exists()
# False
```

<!-- 
    Speaker notes:
    Combining all of this, let's use everything we've learned to clean up. We use `walk()` to walk the structure in a
    depth-first manner (we do this so we get to files before their parent folders). If the `Path` points to a file, 
    call `unlink()` to delete it. If the `Path` is a directory, then call `rmdir()` to remove it (if we've successfully
    deleted child folders, then this should succeed). We also tossed in the parent directory so that the containing
    folder would be cleaned up too.
    
    At the end, the folder should be empty.
 -->

---

## Documentation

[Pathlib - Object-oriented filesystem paths](https://docs.python.org/3/library/pathlib.html)

<!-- 
footer: More information...
_footer: ""
_class: invert bigcode
 -->
