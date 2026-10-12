### Университет ИТМО
### Факультет Программной Инженерии и Компьютерной Техники
### Системы искусственного интеллекта
# Отчёт по ЛР 1

## Реализация первой части
```prolog
% ================================
% Факты с одним аргументом
% ================================
% Бэкенд языки
language(go).
language(java).
language(ruby).
% Фронтенд технологии
language(html).
language(css).
language(js).
% Фреймворки
framework(spring).
framework(jakartaee).
framework(gin).
framework(chi).
framework(rails).
framework(react).
framework(vue).
framework(angular).
% СУБД
subd(postgres).
subd(redis).
subd(mysql).
subd(oracle).
subd(mongodb).
% Инфра
infra(docker).
infra(kuber).
infra(nginx).
% ================================
% Факты с двумя аргументами
% ================================
% Фреймворки языков
uses_language(gin, go).
uses_language(chi, go).
uses_language(spring, java).
uses_language(jakartaee, java).
uses_language(rails, ruby).
uses_language(react, js).
uses_language(vue, js).
uses_language(angular, js).
supports_db(spring, postgres).
supports_db(spring, mysql).
supports_db(gin, postgres).
supports_db(rails, redis).
% Найти фреймворки, использующие один язык
% Пример:
% same_language(gin, X).
same_language(F1, F2) :-
    uses_language(F1, L),
    uses_language(F2, L),
    F1 \= F2.
% Получить язык, используемый фреймворком
framework_language(F, L) :-
    framework(F),
    language(L),
    uses_language(F, L).
% Проверить поддержку СУБД фреймворком
can_use_db(F, DB) :-
    framework(F),
    subd(DB),
    supports_db(F, DB).
% Найти полный backend-стек: язык, фреймворк, СУБД
stack(L, F, DB) :-
    language(L),
    framework(F),
    subd(DB),
    uses_language(F, L),
    supports_db(F, DB).

% Найти два фреймворка, поддерживающих одну СУБД
common_db(F1, F2, DB) :-
    framework(F1),
    framework(F2),
    supports_db(F1, DB),
    supports_db(F2, DB),
    F1 \= F2.

% Найти две разные СУБД, поддерживаемые фреймворком
alternative_db(F, DB1, DB2) :-
    supports_db(F, DB1),
    supports_db(F, DB2),
    DB1 \= DB2.

% Найти фреймворки, для которых не указана поддержка СУБД
no_db_info(F) :-
    framework(F),
    \+ supports_db(F, _).

```


## Запросы к базе знаний Prolog
### 1. Проверка существования языка программирования
```prolog
language(go).
```
### 2. Поиск всех фреймворков JavaScript
```prolog
uses_language(F, js).
```
### 3. Поиск всех СУБД, поддерживаемых Spring 
```prolog
supports_db(spring, DB).
```
### 4. Поиск всех фреймворков, использующих тот же язык, что и Gin
```prolog
same_language(gin, F).
```
### 5. Поиск фреймворков на Go или Java, для которых не указана поддержка PostgreSQL
```prolog
framework(F),
(uses_language(F, go); uses_language(F, java)),
\+ supports_db(F, postgres).
```
### 6. Поиск технологических стеков с альтернативными СУБД
```prolog
stack(L, F, DB1),
alternative_db(F, DB1, DB2).
```
**Результат: два стека на Spring с PostgreSQL и MySQL, которые можно использовать как альтернативы друг другу.**
### 7. Поиск фреймворков на разных языках, поддерживающих одну СУБД
```prolog
common_db(F1, F2, DB),
framework_language(F1, L1),
framework_language(F2, L2),
L1 \= L2.
```
**Результат: Spring (Java) и Gin (Go) поддерживают PostgreSQL. Пара появится в обоих порядках.**
### 8. Поиск фреймворков, для которых неизвестна поддержка СУБД, но есть альтернативы на том же языке
```prolog
no_db_info(F1),
same_language(F1, F2),
can_use_db(F2, DB).
```
**Результат: jakartaee можно заменить на spring с PostgreSQL или MySQL; chi — на gin с PostgreSQL.**
### 9. Поиск фреймворков, поддерживающих PostgreSQL, но не MySQL
```prolog
framework(F),
supports_db(F, postgres),
\+ supports_db(F, mysql).
```
**Результат: gin.**
### 10. Поиск языков, для которых существуют как минимум два разных фреймворка
```prolog
language(L),
framework_language(F1, L),
framework_language(F2, L),
F1 @< F2.
```
**Результат: пары gin/chi, spring/jakartaee, а также пары из react, vue, angular.**
### 11. Поиск стеков, у которых есть альтернативный фреймворк на том же языке, но без указанной поддержки СУБД
```prolog
stack(L, F1, DB),
same_language(F1, F2),
no_db_info(F2).
```
**Результат: стеки Spring с альтернативой Jakarta EE и стек Gin с альтернативой Chi.**
### 12. Поиск пар фреймворков на одном языке, у которых один поддерживает PostgreSQL, а другой — нет по данным БЗ
```prolog
same_language(F1, F2),
supports_db(F1, postgres),
\+ supports_db(F2, postgres).
```
**Результат: spring/jakartaee и gin/chi**