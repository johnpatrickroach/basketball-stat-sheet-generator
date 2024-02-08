# Basketball Stat Sheet Generator

This project is a Python application for generating synthetic basketball stat sheets and corresponding images.
It allows users to create customizable sets of basketball stat sheets with randomized player data.

## Project Description

The Basketball Stat Sheet Generator creates synthetic basketball stat sheets and images based on user-defined 
parameters such as the number of sets, number of players per team, standard deviation multiplier, font size, font type, 
cell width, and cell height.

The generated stat sheets include player names, player numbers, and various basketball statistics such as points, 
rebounds, assists, steals, blocks, turnovers, and fouls. 
The data for each statistic follows a normal distribution with customizable mean and standard deviation values.


## Setup Instructions

To set up and run the Basketball Stat Sheet Generator, follow these steps:

1. **Clone the Repository**: Clone the repository to your local machine using the following command:

   ```
   git clone https://github.com/johnpatrickroach/basketball-stat-sheet-generator.git
   ```

2. **Install Dependencies**: Navigate to the project directory and install the required dependencies using pip:

   ```
   cd basketball-stat-sheet-generator
   pip install -r requirements.txt
   ```

3. **Run the Application**: Execute the `main.py` script to generate basketball stat sheets and images:

   ```
   python main.py
   ```

4. **View Output**: Once the generation process is complete, the generated CSV files and images will be saved in the 
respective output directories (`data` for CSV files and `images` for images).

Certainly! Here's the updated README.md with a section listing the available command-line parameters/arguments along with their defaults, followed by the example of using all the command-line arguments:

---


## Command-line Parameters

The Basketball Stat Sheet Generator supports the following command-line parameters:

- `--num_sets`: Number of sets to generate (default: 5)
- `--num_players`: Number of players per team (default: 10)
- `--std_dev_multiplier`: Standard deviation multiplier for data variability (default: random.uniform(0.5, 1.5))
- `--random_seed`: Random seed for reproducibility (default: 42)
- `--image_output_directory`: Output directory path for generated images (default: 'images')
- `--csv_output_directory`: Output directory path for generated CSV files (default: 'data')
- `--font_size`: Font size for the stat sheet image (default: 14)
- `--cell_width`: Width of each cell in the stat sheet image (default: 150)
- `--cell_height`: Height of each cell in the stat sheet image (default: 30)

## Example Usage

Here's an example of running the Basketball Stat Sheet Generator from the command line with custom values for each parameter:

```bash
python main.py \
    --num_sets 3 \
    --num_players 12 \
    --std_dev_multiplier 1.2 \
    --random_seed 123 \
    --image_output_directory images \
    --csv_output_directory data \
    --font_size 16 \
    --cell_width 180 \
    --cell_height 40
```

This command generates 3 sets of synthetic basketball stat sheets and images with the specified parameters.

--- 

With these additions, users can easily understand the available command-line options and how to customize the generation process according to their needs.


## Authors

- [Patrick Roach](https://github.com/johnpatrickroach)

## Contributing

If you'd like to contribute to the Basketball Stat Sheet Generator, please fork the repository, make your changes, 
and submit a pull request. We welcome contributions and feedback from the community.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- aiomultiprocessing for combining async functions with parallel processing.
- Faker library for generating fake player names and numbers.
- pillow library for image processing capabilities.
- numpy for generating data that follows a normal distribution.