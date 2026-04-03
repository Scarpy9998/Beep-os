BEEP-OS v1.0
> Предупреждение: Проект создан нейронкой, а я вайбкодер. Не желал подобное делать, но сам бы я это не осилил.
Также стоит отметить что логика верчения Бипа написана другим человеком и вот его пост на Реддит:

https://www.reddit.com/r/HalfLife/s/UkfcGXP1dM

 Советую перейти и посмотреть

Итак что это за проект
> Этот проект представляет собой чат с Бипом (Kenshi) в терминале 

Состав проекта:
> Ядро с личностью Бипа. Это рабочая программа, но при запуске работает в голом терминале.
> Интерфейс. Это тот файл, который вырисовывает интерфейс, что логично. Запускать следует именно его.
> Модуль Вики. Позволяет Бипу читать Вики. Чтобы пополнить Вики, следует поставить текстовые файлы с информацией в соответствующую папку. Я немного заполнил эту папку, но проверьте нравится ли мое вики вам

Горячие клавиши:

Ctrl+C - убить процесс

Ctrl+S - сохранить диалог в дневник бипа/логи


Долговременная память ИИ работает через пересказ всего произошедшего в дневник Бипа в папку логов. Я предоставил свои примеры на данном гитхабе, но актуален только последний, ибо я изменял пару раз промт. настроить это вы также можете в основном файле под названием beep.py.

Советую также разделять txt в папке вики для того чтобы поисковику, а также ии было легче работать

Тестировалось на:
> OS: Void Linux / i3wm
> Terminals: cool-retro-term, terminator
> AI: Groq Free API (Llama-3.3-70b-versatile)


Перед использованием найдите и вставьте в beep.py в следущую строку свой ключ:

GROQ_API_KEY = "ваш апи"


Гайд на установку 

1. Установка Python и зависимостей
Если у тебя еще нет Python, поставь его (пример для Void):
`bash
sudo xbps-install -S python3 python3-pip

2. Клонирование и настройка

git clone [https://github.com/Scarpy9998/Beep-os.git](https://github.com/Scarpy9998/Beep-os.git)
cd Beep-os

3. Создание виртуального окружения

python3 -m venv venv
source venv/bin/activate
pip install groq psutil

4. ВАЖНО: Права доступа
Если Бип молчит или ругается на "Permission Denied", просто дай ему права на его же память и слухи:

sudo chown -R $USER:$USER .
chmod -R 755 logs/ wiki/

5. Запуск

Для полного погружения используй cool-retro-term:

python3 interface.py

6. Этот гайд не отменяет остальных советов из этого файла. на самом деле мне очень лень было все переписывать ради гайда


Планы на будущее

На данный момент всё работает через API. Адаптация проекта под локальные нейронки пока только планируется. Также планируется добавить ещё несколько модулей:
> ВНИМАНИЕ Диагностика и слежка за вашим ПК. Отключить это можно будет в любой момент. Сделаю я это для себя, дабы Бип мог реагировать на различные процессы, такие как запуск Стима и подобное. Естественно этот модуль можно выключить, изменить, удалить, но пока его даже нет
> Модуль "ОКО". Это модуль, который позволяет захватывать текст по бинду. (Пока этого нет, повторяю).

 Настройка и кастомизация
Личность и Вики
Промты, определяющие личность Бипа, хранятся в beep.py. Также там можно настроить, каким образом будет отображаться информация из Вики для Бипа. Например, как «слухи в баре».


В файле interface.py можно заменить следующее:
> Арт Бипа (один, где он молчит, и один, где говорит).
> Арт справа сверху. Задумывался как арт локаций из Kenshi. Пока что эта опция не интерактивна. На данный момент там находится «арт смирения».
> Статус-бар. Выключить/включить можно в файле interface.py, изменив значение status_bar_h = 0 (не работает) или status_bar_h = 3 (работает) внутри функции def render_ui():.



Могу отметить тот факт что проект весьма легко изменить в том числе заменив Бипа на другого персонажа, изменив его промты, на что я полностью даю разрешение и позволяю всем сделать своих любимых персонажей ибо это круто.


Требуемые библиотеки

Для работы необходимы следующие Python-пакеты:

> pip install psutil groq

(Или аналоги в зависимости от вашего ключа и модели).


Кстати я без понятия насколько проект может считаться безопасным поэтому надеюсь не взломаю ничей ПК. По крайней мере такой цели у меня нет



BEEP-OS v1.0
> Warning: This project was created by a neural network, and I'm just a hobbyist coder. I didn't want to do something like this, but I couldn't have managed it on my own.
It's also worth noting that the logic behind BEEP was written by someone else, and here's their post on Reddit:

https://www.reddit.com/r/HalfLife/s/UkfcGXP1dM

I recommend checking it out

So, what is this project?
> This project is a chat with Beep (Kenshi) at the terminal

Project components:
> The core with Beep’s personality. This is the main program, but it runs in a bare-bones terminal when launched.
> Interface. This is the file that renders the interface, which makes sense. This is the one you should run.
> Wiki module. Allows Bip to read the Wiki. To populate the Wiki, place text files containing information in the corresponding folder. I’ve filled this folder a bit, but check if you like my Wiki

Keyboard shortcuts:

Ctrl+C - Kill process

Ctrl+S - Save dialog to log

The AI’s long-term memory works by logging everything that happened in Beep’s diary to the logs folder. I’ve provided my examples on this GitHub, but only the latest one is relevant, since I’ve changed the prompt a couple of times. You can also configure this in the main file named beep.py.

I also recommend splitting the txt files into a separate folder within the wiki to make it easier for the search engine and the AI to work.

Tested on:
> OS: Void Linux / i3wm
> Terminals: cool-retro-term, terminator
> AI: Groq Free API (Llama-3.3-70b-versatile)


Before using this, locate and replace the following line in beep.py with your API key:

GROQ_API_KEY = “your API key”

Installation Guide 

1. Installing Python and dependencies
If you don't have Python yet, install it (example for Void):
`bash
sudo xbps-install -S python3 python3-pip

