import string
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict, Counter
import requests
import matplotlib.pyplot as plt

def get_text_from_url(url):
    """Завантажує текст із заданої URL-адреси."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logging.info(f"Помилка при завантаженні тексту: {e}")
        return None

def remove_punctuation(text):
    """Видаляє знаки пунктуації з тексту."""
    return text.translate(str.maketrans("", "", string.punctuation))

def map_function(word):
    """Мапінг: створює пару (слово, 1)."""
    return word.lower(), 1

def shuffle_function(mapped_values):
    """Групує значення за ключами."""
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

def reduce_function(key_values):
    """Редукція: підсумовує кількість входжень кожного слова."""
    key, values = key_values
    return key, sum(values)

def map_reduce(text, search_words=None):
    """Виконує MapReduce на вхідному тексті."""
    text = remove_punctuation(text)
    words = text.split()
    if search_words:
        words = [word for word in words if word.lower() in search_words]

    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))
    
    shuffled_values = shuffle_function(mapped_values)
    
    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))
    
    return dict(reduced_values)

def visualize_top_words(word_counts, top_n=10):
    """Візуалізує топ N слів за частотою."""
    
    top_words = dict(Counter(word_counts).most_common(top_n))
    words = list(top_words.keys())
    frequencies = list(top_words.values())

    plt.figure(figsize=(12, 6))
    bars = plt.barh(words, frequencies, color='skyblue')
    plt.xlabel('Frequency')
    plt.ylabel('Words')
    plt.title(f'Top {top_n} Most Frequent Words')
    plt.gca().invert_yaxis()

    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2, f'{width}', 
                 ha='left', va='center')

    plt.tight_layout()
    plt.show()

def main():
    url = input("Введіть URL тексту для аналізу (або натисніть Enter для використання URL за замовчуванням): ")
    if not url:
        url = "https://www.gutenberg.org/files/1342/1342-0.txt"
    text = get_text_from_url(url)
    
    if text is None:
        return

    search_words = input("Введіть слова для пошуку (розділені пробілом) або натисніть Enter для аналізу сексуальності тексті: ").lower().split()
    
    try:
        word_counts = map_reduce(text, search_words if search_words else None)
        if not word_counts:
            logging.info(f"Не знайдено жодного слова по запиту: {', '.join(search_words)}")
            return
        logging.info("Загальна кількість унікальних слів:", len(word_counts))
        logging.info("Топ 10 слів:", Counter(word_counts).most_common(10))
        visualize_top_words(word_counts)
    except Exception as e:
        logging.info(f"Помилка при обробці тексту: {e}")

if __name__ == "__main__":
    main()