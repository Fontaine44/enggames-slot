# Pygame Slots
## Pygame-based slot machine easily-changeable symbols, sound effects, and music.

[gif placeholder]

## Features

- Five reels, each with three symbols in play at any given time
- 300x300 png image symbols that are easy to change via Python dictionary
- Easy-to-import audio (commented out by default)
- Basic win animation
- Basic UI

## Tech

Basically just Pygame:

- [Pygame] - Python game library
- Images/Music/Sound effects

## Installation

Pygame and Python are required

```sh
pip install -r requirements.txt
```

From cmd/PowerShell:

```sh
python main.py
```

## Media

I have provided some basic symbols that don't look great but they work well enough.  You can simply add a new directory and create a new symbol dictionary in settings.py to replace them.  Same with audio files!  See comments throughout for more info.

## Win Data
win_data is formatted as such:  
`{1: ['symbol_1', [1, 2, 3]], 3: ['symbol_2', [0, 1, 2]]}` 

## Future Development
I will probably try to recreate this in an actual game engine at some point.  Potential future work includes:
- Better animations
- More win scenarios
- Simulations
- Web version
## License

[Creative Commons 0 License]

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)
   [Pygame]: <https://www.pygame.org/docs/>
   [Creative Commons 0 License]: <https://creativecommons.org/share-your-work/public-domain/cc0/>
   