import os

def find_files_by_keyword(root_dir, keywords):
    """Find files containing specific keywords in their name or content."""
    results = []
    
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.py'):
                # First check if keyword is in the filename
                file_path = os.path.join(root, file)
                if any(keyword.lower() in file.lower() for keyword in keywords):
                    results.append((file_path, "filename contains keyword"))
                    continue
                
                # Then check file content (only for smaller files)
                try:
                    file_size = os.path.getsize(file_path)
                    if file_size < 500000:  # Skip files larger than 500KB
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            if any(keyword.lower() in content.lower() for keyword in keywords):
                                results.append((file_path, "content contains keyword"))
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    
    return results

if __name__ == "__main__":
    root_dir = 'd:\\Shenkha_Github\\LibMultiLabel'
    keywords = ['dataset', 'dataloader', 'datamodule', 'eur-lex', 'eurlex']
    
    print("Searching for data loading modules...")
    results = find_files_by_keyword(root_dir, keywords)
    
    if results:
        print("\nPotential data loading files found:")
        for file_path, reason in results:
            print(f"- {file_path} ({reason})")
        
        print("\nThese files likely contain code for loading and processing the EUR-Lex dataset.")
        print("Check the following components:")
        print("1. Dataset classes that parse the raw text files")
        print("2. DataModule implementations that handle batch creation")
        print("3. Tokenizer code for processing the text data")
    else:
        print("No matching files found. Try with different keywords or check the repository structure manually.")
