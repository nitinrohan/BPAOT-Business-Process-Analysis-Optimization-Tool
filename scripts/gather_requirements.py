import pandas as pd

def collect_input():
    entries = []
    print("Enter business requirements (type 'exit' to stop):")
    while True:
        req = input("Requirement: ")
        if req.lower() == 'exit':
            break
        pain = input("Pain Point: ")
        solution = input("Possible Solution: ")
        entries.append({"Requirement": req, "Pain Point": pain, "Proposed Solution": solution})
    return entries

def save_to_excel(data, path="data/requirements.xlsx"):
    df = pd.DataFrame(data)
    df.to_excel(path, index=False)
    print(f"\n✅ Saved to {path}")

if __name__ == "__main__":
    inputs = collect_input()
    save_to_excel(inputs)
