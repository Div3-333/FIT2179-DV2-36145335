import os
import shutil
import json

def consolidate_final_files():
    target_dir = 'final_files'
    os.makedirs(target_dir, exist_ok=True)
    
    mega_metadata = {}
    
    for i in range(1, 11):
        chart_dir = f'chart{i}'
        if not os.path.exists(chart_dir):
            continue
            
        # 1. Consolidate Metadata
        meta_path = os.path.join(chart_dir, 'metadata.json')
        if os.path.exists(meta_path):
            with open(meta_path, 'r') as f:
                mega_metadata[f'chart{i}'] = json.load(f)
        
        # 2. Copy CSV files with prefix to avoid collisions
        for file in os.listdir(chart_dir):
            if file.endswith('.csv'):
                src_path = os.path.join(chart_dir, file)
                dest_filename = f'chart{i}_{file}'
                dest_path = os.path.join(target_dir, dest_filename)
                shutil.copy2(src_path, dest_path)
                print(f"Copied {file} to {dest_path}")

    # 3. Write Mega Metadata
    with open(os.path.join(target_dir, 'mega_metadata.json'), 'w') as f:
        json.dump(mega_metadata, f, indent=4)
    
    print(f"\nConsolidation complete. 'mega_metadata.json' created in {target_dir}/")

if __name__ == "__main__":
    consolidate_final_files()
