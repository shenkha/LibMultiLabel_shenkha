import os

def analyze_dataset_format(file_path, num_samples=5):
    """
    Print the first few samples from the dataset to understand its structure
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= num_samples:
                break
                
            print(f"Sample {i+1}:")
            print(f"Raw line: {line[:100]}..." if len(line) > 100 else f"Raw line: {line}")
            
            # Try to identify the separator between labels and text
            if '\t' in line:
                parts = line.split('\t', 1)
                separator = '\\t'
            else:
                # Try space as separator
                parts = line.split(' ', 1)
                separator = 'space'
            
            if len(parts) == 2:
                labels, text = parts
                print(f"Separator: {separator}")
                print(f"Labels: {labels}")
                print(f"Text: {text[:50]}..." if len(text) > 50 else f"Text: {text}")
            else:
                print("Could not identify clear separator between labels and text")
            
            print("-" * 80)

if __name__ == "__main__":
    dataset_path = "data/EUR-Lex/train.txt"
    if os.path.exists(dataset_path):
        print(f"Analyzing dataset: {dataset_path}")
        analyze_dataset_format(dataset_path)
    else:
        print(f"File not found: {dataset_path}")
        print("Please make sure you've downloaded the EUR-Lex dataset and placed it in the correct location.")
