import json
import os

def consolidate_hd_metadata():
    mega_metadata = {}
    for i in range(1, 11):
        path = f'data/raw/chart{i}/metadata.json'
        if os.path.exists(path):
            with open(path, 'r') as f:
                mega_metadata[f'chart{i}'] = json.load(f)
    
    with open('data/final/mega_metadata.json', 'w') as f:
        json.dump(mega_metadata, f, indent=4)
    print("Consolidated HD Metadata into mega_metadata.json")

if __name__ == "__main__":
    consolidate_hd_metadata()
