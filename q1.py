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

# Print the distributions to check if they are loaded correctly
print("RACE Distribution:", race_dist)
print("Defendant Gender Distribution:", gender_dist)

# Plotting the distributions
years = list(range(2019, 2025))

fig, axs = plt.subplots(2, 1, figsize=(10, 10))

# Plot RACE distribution
for race in race_dist.get(str(years[0]), {}).index:
    axs[0].plot(years, [race_dist.get(str(year), {}).get(race, 0) for year in years], label=race)
axs[0].set_title('RACE Distribution (2019-2024)')
axs[0].set_xlabel('Year')
axs[0].set_ylabel('Proportion')
axs[0].legend()

# Plot Defendant Gender distribution
for gender in gender_dist.get(str(years[0]), {}).index:
    axs[1].plot(years, [gender_dist.get(str(year), {}).get(gender, 0) for year in years], label=gender)
axs[1].set_title('Defendant Gender Distribution (2019-2024)')
axs[1].set_xlabel('Year')
axs[1].set_ylabel('Proportion')
axs[1].legend()

plt.tight_layout()
plt.savefig('dist.png',dpi=300)
plt.show()

