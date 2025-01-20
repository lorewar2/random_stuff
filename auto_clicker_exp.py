import pyautogui
import time

# Check location
def check_loc():
    try:
        while True:
            # Get the current mouse position
            x, y = pyautogui.position()
            # Print the position
            print(f"Mouse position: ({x}, {y})", end="\r")  # Overwrites the same line
            time.sleep(0.1)  # Update every 0.1 seconds
    except KeyboardInterrupt:
        print("\nExiting.")

def click_positions(positions, repeat_count, delay=0.5):
    """
    Clicks on a series of positions in sequence and repeats the process.

    Args:
        positions (list of tuple): List of (x, y) positions to click.
        repeat_count (int): Number of times to repeat the sequence.
        delay (float): Delay in seconds between each click. Default is 0.5 seconds.
    """
    for _ in range(repeat_count):
        for pos in positions:
            pyautogui.moveTo(pos[0], pos[1], duration=0.1)  # Move the mouse
            pyautogui.click()  # Perform the click
            time.sleep(delay)

if __name__ == "__main__":
    #check_loc()
    # Define positions as (x, y) coordinates
    vpn_country_pos = [
        (3209, -282),
        (3209, -225),
        (3209, -168),
        (3209, -111),
        (3209, -54),
        (3209, -3),
        (3209, 60),
        (3209, 117),
        (3209, 174)
    ]
    cursor_pos = [
        (3623, -282),
        (3623, -225),
        (3623, -168),
        (3623, -111),
        (3623, -54),
        (3623, -3),
        (3623, 60),
        (3623, 117),
        (3623, 174)
    ]
    positions_to_click = []
    for cursor in cursor_pos:
        positions_to_click.append(cursor)
        for country in vpn_country_pos:
            positions_to_click.append(country)

    # Define how many times the sequence should be repeated
    repeat_times = 1

    # Call the function with a delay of 1 second between clicks
    click_positions(positions_to_click, repeat_times, delay=1)