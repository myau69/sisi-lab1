from pathlib import Path
import xml.etree.ElementTree as ET

NS = {"owl": "http://www.w3.org/2002/07/owl#"}


def load_ontology(path):
    root = ET.parse(path).getroot()
    classes = {}
    relations = {}

    # class <--> object
    for fact in root.findall("owl:ClassAssertion", NS):
        name = fact.find("owl:Class", NS).get("IRI").lstrip("#")
        item = fact.find("owl:NamedIndividual", NS).get("IRI").lstrip("#")
        classes.setdefault(name, set()).add(item)

    # back/front
    for fact in root.findall("owl:SubClassOf", NS):
        child, parent = fact.findall("owl:Class", NS)
        child = child.get("IRI").lstrip("#")
        parent = parent.get("IRI").lstrip("#")
        classes.setdefault(parent, set()).update(classes.get(child, set()))

    # relations
    for fact in root.findall("owl:ObjectPropertyAssertion", NS):
        name = fact.find("owl:ObjectProperty", NS).get("IRI").lstrip("#")
        source, target = fact.findall("owl:NamedIndividual", NS)
        source = source.get("IRI").lstrip("#")
        target = target.get("IRI").lstrip("#")
        relations.setdefault(name, {}).setdefault(source, set()).add(target)

    return classes, relations


def recommend(classes, relations, language, database):
    results = []
    for framework in classes.get("framework", set()):
        if language not in relations.get("uses_language", {}).get(framework, set()):
            continue
        if database is None:
            results.append((framework, language, "—"))
        else:
            supported = relations.get("support_db", {}).get(framework, set())
            for db in supported & classes.get("subd", set()):
                if database == "любая" or database == db:
                    results.append((framework, language, db))
    return sorted(results)


def main():
    try:
        classes, relations = load_ontology(Path(__file__).with_name("Untitled.owx"))
    except (OSError, ET.ParseError) as error:
        print(f"Не удалось прочитать онтологию: {error}")
        return

    print("\nПОДБОР ТЕХНОЛОГИЧЕСКОГО СТЕКА")
    directions = {"бэк": "backend", "бек": "backend", "backend": "backend",
                  "фронт": "frontend", "frontend": "frontend"}
    while True:
        answer = input("Что разрабатываете — бэк или фронт? ").strip().lower()
        if answer in directions:
            direction = directions[answer]
            break
        print("Напишите «бэк» или «фронт».")

    languages = set()
    for framework in classes.get("framework", set()):
        languages.update(relations.get("uses_language", {}).get(framework, set()))
    languages &= classes.get(direction, set())
    if not languages:
        print("Для этого направления в онтологии нет фреймворков с указанным языком.")
        return
    print("\nДоступные языки: " + ", ".join(sorted(languages)))
    while True:
        language = input("Какой язык предпочитаете? ").strip().lower()
        if language in languages:
            break
        print("Выберите один язык из списка.")

    database = None
    if direction == "backend":
        print("\nБазы данных: " + ", ".join(sorted(classes.get("subd", set()))))
        print("Можно ответить «любая» или «не нужна».")
        while True:
            database = input("Какая база данных нужна? ").strip().lower()
            if database in classes.get("subd", set()) | {"любая", "не нужна"}:
                break
            print("Выберите базу из списка, «любая» или «не нужна».")
        if database == "не нужна":
            database = None

    results = recommend(classes, relations, language, database)
    if not results:
        print("\nПодходящих вариантов не найдено.")
        return
    print(f"\nНайдено вариантов: {len(results)}\n")
    print(f"{'Фреймворк':<14} | {'Язык':<8}" + (" | База данных" if database else ""))
    print("-" * 40)
    for framework, language, db in results:
        print(f"{framework:<14} | {language:<8}" + (f" | {db}" if database else ""))


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nПодбор отменён.")
