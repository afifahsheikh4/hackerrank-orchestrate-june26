import pandas as pd

# simple evaluation placeholder

def main():
    try:
        df = pd.read_csv("../dataset/output.csv")
        print("✅ Evaluation completed")
        print("Total rows:", len(df))
    except:
        print("❌ Could not load output.csv")

if __name__ == "__main__":
    main()
