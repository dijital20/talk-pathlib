# Submission

## Description

Have you seen `pathlib`?  If not, once I show you, you will never go back to string paths and `os.path` ever again! `pathlib` turns paths into path objects, which have attributes and methods that cover a number of operations. In this talk, we will:

- Talk about how to create `Path` objects, and how this differs on Windows vs Mac/Linux
- Talk about the many properties of pure paths
- Talk about folder operations from `Path` objects, such as creating directory structures and recursive globbing.
- Talk about file operations, made simpler with `Path` objects, such as reading contents, getting properties like file size, and deleting.

Stop messing with string paths and get with `pathlib`!

## Objective

Explain how everything you can do with string paths and `os.path` can be done much easier using `pathlib.Path`, and why it should be your default for working with filesystem paths going forward.

## Outline

- Creating a `Path` object.
    - The separation between `PurePath` and `Path` implementations.
    - The magic that Python does when using `Path()` on different platforms.
    - `Path.cwd()` and `Path.home()`
- Attributes of a `Path`
    - `name`, `stem`, `suffix`, `parent`, and `parents`
    - `stat()` and its attributes
    - `expanduser()`for expanding `~` and `resolve()` for canonicalizing paths
    - `exists()`, `is_dir()`, `is_file()`, `is_junction()`, `is_mount()`, and `is_symlink()` to figure out what a a path is.
- Directory operations
    - `mkdir()` and its amazing keyword arguments
    - `glob()` and `rglob()`to search for more paths
    - `rmdir()`
- File operations
    - `write_text()` and `write_bytes()`
    - `read_text()` and `read_bytes()`
    - `open()`
    - `replace()` and `rename()`
    - `unlink()`