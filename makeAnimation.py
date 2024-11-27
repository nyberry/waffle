def makeAnimation(original, target, swaps, animationFilename):

    from PIL import Image, ImageDraw, ImageFont
    import cv2
    import imageio

    def draw_waffle_puzzle(
        state, target, colors, swap=None, frame=None, number_of_frames=12
    ):

        # appearance variables
        grid_size = 5
        cell_size = 25
        line_width = 2
        font_size = 13
        img_size = grid_size * cell_size

        # Create a blank white image
        img = Image.new("RGB", (img_size, img_size), "black")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", font_size)

        # Draw the whole grid except the animated tiles
        for row in range(grid_size):
            for col in range(grid_size):
                idx = row * 5 + col
                if idx not in swap:
                    letter = state[idx]  # Get letter for this tile
                    target_letter = target[idx]
                    x0, y0 = col * cell_size, row * cell_size  # Top-left corner of the cell
                    x1, y1 = (
                        x0 + cell_size,
                        y0 + cell_size,
                    )  # Bottom-right corner of the cell
                    draw_tile(
                        x0,
                        y0,
                        x1,
                        y1,
                        colors[idx],
                        letter,
                        img,
                        draw,
                        cell_size,
                        line_width,
                        font,
                    )

        # draw the animated tiles
        for pair in [(swap[0], swap[1]), (swap[1], swap[0])]:
            idx = pair[0]
            target_idx = pair[1]
            start_row = int(idx / 5)
            start_col = idx % 5
            end_row = int(target_idx / 5)
            end_col = target_idx % 5
            col = start_col + (end_col - start_col) * (frame / (number_of_frames - 1))
            row = start_row + (end_row - start_row) * (frame / (number_of_frames - 1))
            letter = state[idx]
            bg_color = colors[idx]
            x0, y0 = int(col * cell_size), int(
                row * cell_size
            )  # Top-left corner of the cell
            x1, y1 = x0 + cell_size, y0 + cell_size  # Bottom-right corner of the cell
            draw_tile(
                x0, y0, x1, y1, bg_color, letter, img, draw, cell_size, line_width, font
            )

        return img


    def draw_tile(x0, y0, x1, y1, bg_color, letter, img, draw, cell_size, line_width, font):
        # Draw the background rectangle
        draw.rectangle([x0, y0, x1, y1], fill=bg_color)

        # Draw the grid lines (to ensure they're visible on colored backgrounds)
        draw.rectangle([x0, y0, x1, y1], outline="black", width=line_width)

        # Draw the letter in the center of the tile
        text_x = x0 + 2 + cell_size // 4
        text_y = y0 + cell_size // 4
        draw.text((text_x, text_y), letter, fill="black", font=font)

    def determine_background_colors(state, target, scan_if_yellow):
        colors = []
        for i in range(25):
            if state[i] == " ":
                bg_color = "black"
            elif state[i] == target[i]:
                bg_color = "green"
            else:
                matchingLetters = 0
                for j in scan_if_yellow[i]:
                    if target[j] == state[i]:
                        matchingLetters += 1
                        if j < len(colors):
                            if colors[j] == "green" or colors[j] == "yellow":
                                matchingLetters -= 1
                    if matchingLetters:
                        bg_color = "yellow"
                    else:
                        bg_color = "grey"

            colors.append(bg_color)
        return colors


    # transform lists to grid form
    for i in [15, 14, 7, 6]:
        original.insert(i, " ")
        target.insert(i, " ")

    # transform the list of swaps
    def adjust_value(value):
        if value >= 15:
            return value + 4
        elif value >= 14:
            return value + 3
        elif value >= 7:
            return value + 2
        elif value >= 6:
            return value + 1
        return value

    # Apply the function to each value in the list of tuples
    swaps = [(adjust_value(x), adjust_value(y)) for x, y in swaps]

    # add start and end frames
    swap_frames = [(0, 0)] + swaps + [(0, 0)]

    scan_if_yellow = {}
    for row in range(5):
        for col in range(5):
            yellows = []
            idx = row * 5 + col
            if row in [0, 2, 4]:
                for i in range(0, 5):
                    if i != col:
                        yellows.append(row * 5 + i)
            if col in [0, 2, 4]:
                for i in range(0, 5):
                    if i != row:
                        yellows.append(col + i * 5)
            scan_if_yellow[idx] = yellows

    number_of_frames = 15

    # Create the puzzle and show it
    state = original
    frames = []

    for swap in swap_frames:
        colors = determine_background_colors(state, target, scan_if_yellow)
        for frame in range(number_of_frames):
            frames.append(
                draw_waffle_puzzle(state, target, colors, swap, frame, number_of_frames)
            )
        state[swap[0]], state[swap[1]] = state[swap[1]], state[swap[0]]
    frame_one = frames[0]
    frame_one.save(
        animationFilename+".gif",
        format="GIF",
        append_images=frames,
        save_all=True,
        duration=100,
        loop=0,
    )
    print (f"GIF created: {animationFilename}.gif")

    # Read the GIF using imageio
    gif = imageio.mimread(f'{animationFilename}.gif')
    height, width, _ = gif[0].shape

    # Define codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Codec for MP4
    fps = 15  # Adjust frame rate as needed
    out = cv2.VideoWriter(f'{animationFilename}.mp4', fourcc, fps, (width, height))

    # Write each frame to the video
    for frame in gif:
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Convert RGB to BGR
        out.write(frame_bgr)

    out.release()
    print (f"MP4 created: {animationFilename}.mp4")








if __name__ == "__main__":

    original = [
        "R",
        "U",
        "E",
        "D",
        "W",
        "E",
        "A",
        "M",
        "O",
        "A",
        "T",
        "A",
        "T",
        "N",
        "Y",
        "A",
        "R",
        "U",
        "O",
        "A",
        "N",
    ]
    target = [
        "R",
        "E",
        "N",
        "E",
        "W",
        "A",
        "U",
        "O",
        "D",
        "A",
        "T",
        "U",
        "M",
        "A",
        "T",
        "A",
        "R",
        "A",
        "Y",
        "O",
        "N",
    ]
    swaps = [
        (6, 17),
        (1, 11),
        (1, 5),
        (2, 3),
        (2, 8),
        (2, 19),
        (2, 13),
        (9, 12),
        (9, 14),
        (9, 18),
    ]

    makeAnimation(original, target, swaps, "animations/example")
