import csv
import itertools
import logging
import random

from PIL import Image, ImageDraw, ImageFont

# Set up logging
logging.basicConfig(filename='main.log', level=logging.INFO, format='%(asctime)s - %(message)s')


# Function to generate and save an image of the basketball stat sheet
async def generate_and_save_image(
        csv_path: str,
        save_path: str,
        font_size: int = random.choice([12, 14, 16, 18]),
        cell_width: int = 150,
        cell_height: int = 30
):
    """
    Generate and save an image based on data from a CSV file.

    Args:
        csv_path (str): The path to the CSV file containing the data.
        save_path (str): The path to save the generated image.
        font_size (int, optional): The font size for the text in the image. Defaults to a random choice of
            [12, 14, 16, 18].
        cell_width (int, optional): The width of each cell in the data table. Defaults to 150.
        cell_height (int, optional): The height of each cell in the data table. Defaults to 30.

    Raises:
        Exception: If there is an error generating the image.

    Examples:
        # Generate and save an image using default settings
        await generate_and_save_image('data.csv', 'image.png')

        # Generate and save an image with custom font size and cell dimensions
        await generate_and_save_image('data.csv', 'image.png', font_size=16, cell_width=200, cell_height=40)
    """
    try:
        logging.info("Image generation process started.")
        # Read the CSV file
        with open(csv_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            data: list[list[str]] = list(reader)
        num_rows: int = len(data)
        num_cols: int = len(data[0])

        # Define the data to be displayed

        img_width: int = num_cols * cell_width
        img_height: int = (num_rows + 3) * cell_height
        img: Image = Image.new('RGB', (img_width, img_height), color='white')
        d: ImageDraw = ImageDraw.Draw(img)

        # The font style, size, and weight may vary

        # Define pools for font styles, sizes, and weights
        # font_styles = ['arial.ttf', 'times.ttf', 'calibri.ttf']
        # font_sizes = [12, 14, 16, 18]
        # font_weights = ['normal', 'bold']

        # Randomly select font style, size, and weight
        # font_style = random.choice(font_styles)
        # font_size = random.choice(font_sizes)
        # font_weight = random.choice(font_weights)

        # I don not have font files for different font styles:
        # Ex: font = ImageFont.truetype(font_file, font_style, font_size)
        # The PIL library's ImageFont.truetype() function doesn't directly support specifying font weight.
        # If you need to include font weight variations, you would typically select different font files that
        # represent different weights (e.g., regular, bold) from your font pool.
        # Then, you would use the selected font file when creating the ImageFont object.
        # Ex: font = ImageFont.truetype(font_file, font_style, font_size)
        font: ImageFont = ImageFont.load_default(size=font_size)

        # The title may vary in content and placement

        # Define possible titles
        titles: list[str] = ['Basketball Statistics', 'Game Summary', 'Player Stats', 'Team Performance']
        title: str = random.choice(titles)  # Randomly select a title

        # Determine title placement
        title_x: int = random.randint(10, img_width - font_size * len(title))  # Random horizontal placement
        title_y: int = random.randint(10, 30)  # Random vertical placement

        # Draw the title
        d.text((title_x, title_y), title, fill="black", font=font)

        # Draw data table, including space at top for title
        for i, j in itertools.product(range(num_rows), range(num_cols)):
            d.rectangle(
                (
                    (j * cell_width, (i + 2) * cell_height),
                    ((j + 1) * cell_width, (i + 3) * cell_height)
                ),
                fill="white",
                outline="black"
            )
            d.text(
                (j * cell_width + 5, (i + 2) * cell_height + 5),
                data[i][j],
                fill="black",
                font=font
            )

        img.save(save_path)
        logging.info(f"Generated image: {save_path}")
    except Exception as e:
        logging.error(f"Error generating image: {e}")
