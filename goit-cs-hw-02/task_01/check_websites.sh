#!/bin/bash

# Масив URL-адрес для перевірки
websites=(
    "https://google.com"
    "https://facebook.com"
    "https://twitter.com"
)

# Назва файлу для логів
log_file="website_status.log"

# Очищення файлу логів перед записом нових даних
> $log_file

# Перевірка кожного вебсайту
for site in "${websites[@]}"
do
    # Використання curl для перевірки доступності сайту
    if curl -s -L -o /dev/null -w "%{http_code}" "$site" | grep -q "200"; then
        status="UP"
    else
        status="DOWN"
    fi

    # Запис результату в файл логів
    echo "$site is $status" >> "$log_file"
done

# Вивід повідомлення про завершення
echo "Перевірка завершена. Результати записано у файл $log_file"

# Виведення вмісту файлу логів
cat "$log_file"

