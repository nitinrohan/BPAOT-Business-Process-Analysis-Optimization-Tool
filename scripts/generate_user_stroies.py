import pandas as pd

def generate_user_stories(path="data/requirements.xlsx", output_path="data/user_stories.txt"):
    df = pd.read_excel(path)
    stories = []

    for index, row in df.iterrows():
        req = row['Requirement']
        pain = row['Pain Point']
        solution = row['Proposed Solution']
        story = f"As a user, I want to {req.lower()} because {pain.lower()}. Solution: {solution}."
        stories.append(story)

    with open(output_path, "w") as f:
        for story in stories:
            f.write(story + "\n")

    print(f"\n✅ {len(stories)} user stories saved to {output_path}")

if __name__ == "__main__":
    generate_user_stories()
