import multiprocessing
import sys
import time
from typing import List, Dict
from utils import search_file, merge_results, get_files_list, create_files, generate_keywords

def process_search(files: List[str], keywords: List[str], queue: multiprocessing.Queue):
    """Функція для пошуку ключових слів у файлах в окремому процесі."""
    process_results = {}
    for file in files:
        file_results = search_file(file, keywords)
        for keyword, found_files in file_results.items():
            if keyword not in process_results:
                process_results[keyword] = []
            process_results[keyword].extend(found_files)
    queue.put(process_results)

def main():
    try:
        num_files = 5
        num_processes = 4
        directory = "test_files"
        
        create_files(num_files, directory)
        files = get_files_list(directory)
        keywords = generate_keywords(5)  # Генеруємо 5 випадкових ключових слів
        
        print(f"Пошук ключових слів: {keywords}")
        
        # Розділяємо файли між процесами
        files_per_process = len(files) // num_processes
        processes = []
        queue = multiprocessing.Queue()
        
        start_time = time.time()
        
        for i in range(num_processes):
            start = i * files_per_process
            end = start + files_per_process if i < num_processes - 1 else None
            process_files = files[start:end]
            process = multiprocessing.Process(target=process_search, args=(process_files, keywords, queue))
            processes.append(process)
            process.start()
        
        results = []
        for _ in range(num_processes):
            results.append(queue.get())
        
        for process in processes:
            process.join()
        
        end_time = time.time()
        
        merged_results = merge_results(results)
        
        print("\nРезультати пошуку:")
        for keyword, found_files in merged_results.items():
            print(f"{keyword}: знайдено у {len(found_files)} файлах")
        
        print(f"\nЧас виконання: {end_time - start_time:.2f} секунд")
    
    except Exception as e:
        print(f"Виникла помилка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()