# jadlis-swot-news — конвенции репо

Root-as-plugin репозиторий: сам корень и есть плагин `jadlis-swot-news` (`.claude-plugin/plugin.json`), рядом — свой маркетплейс `swot-news-plugin` (`.claude-plugin/marketplace.json`). Основной канал раздачи — хаб `jadlis` (`beCyborg/jadlis-hub`), подшаг 6.3 маршрута передачи. Эти правила читает агент, который коммитит.

## Коммиты

- Тема — Conventional Commits на английском: `type(scope): subject`, ≤72 символа. `scope` = `daily` (скилл `skills/swot-news/`), `setup`, `agents`, `scripts`, `docs`, `ci`.
- Тело двухслойное:
  1. `Что изменилось:` — 1–3 предложения по-русски простым языком, для человека.
  2. `Details (for agents):` — буллеты `Added / Changed / Removed / Migration / Refs` с путями.
- Без строк атрибуции (`Co-Authored-By` и подобных).

## Релизы

- Версия живёт только в `.claude-plugin/plugin.json`; бамп — в том же коммите, что и изменение.
- Тег `jadlis-swot-news--v{X.Y.Z}` (до 3.0.0 — `swot-news--v…`) ставит и пушит в GitHub (`origin`) команда `claude plugin tag . --push`.
- `CHANGELOG.md`: `## [X.Y.Z] — ГГГГ-ММ-ДД — <кратко по-русски> / <short EN>`, затем `### Для человека` (≤3 буллета) и `### For agents` (`Added / Changed / Removed / Migration / Breaking`, с путями).
- После релиза обновить пин в маркетплейсе хаба: в `~/jadlis-hub` (ветка `main`) `python3 tools/bump-pin.py jadlis-swot-news jadlis-swot-news--v{X.Y.Z}`, коммит, `git push origin main`.
- Только patch-forward: никаких force-push, переписывания тегов и релизов.

## README и доки

- Пара `README.md` (RU) + `README.en.md` (EN); первая строка — переключатель `Русский · English` со ссылками друг на друга.
- Одинаковое число и порядок H2 в паре. Проверка: `python3 <хаб>/tools/readme-parity.py .`.
- Пять секций: **Зачем / Как выглядит / Как поставить / Как пользоваться / Границы и стоимость**; дополнительные H2 — только одинаково в обоих языках. Список ≤5 пунктов, первая строка секции — действие.
- Подробные инструкции живут в `docs/УСТАНОВКА.md` и `docs/НАСТРОЙКА.md` — README на них ссылается, а не дублирует.
- Иллюстрации — `docs/img/*.webp`; примеры вывода в README синтетические, реальных выпусков в репо нет.
- Числа и механика сверяются с кодом текущего тега; тег указывается рядом с числом.

## Приватность

- В репо нет ключей, почт, телефонов, путей владельца (`/Users/<имя>`) и содержимого чужих выпусков.
- Перед пушем: `gitleaks git .` и `python3 <хаб>/tools/privacy-grep.py .` (CI GitHub — reusable workflow `beCyborg/jadlis-hub/.github/workflows/plugin-ci.yml` — гоняет `validate` и `gitleaks`).
- Данные Kagi News — CC BY-NC 4.0: атрибуция в футере выпуска обязательна, из шаблонов её не убирать.

## Разработка

- `scripts/fetch_kagi_api.py` — только стандартная библиотека Python 3.9+; зависимостей не добавлять.
- Скилл `swot-news` не задаёт вопросов (`disallowed-tools: AskUserQuestion`) — он ходит по расписанию; вопросы живут только в `swot-news-setup`.
- Кластер-файлы в основной контекст не читать: агентам передаются пути.
- Перед коммитом: `claude plugin validate . --strict` и `claude plugin validate .claude-plugin/marketplace.json`. Этот файл лежит в `.claude/CLAUDE.md`: корневой `CLAUDE.md` валит `--strict`.
- Язык доков — русский (RU-файл первичен) плюс EN; код, идентификаторы и имена скиллов — английский.
