import os

def search_wiki(query, folder_path="wiki_base"):
    """Ищет совпадения по всем .txt файлам в папке wiki_base"""
    if not os.path.exists(folder_path):
        return ""

    keywords = [word.lower() for word in query.split() if len(word) > 3]
    if not keywords: return ""

    found_info = []

    # Сканируем всю папку wiki_base
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), "r", encoding="utf-8") as f:
                for line in f:
                    if any(key in line.lower() for key in keywords):
                        # Добавляем инфу с пометкой, из какого она файла
                        found_info.append(f"[{filename}]: {line.strip()}")

    return f"\nИНФОРМАЦИЯ ИЗ ЗНАНИЙ:\n" + "\n".join(found_info[:2]) if found_info else ""
