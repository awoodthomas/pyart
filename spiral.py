import copy
import cairo
import random
import math
import numpy as np
import matplotlib.pyplot as plt
from colorspace import sequential_hcl
from pyart.turtle import Turtle


def snake_graphic(num_seeds, spawn_thresh, id, animate=False):
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
                        stroke_width=stroke,
                        pref_turn=50,
                        phaser=True)
        turtle.set_color(colors[i])
        # turtle.set_color("#000000")
        turtles.append(turtle)

    # Set up animation if requested
    if animate:
        plt.ion()  # Turn on interactive mode
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.set_title("Drawing Animation")
        ax.axis('off')
        im = ax.imshow(
            np.zeros((canvas_height, canvas_width, 3)), origin='upper')
        plt.tight_layout()
        plt.show(block=False)

    # Draw a square
    moves = 0
    update_interval = 10  # Update display every N moves

    step_size = stroke * 0.5

    def update_display():
        """Convert Cairo surface to numpy array and update matplotlib display."""
        if not animate:
            return
        # Get surface data
        buf = surface.get_data()
        arr = np.frombuffer(buf, np.uint8)
        stride = surface.get_stride()
        # Reshape accounting for stride (bytes per row, may have padding)
        arr = arr.reshape((canvas_height, stride))[
            :, :canvas_width * 4].reshape((canvas_height, canvas_width, 4))
        # Convert ARGB to RGB
        # For ARGB32 on little-endian: bytes in memory are B, G, R, A
        rgb = arr[:, :, [2, 1, 0]]  # Extract R, G, B channels (skip alpha)
        im.set_array(rgb)
        fig.canvas.draw()
        fig.canvas.flush_events()
        plt.pause(0.001)  # Small pause to allow GUI to update

    while len(turtles) > 0:
        moves += 1
        for turtle in turtles:
            # Create a set of preferred moves, with a chance to prefer to turn
            move_list = [turtle.pref_turn]

            # Attempt to move forward at least 2x stroke width without hitting line or edge
            # If move fails, go to the next preferred move
            can_move = False
            for turn_ang in move_list:
                turtle.right(turn_ang)
                if turtle.forward(step_size, True):
                    can_move = True
                    break
                turtle.left(turn_ang)

            # Based on the tailor expansion of the arc equation, how much to step out each time to achieve an intra-spiral spacing of 2x stroke
            turtle.pref_turn = turtle.pref_turn - \
                math.degrees((2*stroke)/(step_size*2*math.pi) *
                             math.pow(math.radians(turtle.pref_turn), 3))

            if not can_move:
                turtles.remove(turtle)
                break

            # Chance to spawn a new turtle at a right angle to the latest move
            # It needs to be able to make a forward move in an orthogonal direction
            spawn_rand = random.random() - 0.5
            if abs(spawn_rand) < spawn_thresh and turtle.phase_count == 0:
                new_turtle = copy.copy(turtle)
                pref_turn = math.copysign(90, -turtle.pref_turn)
                move_list = [pref_turn]
                success = False
                for turn_ang in move_list:
                    new_turtle.right(turn_ang)
                    if new_turtle.forward(stroke, True):
                        success = True
                        break
                    new_turtle.left(turn_ang)
                if success:
                    turtles.append(new_turtle)

        # Update animation display periodically
        if animate and moves % update_interval == 0:
            update_display()

    # Final update to show completed image
    if animate:
        update_display()
        plt.ioff()  # Turn off interactive mode
        plt.show(block=True)  # Keep window open until user closes it

    # Save the drawing
    output_file = f"spiral/{id}.png"
    surface.write_to_png(output_file)
    # print(f"\nDrawing saved to {output_file}")


if __name__ == '__main__':
    generate = 1
    animate = True  # Set to True to see animation, False to skip
    for i in range(generate):
        seeds = random.randint(1, 20)
        turn = random.random() * 0.5 + 0.05
        spawn = 0  # random.random() * 0.02
        snake_graphic(seeds,
                      spawn,
                      f"10{i}_seeds-{seeds}_turn-{round(turn*100)}_spawn-{round(spawn*100)}",
                      animate=animate and i == 0)  # Only animate the first one
        if i % (generate / 10) == 0:
            print(f"{round(i / generate * 100)}% complete")
    print("100% complete!")
