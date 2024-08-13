import pandas as pd
import matplotlib.pyplot as plt

# List of CSV files
files = [f"{year}.csv" for year in range(2019, 2025)]

# Initialize dictionaries to store distributions
race_dist = {}
gender_dist = {}

# Function to clean and prepare data
def prepare_data(df):
    df = df[['RACE', 'Defendant Gender']].dropna()
    return df

# Loop through each file and compute distributions
for file in files:
    year = file.split('.')[0]
    try:
        df = pd.read_csv(file)
        df = prepare_data(df)
        
        # Calculate distributions
        race_dist[year] = df['RACE'].value_counts(normalize=True)
        gender_dist[year] = df['Defendant Gender'].value_counts(normalize=True)
    except Exception as e:
        print(f"Error processing file {file}: {e}")

# Calculate changes in distributions
race_changes = {race: [race_dist[str(year)].get(race, 0) - race_dist[str(2019)].get(race, 0) for year in range(2019, 2025)] for race in race_dist.get('2019', {}).index}
gender_changes = {gender: [gender_dist[str(year)].get(gender, 0) - gender_dist[str(2019)].get(gender, 0) for year in range(2019, 2025)] for gender in gender_dist.get('2019', {}).index}

# Plotting the changes
years = list(range(2019, 2025))

fig, axs = plt.subplots(2, 1, figsize=(10, 10))

# Plot changes in RACE distribution
for race, changes in race_changes.items():
    axs[0].plot(years, changes, label=race)
axs[0].set_title('Changes in RACE Distribution (2019-2024)')
axs[0].set_xlabel('Year')
axs[0].set_ylabel('Change in Proportion')
axs[0].legend()

# Plot changes in Defendant Gender distribution
for gender, changes in gender_changes.items():
    axs[1].plot(years, changes, label=gender)
axs[1].set_title('Changes in Defendant Gender Distribution (2019-2024)')
axs[1].set_xlabel('Year')
axs[1].set_ylabel('Change in Proportion')
axs[1].legend()

plt.tight_layout()
plt.savefig('change.png',dpi=300)
plt.show()

