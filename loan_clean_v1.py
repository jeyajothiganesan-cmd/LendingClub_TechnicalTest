import pandas as pd
import numpy as np
import re


INPUT_CSV  = r"C:\Users\jeyaj\OneDrive\Desktop\Technical_Test\archive\loan.csv"  
OUTPUT_CSV = r"C:\Users\jeyaj\OneDrive\Desktop\Technical_Test\archive\clean_loan.csv"

def pick_col(cols, candidates):
    for c in candidates:
        if c in cols:
            return c
    return None


CANDIDATES = {
   
    "id":        ["id","Id","ID"],
    "listD":     ["issue_d","list_d","listD","issueDate"],  
    "acceptD":   ["accept_d","acceptD"],                    
    "loanAmnt":   ["loan_amnt","loanAmnt"],
    "fundedAmnt": ["funded_amnt","fundedAmnt"],
    "installment":["installment"],
    "term":       ["term"],
    "intRate":    ["int_rate","intRate"],
    "grade":     ["grade"],
    "subGrade":  ["sub_grade","subGrade"],
    "purpose":   ["purpose"],
    "addrState": ["addr_state","addrState"],
    "annualInc": ["annual_inc","annualInc"],
    "dti":       ["dti"],
    "loan_status": ["loan_status","status"],
}

df = pd.read_csv(INPUT_CSV)
df.columns = [c.strip() for c in df.columns]

mapping = {}
for std_name, candidates in CANDIDATES.items():
    src = pick_col(df.columns, candidates)
    if src is not None and df[src].notna().sum() > 0:
        mapping[src] = std_name

if not mapping:
    raise ValueError("No expected columns found with data. Check INPUT_CSV and column names.")

df = df[list(mapping.keys())].rename(columns=mapping)

for c in ["listD","acceptD"]:
    if c in df.columns:
        df[c] = pd.to_datetime(df[c], errors="coerce")

if "intRate" in df.columns:
    df["intRate"] = (
        df["intRate"].astype(str).str.replace("%","", regex=False).str.strip()
        .replace({"": np.nan, "nan": np.nan})
    )
    df["intRate"] = pd.to_numeric(df["intRate"], errors="coerce")

if "term" in df.columns:
    df["term"] = pd.to_numeric(df["term"].astype(str).str.extract(r"(\d+)")[0], errors="coerce")

ref = None
if "listD" in df.columns and df["listD"].notna().any():
    ref = df["listD"]
elif "acceptD" in df.columns and df["acceptD"].notna().any():
    ref = df["acceptD"]

if ref is not None:
    ref = pd.to_datetime(ref, errors="coerce")
    df["ApplicationMonth"] = ref.dt.to_period("M").dt.to_timestamp()

df.to_csv(OUTPUT_CSV, index=False)

print("Saved:", OUTPUT_CSV)
print("Rows:", len(df))
print("Columns:", len(df.columns))
print("Columns included:", list(df.columns))
