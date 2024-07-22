import pandas as pd
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt

# Initialize dictionaries to store p-values for each year
pvals_anova = {}
pvals_chi = {}
pvals_combined = {}

# Ask user for input
print("Please select one of the following options:")
print("1. Evaluate 'RACE'")
print("2. Evaluate 'Defendant Gender'")
print("3. Evaluate both 'RACE' and 'Defendant Gender'")
choice = int(input("Enter your choice (1, 2, or 3): "))

# Determine variables to evaluate based on user input
if choice == 1:
    variables = ['RACE']
elif choice == 2:
    variables = ['Defendant Gender']
elif choice == 3:
    variables = ['RACE', 'Defendant Gender']
else:
    print("Invalid choice. Please enter 1, 2, or 3.")
    exit()

# Define line styles and widths for each variable and test
styles = {'RACE': {'linestyles': ['-', '--', ':', '-.'], 'linewidths': [1, 1, 1, 1]},
          'Defendant Gender': {'linestyles': ['-', '--', ':', '-.'], 'linewidths': [2, 2, 2, 2]}}

# Loop over each year
for year in range(2019, 2025):
    # Load the data
    df = pd.read_csv(f'{year}.csv')

    for variable in variables:
        # Handle empty cells by filling with a default value or removing
        df = df.dropna(subset=['Case Closed', variable])

        # Convert string values to categories for analysis
        df['Case Closed'] = df['Case Closed'].astype('category').cat.codes
        df[variable] = df[variable].astype('category').cat.codes

        # Perform ANOVA test
        fval_anova, pval_anova = stats.f_oneway(*[df.loc[df[variable] == val, 'Case Closed'] for val in df[variable].unique()])
        pvals_anova.setdefault(variable, []).append(pval_anova)

        # Perform Chi-Square test
        contingency_table = pd.crosstab(df[variable], df['Case Closed'])
        chi2, pval_chi, dof, expected = stats.chi2_contingency(contingency_table)
        pvals_chi.setdefault(variable, []).append(pval_chi)

        # Combine the p-values using Fisher's method
        combined_pval = stats.combine_pvalues([pval_anova, pval_chi], method='fisher')[1]
        pvals_combined.setdefault(variable, []).append(combined_pval)

# Plot the trends
plt.figure(figsize=(10, 6))
years = list(range(2019, 2025))
for variable in variables:
    plt.plot(years, pvals_anova[variable], label=f'ANOVA {variable}', linestyle=styles[variable]['linestyles'][0], linewidth=styles[variable]['linewidths'][0], color='black')
    plt.plot(years, pvals_chi[variable], label=f'Chi-Square {variable}', linestyle=styles[variable]['linestyles'][1], linewidth=styles[variable]['linewidths'][1], color='black')
    plt.plot(years, pvals_combined[variable], label=f'Combined {variable}', linestyle=styles[variable]['linestyles'][2], linewidth=styles[variable]['linewidths'][2], color='black')

# Add a horizontal line at p-value=0.05
plt.axhline(y=0.05, color='r', linestyle='--')

plt.xlabel('Year')
plt.ylabel('p-value')
plt.title('Trend of Bias Tests')
plt.legend()
plt.savefig('result.png',dpi=300)
plt.show()
