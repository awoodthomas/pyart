"""Example script showing a hardcoded drawing sequence."""
import copy
import cairo
import random
import math
from colorspace import sequential_hcl
from pyart.turtle import Turtle


def snake_graphic(num_seeds, turn_thresh, spawn_thresh, id):
    # Create a turtle on a 512x512 canvas
    canvas_width = 512
    canvas_height = 512
    surface = cairo.ImageSurface(
        cairo.FORMAT_ARGB32, canvas_width, canvas_height)

    ctx = cairo.Context(surface)

    # Set white background
    ctx.set_source_rgb(1.0, 1.0, 1.0)
    ctx.paint()

    stroke = 10

    turtles = []

    colors = sequential_hcl(palette="burg")(num_seeds)

    for i in range(num_seeds):
        turtle = Turtle(ctx=ctx,
                        x=random.randint(1, math.floor(
                            canvas_width / stroke / 2)) * stroke * 2,
                        y=random.randint(1, math.floor(
                            canvas_height / stroke / 2)) * stroke * 2,
                        angle=random.randint(0, 3)*90.0,
                        stroke_width=stroke)
        turtle.set_color(colors[i])
        turtles.append(turtle)

    moves = 0

    while len(turtles) > 0:
        for turtle in turtles:
            moves += 1
            # Create a set of preferred moves, with a chance to prefer to turn
            turn_rand = random.random() - 0.5
            pref_turn = math.copysign(random.randint(10, 45), turn_rand)
            move_list = [0.0, pref_turn, -pref_turn]
            if abs(turn_rand) < turn_thresh:
                move_list = [pref_turn, -pref_turn, 0.0]

            # If move fails, go to the next preferred move
            can_move = False
            for turn_ang in move_list:
                turtle.right(turn_ang)
                if turtle.forward(stroke, True):
                    can_move = True
                    break
                turtle.left(turn_ang)

            if not can_move:
                turtles.remove(turtle)
                break

            # Chance to spawn a new turtle at a right angle to the latest move
            # It needs to be able to make a forward move in an orthogonal direction
            spawn_rand = random.random() - 0.5
            if abs(spawn_rand) < spawn_thresh:
                new_turtle = copy.copy(turtle)
                pref_turn = math.copysign(90, spawn_rand)
                move_list = [pref_turn, -pref_turn]
                success = False
                for turn_ang in move_list:
                    new_turtle.right(turn_ang)
                    if new_turtle.forward(stroke, True):
                        success = True
                        break
                    new_turtle.left(turn_ang)
                if success:
                    turtles.append(new_turtle)

    # Save the drawing
    output_file = f"output_tight/{id}.png"
    surface.write_to_png(output_file)


if __name__ == '__main__':
    generate = 300
    for i in range(generate):
        seeds = random.randint(1, 20)
        turn = random.random() * 0.5 + 0.05
        spawn = random.random() * 0.2 + 0.05
        snake_graphic(seeds,
                      turn,
                      spawn,
                      f"{i}_seeds-{seeds}_turn-{round(turn*100)}_spawn-{round(spawn*100)}")
        if i % (generate / 10) == 0:
            print(f"{round(i / generate * 100)}% complete")
    print("100% complete!")
