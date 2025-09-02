import pandas as pd
from analyzer import analyze_groups

# Read Excel file (example.xlsx should have columns: Group1, Group2, Group3)
df = pd.read_excel("example.xlsx")

# Each column = one group
groups = [df[col].dropna().tolist() for col in df.columns]

result = analyze_groups(groups)

print("=== Statistical Analysis ===")
print(f"Test: {result['test_used']}")
print(f"Statistic: {result['statistic']:.4f}, p-value={result['p_value']:.4f}")
print(f"Shapiro p-values: {result['shapiro_p']}")
print(f"Levene p-value: {result['levene_p']:.4f}")
