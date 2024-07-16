import pandas as pd
import numpy as np
from lifelines import KaplanMeierFitter
from lifelines.statistics import multivariate_logrank_test
import matplotlib.pyplot as plt

# Generate example data with 100 data points and 3 groups
np.random.seed(42)
data = {
    'days_to_readmission': np.concatenate([
        np.random.exponential(scale=5, size=30),  # 30 patients with readmission times
        np.array([np.nan] * 70)                     # 70 patients not readmitted
    ]),
    'complication': np.random.choice(['Group1', 'Group2', 'Group3'], size=100, p=[0.33, 0.33, 0.34])
}
df = pd.DataFrame(data)

# Create the event indicator
df['event'] = df['days_to_readmission'].notnull().astype(int)
max_value = df['days_to_readmission'].max() + 1
df.loc[df['days_to_readmission'].isnull(), 'days_to_readmission'] = max_value
df['days_to_readmission'] = pd.to_numeric(df['days_to_readmission'])  # Ensure the column is numeric

# Initialize the plot
plt.figure(figsize=(10, 6))

# Define line styles
line_styles = {
    'Group1': '-',
    'Group2': '--',
    'Group3': ':'
}

# Fit and plot the Kaplan-Meier estimators for each group
kmf = KaplanMeierFitter()
groups = df['complication'].unique()
for group in groups:
    mask = df['complication'] == group
    kmf.fit(durations=df[mask]['days_to_readmission'], event_observed=df[mask]['event'], label=group)
    kmf.plot_survival_function(ci_show=False, linestyle=line_styles[group], linewidth=2, color='black')
    
    # Manually plot the confidence intervals as lines
    plt.plot(kmf.confidence_interval_.index, kmf.confidence_interval_[f'{group}_lower_0.95'], linestyle=line_styles[group], color='gray', linewidth=1)
    plt.plot(kmf.confidence_interval_.index, kmf.confidence_interval_[f'{group}_upper_0.95'], linestyle=line_styles[group], color='gray', linewidth=1)

# Perform the log-rank test to compare the survival curves
results = multivariate_logrank_test(df['days_to_readmission'], df['complication'], df['event'])
p_value = results.p_value

# Add plot details
plt.title(f'Kaplan-Meier Survival Curve\np-value: {p_value:.4f}', fontsize=14)
plt.xlabel('Days to Readmission', fontsize=12)
plt.ylabel('Survival Probability', fontsize=12)
plt.legend(fontsize=12)
plt.grid(False)
plt.show()
