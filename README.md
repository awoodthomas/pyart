# PyArt

A crack at some simple generative art, using PyCairo for illustration. "Turtles" can iteratively draw paths - throwback to one of the first computer science courses I ever took!

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

To start, just some 90 degree turns:

<img src="https://github.com/awoodthomas/pyart/blob/master/favorites/279_seeds-9_turn-19_spawn-19.png" width="200"/> <img src="https://github.com/awoodthomas/pyart/blob/master/favorites/287_seeds-3_turn-24_spawn-25.png" width="200"/> <img src="https://github.com/awoodthomas/pyart/blob/master/favorites/188_seeds-2_turn-24_spawn-39.png" width="200"/>

Next, let's go to 45 degree turns. These are some of my favorites. Sparser ones look like metro systems, denser ones look very PCB-esque.

<img src="https://github.com/awoodthomas/pyart/blob/master/favorites/139_seeds-3_turn-7_spawn-6.png" alt="drawing" width="200"/> <img src="https://github.com/awoodthomas/pyart/blob/master/favorites/113_seeds-7_turn-10_spawn-25.png" alt="drawing" width="200"/> <img src="https://github.com/awoodthomas/pyart/blob/master/favorites/159_seeds-3_turn-6_spawn-30.png" alt="drawing" width="200"/>

If we go to 10 degree turns, we get something more like old city streets. Or, if we go to random turn lengths, something more like blood vessels.

<img src="https://github.com/awoodthomas/pyart/blob/master/favorites/131_seeds-1_turn-39_spawn-29.png" alt="drawing" width="200"/> <img src="https://github.com/awoodthomas/pyart/blob/master/favorites/9_seeds-10_turn-14_spawn-28.png" alt="drawing" width="200"/> <img src="https://github.com/awoodthomas/pyart/blob/master/favorites/222_seeds-16_turn-34_spawn-23.png" alt="drawing" width="200"/>

Now let's try some spirals! These turtles are allowed to pass through boundaries until they can resume their spiral.

<img src="https://github.com/awoodthomas/pyart/blob/master/favorites/87_seeds-4_turn-47_spawn-0.png" width="200"/> <img src="https://github.com/awoodthomas/pyart/blob/master/favorites/226_seeds-3_turn-49_spawn-0.png" width="200"/> <img src="https://github.com/awoodthomas/pyart/blob/master/favorites/96_seeds-20_turn-16_spawn-0.png" width="200"/>

If we allow branching on spirals, it gets pretty wild. Low branching probabilities makes this a bit more sane.

<img src="https://github.com/awoodthomas/pyart/blob/master/favorites/2_seeds-1_turn-31_spawn-4.png" width="200"/> <img src="https://github.com/awoodthomas/pyart/blob/master/favorites/102_seeds-1_turn-45_spawn-0.png" width="200"/> <img src="https://github.com/awoodthomas/pyart/blob/master/favorites/104_seeds-1_turn-49_spawn-0.png" width="200"/>
