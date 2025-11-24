# PyArt

A crack at some simple generative art, using PyCairo for illustration. "Turtles" can iteratively draw paths. 

`snake.py` - Turtles that have probabilisticly decide to turn or branch off another turtle. Different thresholds for turning, branching, different starting turtle "seeds", and different turn angles generate very different images!

`spiral.py` - Turtles that spiral around! Turtles will quickly collide into edges or other spirals. Currently allows "phasing" - where turtles are allowed to pass through boundaries without drawing for a limited number of steps. Idea for the future: have turtles just make a 180 degree turn (with some width) if they hit something...

## Setup

Install dependencies using Poetry:

```bash
poetry install
```

## Running

```bash
poetry run -m python snake.py
```

## Example Images