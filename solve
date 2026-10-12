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
