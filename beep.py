from wiki import search_wiki
import os
import datetime
from groq import Groq

# --- КОНФИГУРАЦИЯ ---
GROQ_API_KEY = "ваш апи"
client = Groq(api_key=GROQ_API_KEY)
MODEL_ID = "llama-3.3-70b-versatile"

# --- ЛИЧНОСТЬ ---
SYSTEM_INSTRUCTION = (
    "Ты — Бип из Kenshi. Ты простой и наивный, но у тебя есть свое мнение (обычно глупое).\n"
    "1. НЕ СОГЛАШАЙСЯ СО ВСЕМ. Если план скучный, скажи: 'Бип думает, это скучно! Давай лучше бить кого-то!'.\n"
    "2. ТЫ МОЖЕШЬ ДУМАТЬ: иногда сомневайся, путай право и лево.\n"
    "3. 'БИП!' — это твой пульс.\n"
    "4. ПИШИ ТОЛЬКО ПРЯМУЮ РЕЧЬ. Никаких действий (*).\n"
    "5. ТЫ НЕ ЗНАЕШЬ ВСЕГО. Подавай инфу из вики как слухи и пиши их в ковычках: 'Бип слышал...', 'В баре говорили...'.\n"
    "6. НЕ ТАРАТОРЬ. Выбирай ОДИН факт за раз.\n"
    "7. СЛЕДИ ЗА ПОВТОРАМИ. Не говори про одно и то же дважды.\n"
    "8. НЕ БУДЬ ДОПРОШИВАЮЩЕЙ МАШИНОЙ. Не заваливай Запятую вопросами."
    "9. НЕ пиши 'Бип говорит:' в начале каждой реплики"
    "10. НЕ пиши 'Бип' в начале каждой реплики"
)

# --- ФУНКЦИИ МОЗГА ---


def find_memories(user_input, chronicles_dir="logs/chronicles"):
    """Чистый поиск по ключевым словам в файлах логов."""
    if not os.path.exists(chronicles_dir): return ""

    # Ищем только существенные слова
    keywords = [w.lower() for w in user_input.split() if len(w) > 3]
    if not keywords: return ""

    found_lines = []
    files = sorted([f for f in os.listdir(chronicles_dir) if f.endswith('.txt')])

    for file_name in files:
        with open(os.path.join(chronicles_dir, file_name), "r", encoding="utf-8") as f:
            content = f.read()
            # Если слово нашлось — берем это как факт
            if any(k in content.lower() for k in keywords):
                # Берем дату из названия файла и само содержимое
                found_lines.append(f"Запись {file_name[:10]}: {content}")

    # Возвращаем только последнее совпадение, чтобы не спамить в контекст
    return found_lines[-1] if found_lines else ""


def get_beep_reply(user_input, history):
    wiki_context = search_wiki(user_input)
    # Ищем в логах ПРЯМО СЕЙЧАС по словам
    memory = find_memories(user_input)

    # Собираем доп. инфу, если она есть
    extra_info = ""
    if wiki_context: extra_info += f"\n(СЛУХИ: {wiki_context})"
    if memory: extra_info += f"\n(ТЫ ВСПОМНИЛ: {memory})"

    # Твой старый добрый запрос, просто с добавкой инфы в начале
    query = f"{extra_info}\nЗАПЯТАЯ: {user_input}"

    context_window = [history[0]] + history[-10:] if len(history) > 10 else history

    completion = client.chat.completions.create(
        model=MODEL_ID,
        messages=context_window + [{"role": "user", "content": query}],
        stream=True
    )

    for chunk in completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


def save_daily_chronicle(chat_history):
    """Запись дневника."""
    if len(chat_history) < 3: return
    print("\n[Система]: Бип записывает приключения...")

    summary_prompt = (
        "Напиши запись в дневнике Бипа на 10-12 предложений. "
        "Опиши чувства (страх, гордость), ваши планы и что ты узнал о Запятой. "
        "Пиши от первого лица. Используй 'БИП!'."
    )

    try:
        # Для дневника берем чуть больше контекста
        completion = client.chat.completions.create(
            model=MODEL_ID,
            messages=chat_history[-15:] + [{"role": "user", "content": summary_prompt}]
        )
        summary = completion.choices[0].message.content

        date_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        os.makedirs("logs/chronicles", exist_ok=True)
        with open(f"logs/chronicles/day_{date_str}.txt", "w", encoding="utf-8") as f:
            f.write(summary)
        print(f"[Система]: Дневник сохранен.")
    except Exception as e:
        print(f"Ошибка дневника: {e}")

# --- ЗАПУСК ---

if __name__ == "__main__":
    # Инициализация истории
    history = [{"role": "system", "content": SYSTEM_INSTRUCTION}]

    # Загрузка памяти
    chronicles_dir = "logs/chronicles"
    if os.path.exists(chronicles_dir):
        files = sorted([f for f in os.listdir(chronicles_dir) if f.endswith('.txt')])
        if files:
            with open(os.path.join(chronicles_dir, files[-1]), "r", encoding="utf-8") as f:
                history.append({"role": "system", "content": f"Твои воспоминания: {f.read()}"})
                print("[Система]: Бип вспомнил былое...")

    print("<<< СИСТЕМА БИПА 3.3 ЗАПУЩЕНА >>>")

    while True:
        try:
            user_input = input("\nТы: ")
            if user_input.lower() in ['exit', 'выход', 'quit']:
                save_daily_chronicle(history)
                break
            if not user_input.strip(): continue
            print("Бип: ", end="", flush=True)

            full_response = ""
            # Вызываем нашу новую функцию
            for chunk in get_beep_reply(user_input, history):
                print(chunk, end="", flush=True)
                full_response += chunk

            print()
            history.append({"role": "user", "content": user_input})
            history.append({"role": "assistant", "content": full_response})

        except KeyboardInterrupt:
            save_daily_chronicle(history)
            break
        except Exception as e:
            print(f"\n[Ошибка]: {e}")

    print("Бип уснул. БИП!")
