import sys
import threading
import time
from typing import List, Dict
from utils import search_file, merge_results, get_files_list, create_files, generate_keywords

def thread_search(files: List[str], keywords: List[str], results: List[Dict[str, List[str]]]):
    """Функція для пошуку ключових слів у файлах в окремому потоці."""
    thread_results = {}
    for file in files:
        file_results = search_file(file, keywords)
        for keyword, found_files in file_results.items():
            if keyword not in thread_results:
                thread_results[keyword] = []
            thread_results[keyword].extend(found_files)
    results.append(thread_results)

def main():
    try:
        num_files = 5
        num_threads = 5
        directory = "test_files"
        
        create_files(num_files, directory)
        files = get_files_list(directory)
        keywords = generate_keywords(5)  # Генеруємо 5 випадкових ключових слів
        
        logging.info(f"Пошук ключових слів: {keywords}")
        
        # Розділяємо файли між потоками
        files_per_thread = len(files) // num_threads
        threads = []
        results = []
        
        start_time = time.time()
        
        for i in range(num_threads):
            start = i * files_per_thread
            end = start + files_per_thread if i < num_threads - 1 else None
            thread_files = files[start:end]
            thread = threading.Thread(target=thread_search, args=(thread_files, keywords, results))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        
        merged_results = merge_results(results)
        
        logging.info("\nРезультати пошуку:")
        for keyword, found_files in merged_results.items():
            logging.info(f"{keyword}: знайдено у {len(found_files)} файлах")
        
        logging.info(f"\nЧас виконання: {end_time - start_time:.2f} секунд")
    
    except Exception as e:
        logging.info(f"Виникла помилка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()