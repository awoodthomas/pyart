"""Turtle graphics object using pycairo for drawing."""

import math
import cairo


class Turtle:
    """A turtle that can draw on a cairo surface."""

    def __init__(self,
                 ctx: cairo.Context, x: float, y: float, angle: float,
                 stroke_width: float = 1.0, pref_turn: float = 0.0,
                 phaser: bool = False):
        """Initialize the turtle at the center of the canvas.

        Args:
            ctx: Cairo context to draw on
            x, y, angle: Initial position and angle of the turtle
            stroke_width: Width of the drawing stroke
            pref_turn: Preferred turn direction in degrees (used for spirals)
            phaser: If True, enable phaser mode, allows passing through drawn lines
        """
        surface = ctx.get_target()
        self.canvas_width = surface.get_width()
        self.canvas_height = surface.get_height()
        self.surface = surface  # Store surface reference for pixel access

        self.ctx = ctx  # Use the passed-in context directly

        # Initialize turtle state
        self.x = x
        self.y = y
        self.angle = angle  # Angle in degrees, 0 = right, 90 = up
        self.pen_down = True
        self.color = (0.0, 0.0, 0.0)  # RGB tuple, default black
        self.stroke_width = stroke_width
        self.pref_turn = pref_turn
        self.phaser = phaser
        self.phase_count = 0

        # Move to starting position
        self.ctx.move_to(self.x, self.y)
        self._update_color()

    def forward(self, distance: float = 1.0, check: bool = False):
        """Move the turtle forward by the specified distance.

        Args:
            distance: Distance to move forward in pixels
            check: If True, check for collisions before moving
        """
        # Calculate new position based on angle
        angle_rad = math.radians(self.angle)
        new_x = self.x + distance * math.cos(angle_rad)
        new_y = self.y - distance * math.sin(angle_rad)

        # Check if pixels at the target position are already drawn
        # If phasing, also check the current position
        if check and (
                self._check_point_collision(new_x, new_y, self.stroke_width) or (
                    self.phase_count > 0 and self._check_point_collision(
                        self.x, self.y, self.stroke_width, True)
                )):

            if not self.phaser or self.phase_count > 500:
                return False
            self.phase_count += 1
            self.penup()
        else:
            self.phase_count = 0
            self.pendown()

        if self.pen_down:
            self.ctx.move_to(self.x, self.y)
            self.ctx.line_to(new_x, new_y)
            self._update_color()
            self.ctx.stroke()

        self.x = new_x
        self.y = new_y
        return True

    def right(self, degrees: float = 90.0):
        """Turn the turtle right (clockwise).

        Args:
            degrees: Number of degrees to turn
        """
        self.angle -= degrees
        self.angle = self.angle % 360.0

    def left(self, degrees: float = 90.0):
        """Turn the turtle left (counter-clockwise).

        Args:
            degrees: Number of degrees to turn
        """
        self.angle += degrees
        self.angle = self.angle % 360.0

    def penup(self):
        """Lift the pen so the turtle doesn't draw while moving."""
        self.pen_down = False

    def pendown(self):
        """Lower the pen so the turtle draws while moving."""
        self.pen_down = True
        # Move to current position to start a new path
        self.ctx.move_to(self.x, self.y)

    def set_color(self, color):
        """Set the drawing color.

        Args:
            color: Color as hex string (e.g., "#FF0000" for red) or RGB tuple (0.0-1.0)
        """
        if isinstance(color, str):
            # Parse hex color
            color = color.lstrip('#')
            r = int(color[0:2], 16) / 255.0
            g = int(color[2:4], 16) / 255.0
            b = int(color[4:6], 16) / 255.0
            self.color = (r, g, b)
        else:
            self.color = color
        self._update_color()

    def goto(self, x: float, y: float):
        """Move the turtle to a specific position.

        Args:
            x: Target x coordinate
            y: Target y coordinate
        """
        if self.pen_down:
            self.ctx.line_to(x, y)
            self.ctx.stroke()
            self.ctx.move_to(x, y)
        else:
            self.ctx.move_to(x, y)

        self.x = x
        self.y = y

    def _check_point_collision(self, x: float, y: float, margin: float, all_around: bool = False) -> bool:
        """Check if pixels at the endpoint (with margin) are already drawn.

        Args:
            x, y: endpoint, rounded to an int
            margin: amount to check around the endpoint, rounded to an int
            all_around: If True, check all around the point; if False, check only forward semicircle

        Returns:
            True if collision detected (pixels are already drawn), False otherwise
        """
        x = round(x)
        y = round(y)
        margin = round(margin)

        # Use the turtle's current angle as the forward direction
        forward_angle = self.angle
        ang = 180 if all_around else 90

        # Check from -90 to +90 degrees relative to the forward direction
        for theta_deg in range(-ang, ang+1, 30):
            # Calculate angle relative to forward direction
            check_angle_deg = forward_angle + theta_deg
            check_angle_rad = math.radians(check_angle_deg)

            # Calculate check position: endpoint + margin in the check direction
            # Note: y increases downward, so we use negative sin for y
            check_x = round(x + margin * math.cos(check_angle_rad))
            check_y = round(y - margin * math.sin(check_angle_rad))

            if self._check_pixel_collision(check_x, check_y):
                return True

        return False

    def _check_pixel_collision(self, check_x: int, check_y: int) -> bool:
        # Get pixel data from surface
        stride = self.surface.get_stride()
        data = self.surface.get_data()

        if check_x < 0 or check_x >= self.canvas_width:
            return True
        if check_y < 0 or check_y >= self.canvas_height:
            return True

        # Get pixel index (ARGB32 format: 4 bytes per pixel)
        pixel_index = check_y * stride + check_x * 4
        if pixel_index + 3 >= len(data):
            return True

        # Read ARGB values
        # For ARGB32 on little-endian: bytes are B, G, R, A
        # But we need to account for premultiplied alpha in Cairo
        b = data[pixel_index]
        g = data[pixel_index + 1]
        r = data[pixel_index + 2]
        a = data[pixel_index + 3]

        # Check if pixel is not white (has been drawn on)
        # White background is (255, 255, 255, 255) or close to it
        # We consider it a collision if the pixel is significantly darker than white
        # Account for premultiplied alpha: if alpha < 255, colors are already scaled
        if a > 0:
            # If alpha is not full, check if the pixel is non-white
            # For premultiplied alpha, we need to check the actual color
            if a < 255:
                # Premultiplied: if alpha is low, it's likely drawn
                if a > 10:  # Not fully transparent
                    return True
            else:
                # Full alpha, check RGB values directly
                if r < 250 or g < 250 or b < 250:
                    return True
        return False

    def _update_color(self):
        """Update the cairo context with the current color."""
        self.ctx.set_source_rgb(*self.color)
        self.ctx.set_line_width(self.stroke_width)
        self.ctx.set_line_cap(cairo.LINE_CAP_ROUND)
