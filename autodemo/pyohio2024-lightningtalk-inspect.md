# PyOhio 2024 Lightning Talk - Inspect is fun!

```python
# 
    # Inspect is fun!
    #
    # Josh Schneider
    # dijital20@github.com @diji@mastodon.social
    #
    # PyTexas Conference Organizer
    # https://pytexas.org/2025
    #
    # PyTexas Virtual Meetup Organizer and Host
    # https://pytexas.org/meetup```
```

## Sample function

```python
def announce(
        text: str,
        *more_text: str, 
        title: str | None = None, 
        header_char: str = '=',
        headers: bool = False,
        width: int = 80,
    ) -> str:
    output = ''
    if title:
        output += f'{header_char} {title} {header_char * (width - len(title) - 3)}\n'
    elif headers:
        output += header_char * width + '\n'

    output += '\n'.join((text, *more_text)) + '\n'

    if title or headers:
        output += header_char * width + '\n'
    
    return output

print(announce('Hi there', 'How are you?'))

print(announce('Hi there', title='Josh'))

print(announce('Hi there', 'How are you?', headers=True, header_char='*'))
```

## Inspect the signature of a function

```python
import inspect

# Get the signature of a function
sig = inspect.signature(announce)
sig.parameters  # List parameters
sig.parameters['header_char']  # Get a single parameter
sig.parameters['header_char'].name
sig.parameters['header_char'].annotation
sig.parameters['header_char'].default

```

## Get the call args of a function

```python
# Get the call arguments of a function
inspect.getcallargs(announce, 'Hi there', 'How are you?')
inspect.getcallargs(announce, 'Hi there', title='Josh')
inspect.getcallargs(announce, 'Hi there', 'How are you?', headers=True, header_char='*')
```

## Test what an object is with predicates

```python
# Test what something is
inspect.isfunction(announce)
inspect.isclass(announce)
```

## Look at the stack and frames

```python
# Take a look at the stack and frames

inspect.stack()

f = inspect.currentframe()
f
f.f_locals
f.f_globals

# There's more, so get exploring!
```
