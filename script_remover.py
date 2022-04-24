"""
Script removing all data inside all <script>
tags in all root directory and all inned folders
"""

import os
import pathlib
import re


p = pathlib.Path("") # Определяем корень, где лежит скрипт
pattern = r"(?is)(<script[^>]*>)(.*?)(</script>)" # Паттерн поиска тегов скрипта в html файлах


def del_script():
    html_names = []
    for root, dirs, files in os.walk(p): # Создание списка всех вложенных папок
        for file in files:
            if '.html' in file: # Удаляем из списка всё, что не html
                html_names.append([root, file]) # Создаём список из строк путь+название файла
    for file_name in html_names:
        with open(os.path.join(file_name[0], file_name[1]), encoding="utf8") as text: # Открываем
            text = text.read()                                                        # и читаем файлы
        result = []
        output = []
        try:
            holder = re.split(pattern, text) # Отделяем теги <script> и их содержимое от текста
            for el in range(len(holder)):
                if "<script" in holder[el-1]: # Удаляем текст из тегов
                    None
                else:
                    result.append(holder[el]) # Добавляем в отдельный список остальной контент
            for el in range(len(result)):
                if "<script" in result[el] or "</script" in result[el]: # ---
                    if "<script src=" in result[el]:                    # Удаляем все теги <script>
                        output.append(result[el])                       # в которых нет src=
                    if "<script src=" in result[el-1]:                  #
                        output.append(result[el])                       #---
                    else: None
                else: output.append(result[el]) # Добавляем остальной контент в список
            result = "".join(output) # Превращаем список в строку
        except: print ("Нет необработанных скриптов")
        try:
            with open (os.path.join(file_name[0], file_name[1]), "w", encoding="utf-8") as f:
                f.write(result) # Записываем строку в файл
        except: print ("Нет скриптов в файле, либо файл повреждён")



if __name__ == "__main__":
    cwd = os.getcwd()
    print (f"""Вы находитесь в {cwd}
при продолжении удалятся ВСЕ теги <script>
в текущей папке и во всех вложенных""")
    check_agree = input(f"Что бы продолжить, введите yes: ")
    if check_agree == "yes":
        del_script()
        print ("Все скрипты удалены")
    else:
        print ("Хух, ничего не удалено")