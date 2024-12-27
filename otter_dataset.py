import pandas as pd
import numpy as np

df = pd.read_csv('dataset.csv')

# Identify dropped columns first
null_counts = df.isnull().sum()
dropped_cols = null_counts[null_counts == len(df)].index
print("Dropped columns (100% null):", dropped_cols.tolist())

# Remove dropped columns
df = df.drop(columns=dropped_cols)

# Now analyze remaining data
print("\nRemaining columns with nulls (%):")
null_percentages = (df.isnull().sum() / len(df) * 100).sort_values(ascending=False)
print(null_percentages[null_percentages > 0])

# Check metrics only from available columns
available_metrics = []
for metric in ['usd_subtotal', 'prep_time_for_ofo_minutes', 'order_rating', 'order_issue_count']:
   if metric in df.columns:
       available_metrics.append(metric)

print("\nKey metrics summary:")
print(df[available_metrics].describe())
