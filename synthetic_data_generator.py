# import asyncio
import csv
import logging
import random

import numpy as np
from faker import Faker

# Set up logging
logging.basicConfig(filename='log.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Set up Faker to generate fake player names and numbers
fake = Faker()

# Define the mean deviation for each stat category
stats_mean_and_st_dev = {
    'Points': {"mean": 10.000, "std_dev": 3.0000},
    'Rebounds': {"mean": 3.0000, "std_dev": 0.9000},
    'Assists': {"mean": 2, "std_dev": 0.6000},
    'Steals': {"mean": 0.5000, "std_dev": 0.1500},
    'Blocks': {"mean": 0.5000, "std_dev": 0.1500},
    'Turnovers': {"mean": 0.5000, "std_dev": 0.1500},
    'Fouls': {"mean": 1.0000, "std_dev": 0.3000}
}


# Function to generate synthetic stats to use for the team with visual variations
async def generate_stats_to_use_and_column_names() -> tuple[list[str], list[str], int, int]:
    """
    Generate the list of column names and statistics to use for generating synthetic basketball data.

    Returns:
        tuple[list[str], list[str], int, int]: A tuple containing the following:
            - A list of all column names, including name, number, and statistics columns.
            - A list of only the statistics column names.
            - The index of the name column in the list of all column names.
            - The index of the number column in the list of all column names.
    """
    # Name and number columns
    name_column = random.choice(["Player", "Name", "Player Name"])
    number_column = random.choice(["#", "Number", "Player Number"])
    name_number_columns = [name_column, number_column]

    # After points, the other stats may have different orderings and some may not always be included
    # Define statistic keys and their display names
    stat_keys = list(stats_mean_and_st_dev.keys())
    stats_to_use = ['Points']  # Always include points

    excluded_stats = random.sample(stat_keys[1:], k=random.randint(0, len(stat_keys) - 2))  # Randomly exclude stats

    # Add non-excluded stats to the display names list, except for 'Points', since 'Points' already included
    stats_to_use.extend(
        stat for stat in stat_keys if (stat not in excluded_stats and stat != 'Points')
    )

    all_columns = name_number_columns + stats_to_use

    # Shuffle the column names to introduce variability
    random.shuffle(all_columns)

    # Now get just stat columns
    stat_columns = [column for column in all_columns if column not in name_number_columns]

    # Get name column index
    name_column_index: int = all_columns.index(name_column)
    # Get number column index
    number_column_index: int = all_columns.index(number_column)

    return all_columns, stat_columns, name_column_index, number_column_index


# Function to generate synthetic player names and player numbers
async def generate_player_names(num_players) -> list[str]:
    """
    Generate a list of synthetic player names.

    Args:
        num_players (int): The number of player names to generate.

    Returns:
        list[str]: A list of synthetic player names.
    """
    return [
        fake.name()
        for _ in range(num_players)
    ]


async def generate_player_numbers(num_players) -> list[int]:
    """
    Generate a list of synthetic player numbers.

    Args:
        num_players (int): The number of player numbers to generate.

    Returns:
        list[int]: A list of synthetic player numbers.
    """
    return [
        fake.random_int(min=1, max=99)
        for _ in range(num_players)
    ]


# Function to generate synthetic data for the team
async def generate_data_for_stat(stat, num_players, std_dev_multiplier) -> np.ndarray:
    """
    Generate synthetic data for a specific statistic.

    Args:
        stat (str): The name of the statistic to generate data for.
        num_players (int): The number of players to generate data for.
        std_dev_multiplier (float): The standard deviation multiplier for generating data.

    Returns:
        np.ndarray: An array of synthetic data for the specified statistic.

    Note:
        The function uses the mean and standard deviation of the specified statistic from the `stats_mean_and_st_dev` dictionary
        to generate data using a normal distribution with the specified standard deviation multiplier.
    """
    mean = stats_mean_and_st_dev[stat]["mean"]
    std_dev = stats_mean_and_st_dev[stat]["std_dev"]
    # lower_limit = max(0, mean - (2 * (std_dev * std_dev_multiplier)))
    # upper_limit = mean + (2 * (std_dev * std_dev_multiplier))
    values = np.random.normal(
        mean,
        std_dev * std_dev_multiplier,
        num_players
    )
    # return np.clip(values, lower_limit, upper_limit).astype(int)
    return np.round(values).astype(int)


# Function to generate synthetic data for the team
async def generate_team_data(num_players, std_dev_multiplier):
    """
    Generate team data for a basketball stat sheet.

    Args:
        num_players (int): The number of players on the team.
        std_dev_multiplier (float): The standard deviation multiplier for generating player stats.

    Yields:
        list: The column names row.
        list: Each player's row, including their name, number, and stats.
        list: The team totals row.

    Raises:
        None.

    Examples:
        team_data_generator = generate_team_data(num_players=10, std_dev_multiplier=2.0)
        for row in team_data_generator:
            print(row)
    """
    all_columns, stat_columns, name_column_index, number_column_index = await generate_stats_to_use_and_column_names()
    team_totals: list = []
    team_stats: dict = {}
    player_names: list[str] = await generate_player_names(num_players=num_players)
    player_numbers: list[int] = await generate_player_numbers(num_players=num_players)
    for stat in stat_columns:
        data_for_stat: np.ndarray = await generate_data_for_stat(
            stat=stat,
            num_players=num_players,
            std_dev_multiplier=std_dev_multiplier
        )
        team_stats[stat] = data_for_stat
        team_totals.append(np.sum(data_for_stat))
    # Yield column names row
    yield all_columns
    for player_name, player_number, stat_values in zip(player_names, player_numbers, zip(*team_stats.values())):
        # Build player row:
        player_row: list = [None] * len(all_columns)
        player_row[name_column_index] = player_name
        player_row[number_column_index] = player_number
        for stat, value in zip(stat_columns, stat_values):
            stat_index = all_columns.index(stat)
            player_row[stat_index] = value
        # Yield player row
        yield player_row
    # Build team totals row
    team_totals_row: list = [None] * len(all_columns)
    team_totals_row[name_column_index] = 'Team Totals'
    team_totals_row[number_column_index] = ''
    for stat, value in zip(stat_columns, team_totals):
        stat_index = all_columns.index(stat)
        team_totals_row[stat_index] = value
    # Yield team totals row
    yield team_totals_row


# Function to save the data to a CSV file
async def generate_and_save_data(save_path, num_players, std_dev_multiplier):
    """
    Generate and save team data to a CSV file.

    Args:
        save_path (str): The path to save the generated data CSV file.
        num_players (int): The number of players on the team.
        std_dev_multiplier (float): The standard deviation multiplier for generating player stats.

    Returns:
        str: The path where the data CSV file is saved.

    Raises:
        None.
    """
    logging.info("Data generation process started.")
    try:
        with open(save_path, 'w') as file:
            writer = csv.writer(file)
            async for row in generate_team_data(num_players=num_players, std_dev_multiplier=std_dev_multiplier):
                writer.writerow(row)
        logging.info(f"Saved data to CSV: {save_path}")
        return save_path
    except Exception as e:
        logging.error(f"Error saving data to CSV: {e}")

# if __name__ == "__main__":
#     asyncio.run(generate_and_save_data(save_path="test.csv"))
