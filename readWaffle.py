from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def readWaffle(puzzle_number=None):

    driver = webdriver.Chrome()

    if puzzle_number:
        # Navigate to the target webpage
        driver.get("https://wafflegame.net/archive")

        # Locate the <div> element
        element = driver.find_element(
            By.CSS_SELECTOR, f'div.item[data-id="{puzzle_number}"]'
        )

        # Click the element to trigger the JavaScript function
        element.click()

    else:
        # load the Waffle page
        driver.get("https://wafflegame.net")

    # Wait for the tiles to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'div[class^="tile draggable tile"]')
        )
    )

    # Find the divs that start with 'tile draggable tile'
    tile_elements = driver.find_elements(
        By.CSS_SELECTOR, 'div[class^="tile draggable tile"]'
    )

    # Extract the text content (characters) and their associated colors
    tiles = []
    for tile in tile_elements:
        letter = tile.text  # Get the text of the tile
        class_names = tile.get_attribute("class")  # Get class attribute as a string

        # Determine the color based on the class names
        if "green" in class_names:
            color = "green"
        elif "yellow" in class_names:
            color = "yellow"
        else:
            color = "grey"

        tiles.append((letter, color))

    # Locate the element using its class name and get the text
    game_number_element = driver.find_element(By.CLASS_NAME, "game-number")
    game_number_text = game_number_element.text

    # Extract the number part from the text
    game_number = game_number_text.split("#")[-1]

    # Close the WebDriver
    driver.quit()
    return tiles, game_number


if __name__ == "__main__":
    print(readWaffle())
