import argparse
import asyncio
import os
import random
import time
from itertools import repeat

from aiomultiprocess import Pool

from image_generator import generate_and_save_image
from synthetic_data_generator import generate_and_save_data


def parse_arguments():
    """
    Parse command line arguments for generating synthetic basketball stat sheet images and CSV files.

    Returns:
        argparse.Namespace: Parsed command line arguments.

    Raises:
        None.
    """
    parser = argparse.ArgumentParser(
        description="Generate synthetic basketball stat sheet images and CSV files."
    )
    parser.add_argument(
        "--num_sets", type=int, default=5,
        help="Number of sets to generate (default: 5)"
    )
    parser.add_argument(
        "--num_players", type=int, default=10,
        help="Number of players per team (default: 10)"
    )
    parser.add_argument(
        "--std_dev_multiplier", type=float, default=random.uniform(0.5, 1.5),
        help="Standard deviation multiplier for data variability (default: random.uniform(0.5, 1.5))"
    )
    parser.add_argument(
        "--random_seed", type=int, default=42,
        help="Random seed for reproducibility (default: 42). This allows others to reproduce the same synthetic data "
             "by using the same seed value."
    )
    parser.add_argument(
        "--image_output_directory", type=str, default="images",
        help="Output directory path (default: 'images')"
    )
    parser.add_argument(
        "--csv_output_directory", type=str, default="data",
        help="Output directory path (default: 'data')"
    )
    parser.add_argument(
        "--font_size", type=int, default=random.choice([12, 14, 16, 18]),
        help="Font size for the stat sheet image (default: random.choice([12, 14, 16, 18]))"
    )
    parser.add_argument(
        "--cell_width", type=int, default=150,
        help="Width of each cell in the stat sheet image (default: 150)"
    )
    parser.add_argument(
        "--cell_height", type=int, default=30,
        help="Height of each cell in the stat sheet image (default: 30)"
    )
    return parser.parse_args()


async def main():
    """
    Run the main process for generating synthetic basketball stat sheet images and CSV files.

    Returns:
        None.

    Raises:
        None.
    """
    args = parse_arguments()

    # Set random seed for reproducibility
    random.seed(args.random_seed)

    # Get current working directory
    cwd = os.getcwd()

    # Create csv output directory if it doesn't exist
    os.makedirs(f'{cwd}/{args.csv_output_directory}', exist_ok=True)

    # Create image output directory if it doesn't exist
    os.makedirs(f'{cwd}/{args.image_output_directory}', exist_ok=True)

    # Define csv save path
    csv_save_path = f"{cwd}/{args.csv_output_directory}"

    # Define image save path
    image_save_path = f"{cwd}/{args.image_output_directory}"

    async with Pool() as pool:
        now_epoc = int(time.time())
        csv_save_paths = [
            f"{csv_save_path}/set_{i}_{now_epoc}.csv"
            for i in range(1, args.num_sets + 1)
        ]
        async for csv_path in pool.starmap(
                generate_and_save_data, zip(csv_save_paths, repeat(args.num_players), repeat(args.std_dev_multiplier))
        ):
            await generate_and_save_image(
                csv_path=csv_path,
                save_path=csv_path.replace(csv_save_path, image_save_path).replace(".csv", ".png"),
                font_size=args.font_size,
                cell_width=args.cell_width,
                cell_height=args.cell_height
            )


if __name__ == "__main__":
    asyncio.run(main())
