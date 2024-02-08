import csv
import itertools
import logging
import random

from PIL import Image, ImageDraw, ImageFont

# Set up logging
logging.basicConfig(filename='main.log', level=logging.INFO, format='%(asctime)s - %(message)s')


# Function to generate and save an image of the basketball stat sheet
async def generate_and_save_image(csv_path, save_path, font_size=random.choice([12, 14, 16, 18]), cell_width=150,
                                  cell_height=30):
    try:
        logging.info("Image generation process started.")
        # Read the CSV file
        with open(csv_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
        num_rows = len(data)
        num_cols = len(data[0])

        # Define the data to be displayed

        img_width = num_cols * cell_width
        img_height = (num_rows + 3) * cell_height
        img = Image.new('RGB', (img_width, img_height), color='white')
        d = ImageDraw.Draw(img)

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
        font = ImageFont.load_default(size=font_size)

        # The title may vary in content and placement

        # Define possible titles
        titles = ['Basketball Statistics', 'Game Summary', 'Player Stats', 'Team Performance']
        title = random.choice(titles)  # Randomly select a title

        # Determine title placement
        title_x = random.randint(10, img_width - font_size * len(title))  # Random horizontal placement
        title_y = random.randint(10, 30)  # Random vertical placement

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
