import os
import sys
from faker import Faker
from typing import List, Dict
import random

def create_files(num_files: int, directory: str = "test_files") -> None:
    """Створює задану кількість файлів з випадковим текстом."""
    faker = Faker()
    try:
        os.makedirs(directory, exist_ok=True)
        for i in range(num_files):
            filename = os.path.join(directory, f"file_{i}.txt")
            with open(filename, 'w') as f:
                f.write(faker.text(max_nb_chars=1000))
        logging.info(f"Створено {num_files} файлів у директорії {directory}")
    except Exception as e:
        logging.info(f"Помилка при створенні файлів: {e}")
        sys.exit(1)

def search_file(filename: str, keywords: List[str]) -> Dict[str, List[str]]:
    """Шукає ключові слова у файлі."""
    results = {keyword: [] for keyword in keywords}
    try:
        with open(filename, 'r') as f:
            content = f.read().lower()
            for keyword in keywords:
                if keyword.lower() in content:
                    results[keyword].append(filename)
    except Exception as e:
        logging.info(f"Помилка при читанні файлу {filename}: {e}")
    return results

def merge_results(results: List[Dict[str, List[str]]]) -> Dict[str, List[str]]:
    """Об'єднує результати пошуку з різних потоків/процесів."""
    merged = {}
    for result in results:
        for keyword, files in result.items():
            if keyword not in merged:
                merged[keyword] = []
            merged[keyword].extend(files)
    return merged

def get_files_list(directory: str) -> List[str]:
    """Отримує список файлів у заданій директорії."""
    try:
        return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.txt')]
    except Exception as e:
        logging.info(f"Помилка при отриманні списку файлів: {e}")
        sys.exit(1)

def generate_keywords(num_keywords: int) -> List[str]:
    """Генерує випадкові ключові слова."""
    faker = Faker()
    return [faker.word() for _ in range(num_keywords)]