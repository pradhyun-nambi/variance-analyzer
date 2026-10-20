from src.load import load_csv, combine
from src.variance import add_variance, flag_material

df = combine(load_csv("data/budget.csv"), load_csv("data/actuals.csv"))
df = flag_material(add_variance(df))

print("ALL ROWS WITH A VARIANCE OR MISSING DATA")
print(df[df["variance"] != 0].to_string(index=False))
print()
print("FLAGGED")
print(df[df["flagged"]].to_string(index=False))