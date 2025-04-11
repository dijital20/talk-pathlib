# The `autodemo` Script

## How did this start!

When I finished the first draft of my slides for PyOhio, I had a thought that
slides might be boring. I mean, this is `pathlib`... nothing in my talk relies
on internet connectivity or anything external, so there's no reason I can't just
live demo.

Except for the part where I type like a crazy person... and I worried that I
might eat up time correcting typos.

So... here's a half step. `autodemo` parses a text file, and executes each line
that it finds. Like the REPL, it executes each line, and gives real feedback,
but in a way that could be planned out ahead of time. 

Since my script worked like a workflow, with variables being defined and used 
again later, I felt like it was important to display a local namespace, so that
the audience can keep up with the changes.

Then I added color and style... because who doesn't like color?

So... there's `autodemo.py`. The code is provided as-is with no real warranty.
Fork it, add to it, break it, have fun with it. It was a fun problem to solve.

## How do I use it?

```plaintext
usage: autodemo.py [-h] [--work-dir WORK_DIR] [--timer TIMER] file_path

Execute steps in a file.

positional arguments:
  file_path             Path to execute.

options:
  -h, --help            show this help message and exit
  --work-dir, -w WORK_DIR
                        Working directory.
  --timer, -t TIMER     Advance on this interval rather than taking input.
```

For example, if you have your commands in `commands.txt`, then it's as easy as:

```shell
python autodemo.py commands.txt
```

Easy peasy, right?

I developed and tested this with Python 3.12, but it should work with anything
3.10 an up. It should work in any terminal that supports ANSI escape sequences.

## Plans...

I think I might split this into its own module. The two features I have in mind:

* Support for markdown files. Like, parse the file looking for lines inside
  code fences with type `py` or `python`.
* Maybe using `textual` to do a better UI? It certainly would make some aspects
  easier.

Got other thoughts? Shout at me!