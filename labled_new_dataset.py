import pandas as pd

# Load dataset (replace with your file path)
df = pd.read_csv("dataset.csv", header=None, names=["ax","ay","az","gx","gy","gz"])

# Parameters for nodding detection
AZ_NORMAL = 9.8
THRESHOLD = 1.5   # if az deviates more than ±1.5g from 9.8, mark as nodding

def detect_nod(row):
    if abs(row["az"] - AZ_NORMAL) > THRESHOLD:
        return 1   # microsleep/nodding
    else:
        return 0   # awake

df["label"] = df.apply(detect_nod, axis=1)

# Save labeled dataset
df.to_csv("labeled_dataset.csv", index=False)

print(df.head(50))
print("\nLabel counts:\n", df["label"].value_counts())
