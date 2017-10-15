# Zombie Survival

2D survival game. Bootstrapped using [pygame_template](https://github.com/alchermd/pygame_template/)


## Project Structure Overview

```
.
├── assets
│   ├── audio
│   └── image
├── gamelib
│   ├── game.py
│   ├── __init__.py
│   ├── palette.py
│   └── sprite.py
├── game.py
```

* `assets/` - contains the assets used in the game.

* `gamelib/game.py` - contains the `Game` class that handles events, game logic, draw functions, and other related functionalities.

* `gamelib/palette.py` - a collection of basic `pygame.Color` objecs.

* `gamelib/sprite.py` - custom sprite objects derived from `pygame.sprite.Sprite`

* `game.py` - initializes the `pygame` engine and loads the `gamelib.game.Game` class.

## License

See [LICENSE](./LICENSE) for more information.