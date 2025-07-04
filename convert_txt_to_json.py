import json

# Change this filename if your .txt file has a different name
txt_filename = 'thelogisticsoflogistics_2025-07-04.txt'
json_filename = 'thelogisticsoflogistics_2025-07-04.json'

# Step 1: Read the .txt file content
with open(txt_filename, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Step 2: Process lines (e.g., strip whitespace)
headlines = [line.strip() for line in lines if line.strip()]

# Step 3: Save as JSON file
with open(json_filename, 'w', encoding='utf-8') as f:
    json.dump(headlines, f, ensure_ascii=False, indent=4)

print(f"Converted {txt_filename} to {json_filename} successfully!")
