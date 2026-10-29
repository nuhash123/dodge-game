# Dodge

A small arcade game made with Python and pygame. Move the green square and
dodge the falling red blocks. The longer you survive, the faster they fall.

## How to play

| Action | Control |
|---|---|
| Move left / right | Arrow keys or A / D |
| Move with mouse or touch | Hold the left mouse button and drag |
| Restart after Game Over | SPACE or click |

Every block you dodge gives you 1 point. The game keeps track of your best score.

## Run it

```bash
pip install -r requirements.txt
python dodge.py
```

Requires Python 3.8 or newer.

## What it demonstrates

- The game loop (events, update, draw, 60 FPS)
- Keyboard and mouse/touch input
- Rectangles, collision detection (`colliderect`)
- Spawning objects with a timer, stored in a list
- Difficulty that increases with the score
- Game states (playing / game over) and restart

## About

Built as a learning project, step by step, with guidance from Claude
(Anthropic's AI assistant). I typed, ran and debugged each step myself.

## License

MIT, see [LICENSE](LICENSE).