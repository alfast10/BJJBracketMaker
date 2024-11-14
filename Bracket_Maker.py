import pandas as pd
import random

def generate_matches(input_file):
    # Read the data from the input CSV file
    data = pd.read_csv(input_file)
    max_matches = 3

    # Group competitors by school
    competitors_by_school = {}
    for _, row in data.iterrows():
        if row['School'] not in competitors_by_school:
            competitors_by_school[row['School']] = []
        competitors_by_school[row['School']].append((row['Name'], row['School']))

    # Shuffle the order of competitors within each school to randomize matches
    for school, competitors in competitors_by_school.items():
        random.shuffle(competitors)

    # Generate match pairings
    matches = []
    competitors_list = list(data['Name'])  # List of all competitors
    remaining_matches = {competitor: max_matches for competitor in competitors_list}  # Dict to track remaining matches for each competitor

    for competitor in competitors_list:
        school = data.loc[data['Name'] == competitor, 'School'].values[0]
        other_competitors = [c for c in competitors_list if c != competitor and data.loc[data['Name'] == c, 'School'].values[0] != school]
        random.shuffle(other_competitors)

        matches_count = 0
        for opponent in other_competitors:
            if remaining_matches[competitor] > 0 and remaining_matches[opponent] > 0 and matches_count < max_matches:
                matches.append((f"{competitor} ({school})", f"{opponent} ({data.loc[data['Name'] == opponent, 'School'].values[0]})"))
                remaining_matches[competitor] -= 1
                remaining_matches[opponent] -= 1
                matches_count += 1

    # Randomize the order of matches
    random.shuffle(matches)

    # Create the output file name
    output_file = input_file.split('.csv')[0] + '_Matches.csv'

    # Create a DataFrame for the match list
    matches_df = pd.DataFrame(matches, columns=['Competitor 1', 'Competitor 2'])

    # Save the matches to the output CSV file
    matches_df.to_csv(output_file, index=False)
    print(f"Matches generated and saved to {output_file}")
def process_multiple_files(files):
    for file in files:
        generate_matches(file)

if __name__ == "__main__":
    input_files = input("Enter CSV file names, separated by commas: ").split(',')
    input_files = [file.strip() for file in input_files]  # Strip whitespace from each file name
    process_multiple_files(input_files)
