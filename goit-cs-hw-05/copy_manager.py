import asyncio
import argparse
import logging
import sys
from aiopath import AsyncPath
from aioshutil import copy2

# Налаштування логування
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def copy_file(source: AsyncPath, dest: AsyncPath):
    """Асинхронно копіює файл у відповідну підпапку."""
    try:
        ext = source.suffix.lower()[1:]  # Отримуємо розширення файлу без крапки
        if not ext:
            ext = 'no_extension'
        
        dest_folder = dest / ext
        await dest_folder.mkdir(exist_ok=True, parents=True)
        
        await copy2(source, dest_folder / source.name)
        logging.info(f"Скопійовано {source} в {dest_folder}")
    except Exception as e:
        logging.error(f"Помилка при копіюванні {source}: {str(e)}")

async def read_folder(source: AsyncPath, dest: AsyncPath):
    """Асинхронно читає всі файли у вихідній папці та її підпапках."""
    try:
        async for entry in source.rglob('*'):
            if await entry.is_file():
                await copy_file(entry, dest)
    except Exception as e:
        logging.error(f"Помилка при читанні {source}: {str(e)}")

async def main(source_folder: str, output_folder: str):
    source = AsyncPath(source_folder)
    dest = AsyncPath(output_folder)

    if not await source.exists():
        logging.error(f"Вихідна папка {source} не існує")
        return

    await dest.mkdir(exist_ok=True, parents=True)
    await read_folder(source, dest)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Асинхронне сортування файлів за розширенням")
    parser.add_argument("source", nargs='?', help="Шлях до вихідної папки")
    parser.add_argument("output", nargs='?', help="Шлях до папки призначення")
    args = parser.parse_args()

    if args.source is None or args.output is None:
        logging.info("Ви забули аргументи. Ваша команда в командній строці має відповідати наступній схемі:")
        logging.info("python3 copy_manager.py /шлях/до/вихідної/папки /шлях/до/папки/призначення")
        sys.exit(1)

    asyncio.run(main(args.source, args.output))