2. Cloning and setting up

git clone [https://github.com/Scarpy9998/Beep-os.git](https://github.com/Scarpy9998/Beep-os.git)
cd Beep-os

3. Creating a virtual environment

python3 -m venv venv
source venv/bin/activate
pip install groq psutil

4. IMPORTANT: Permissions
If Beep is silent or complains about “Permission Denied,” just give it access to its own memory and logs:

sudo chown -R $USER:$USER .
chmod -R 755 logs/ wiki/

5. Running

For a full immersion experience, use cool-retro-term:

python3 interface.py

6. This guide does not supersede the other tips in this file. To be honest, I was too lazy to rewrite everything just for the guide


Future Plans

Currently, everything works via the API. Adapting the project for local neural networks is still only in the planning stages. There are also plans to add a few more modules:
> WARNING: Diagnostics and monitoring of your PC. You can disable this at any time. I’m doing this for myself so that Bip can react to various processes, such as launching Steam and similar actions. Of course, this module can be disabled, modified, or deleted, but it doesn’t even exist yet
> The “OKO” module. This is a module that allows you to capture text via a hotkey. (I repeat: this doesn’t exist yet.)


 Configuration and Customization
Personality and Wiki
The prompts that define Beep’s personality are stored in beep.py. You can also configure how information from the Wiki will be displayed for Beep there. For example, as “bar talk.”


In the interface.py file, you can replace the following:
> Beep's art (one where he is silent, and one where he is speaking).
> Art in the top-right corner. It was conceived as location art from Kenshi. This option is not interactive yet. Currently, it displays the “art of humility.”
> Status bar. You can toggle it on or off in the interface.py file by changing the value status_bar_h = 0 (off) or status_bar_h = 3 (on) inside the def render_ui(): function.



I should note that the project is very easy to modify, including replacing Bip with another character or changing his prompts, which I fully permit and encourage everyone to create their own favorite characters because that’s cool.


Required libraries

The following Python packages are required to run the project:

> pip install psutil groq

(Or equivalents depending on your key and model).


By the way, I have no idea how secure this project is, so I hope I don’t hack anyone’s PC. At least, that’s not my intention.


Translated with DeepL.com (free version)
