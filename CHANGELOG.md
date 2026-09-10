# Changelog — jadlis-swot-news

Формат: [Keep a Changelog](https://keepachangelog.com/ru/1.1.0/), версии — [SemVer](https://semver.org/lang/ru/).

## [3.0.0] — 2026-09-10 — переименование плагина / plugin rename

### Для человека
- Плагин теперь называется `jadlis-swot-news`: ставится строкой `claude plugin install jadlis-swot-news@jadlis` из хаба `https://github.com/beCyborg/jadlis-hub`.
- Ежедневный прогон запускается короткой командой `/swot-news` (полная форма — `/jadlis-swot-news:swot-news`), онбординг — `/jadlis-swot-news:swot-news-setup`.
- Совместимости со старыми именами нет: переустанови плагин, старая установка `swot-news@jadlis` больше не обновляется.

### For agents
- Changed: `.claude-plugin/plugin.json` — `name` `swot-news` → `jadlis-swot-news`, `version` 2.0.1 → 3.0.0.
- Changed: `.claude-plugin/marketplace.json` — имя записи плагина → `jadlis-swot-news` (имя маркетплейса `swot-news-plugin` не менялось).
- Changed: `skills/daily-news-swot/` → `skills/swot-news/` (`git mv`), frontmatter `name: daily-news-swot` → `name: swot-news`; `skills/setup/` → `skills/swot-news-setup/` (`git mv`), `name: setup` → `name: swot-news-setup` (голое `/setup` конфликтовало с общим именем).
- Changed: `agents/*.md` — в `description` скилл-владелец теперь `jadlis-swot-news:swot-news`; имена файлов агентов не менялись.
- Changed: `README.md`, `README.en.md`, `docs/УСТАНОВКА.md`, `docs/НАСТРОЙКА.md`, `CLAUDE.md`, `skills/**`, `scripts/fetch_kagi_api.py`, `scripts/category_groups.json` — установочные строки, полные формы команд и пути `${CLAUDE_PLUGIN_ROOT}/skills/...`.
- Changed: `README.md`, `README.en.md` — пункт «Короткая команда» переписан: короткая команда `/swot-news` теперь существует (раньше в тексте утверждалось обратное).
- Changed: адрес хаба `beCyborg/jadlis-start` → `beCyborg/jadlis-hub` во всех текстах.
- Changed: `.github/workflows/plugin-validate.yml` — вызов `beCyborg/jadlis-hub/.github/workflows/plugin-ci.yml@main`.
- Migration: `claude plugin uninstall swot-news@jadlis --keep-data` → `claude plugin marketplace add https://github.com/beCyborg/jadlis-hub` → `claude plugin install jadlis-swot-news@jadlis`. Рабочая папка и `.swot-news/config.json` не меняются. Записи ниже описывают прошлые версии и сохраняют старые имена.

## [2.0.1] — 2026-09-07 — переименование репозитория / repository rename

### Для человека
- Репо переименовано в `jadlis-swot-news`, маркетплейс `jadlis` (`swot-news@jadlis`); старый адрес редиректит, старая установка продолжает работать.

### For agents
- Changed: `.claude-plugin/plugin.json` — `version` 2.0.0 → 2.0.1, `repository` → `https://github.com/beCyborg/jadlis-swot-news`, добавлен `homepage`.
- Changed: `.claude-plugin/marketplace.json` — `homepage` записи → новый адрес; имя маркетплейса `swot-news-plugin` оставлено без изменений.
- Changed: `README.md`, `README.en.md`, `docs/УСТАНОВКА.md` — установка через хаб `https://github.com/beCyborg/jadlis-start.git` → `swot-news@jadlis`; блок альтернативной установки из своего маркетплейса заменён строкой о том, что старые установки продолжают работать.
- Changed: `CLAUDE.md` — заголовок и адрес хаба.
- Changed: `.github/workflows/plugin-validate.yml` — вызов переиспользуемого workflow `beCyborg/jadlis-start/.github/workflows/plugin-ci.yml@main` (`mode: plugin` — репо root-as-plugin).
- Migration: не требуется, скиллы, агенты и скрипты не менялись.

## [2.0.0] — 2026-09-07 — переименование скилла и слияние локальной версии / skill rename and local merge

### Для человека
- Ежедневный скилл теперь вызывается как `/swot-news:daily-news-swot` — то же имя, что у локальной версии и в расписании.
- Агенты переименованы в `swot-news-analyst` / `swot-news-enricher` — тоже совпадают с локальными.
- Обогатитель научился переключаться на Exa, когда у Brave кончился лимит.

### For agents
- Changed: `skills/daily/` → `skills/daily-news-swot/` (`git mv`), `name: daily` → `name: daily-news-swot`; ссылки обновлены в `README.md`, `README.en.md`, `docs/УСТАНОВКА.md`, `skills/setup/SKILL.md`, `skills/setup/assets/SWOT.md`, `CLAUDE.md`.
- Changed: `agents/analyst.md` → `agents/swot-news-analyst.md`, `agents/enricher-brave.md` → `agents/swot-news-enricher.md`, `agents/enricher-web.md` → `agents/swot-news-enricher-web.md`; `subagent_type` в `skills/daily-news-swot/SKILL.md` теперь без префикса плагина.
- Changed: `agents/swot-news-enricher.md` — фоллбэк на `mcp__exa__web_search_exa` при 402/403 от Brave.
- Added: `skills/daily-news-swot/references/gotchas.md` — ловушки Kagi News API (перенос из локальной версии).
- Added: `scripts/fix_swot_folder_order.py` — порядок папки выпусков в Obsidian-плагине manual-sorting; фаза 7.5, выполняется только при `obsidian.enabled = true`.
- Breaking: старое имя команды `/swot-news:daily` и старые `subagent_type` больше не работают.

## [1.0.1] — 2026-09-06 — README RU/EN, CHANGELOG-формат, gitleaks в CI / bilingual README, changelog format, gitleaks in CI

### Для человека
- README переписан по пяти секциям и получил английскую версию рядом.
- В репо появился журнал изменений: видно, что и когда менялось.
- CI теперь ещё и проверяет, что в репозиторий не утёк ключ.

### For agents
- Added: `README.en.md` (EN) — пять секций плюс «Data and licences», паритет H2 с RU.
- Added: `CHANGELOG.md` в формате хаба (`### Для человека` / `### For agents`).
- Added: `CLAUDE.md` — конвенции репо (коммиты, релизы, README, приватность, разработка).
- Added: `docs/img/04-swot-news-01.webp`, `docs/img/04-swot-news-02.webp` — иллюстрации секции «Как выглядит».
- Added: job `gitleaks` в `.github/workflows/plugin-validate.yml` (`gitleaks/gitleaks-action@v2`, `fetch-depth: 0`).
- Changed: `README.md` — пять секций «Зачем / Как выглядит / Как поставить / Как пользоваться / Границы и стоимость» плюс «Данные и лицензии»; установка через хаб `swot-news@jadlis` вынесена основным путём, свой маркетплейс `swot-news@swot-news-plugin` — рядом.
- Changed: формулировки онбординга (`skills/setup/references/interview.md`, `category-selection.md`, `assets/Контекст.md`) и пример пути в `docs/НАСТРОЙКА.md` — сняты слова и личный путь, на которые срабатывает privacy-гейт; смысл вопросов и вариантов ответов прежний.
- Changed: `version` в `.claude-plugin/plugin.json` — 1.0.0 → 1.0.1 (patch).
- Migration: не требуется — логика скиллов, агенты и `scripts/fetch_kagi_api.py` не менялись.

## [1.0.0] — 2026-09-01 — первый релиз / first release

### Для человека
- `/swot-news:setup` — онбординг: разбор папки, интервью о профиле, проход по направлениям Kagi News, раскладка по кластерам, создание рабочей структуры.
- `/swot-news:daily` — ежедневный прогон: сбор → параллельный анализ → дельта-выпуск → дайджест в чат. Вопросов не задаёт, годится для расписания.
- Анти-заглушка: батч не новее последнего выпуска — заметка не создаётся, мусорных файлов не остаётся.

### For agents
- Added: `skills/setup/` (шаги 0–8, `--recheck` / `--profile` / `--reset`, assets `Контекст.md`, `SWOT.md`, `_Watchlist.md`, `config.template.json`, `swot-all.base`, `settings-snippet.json`).
- Added: `skills/daily/` (фазы 0–6, references: `context-loading.md`, `aggregation-rules.md`, `daily-note-template.md`, `markdown-modes.md`, `swot-card-template.md`, `dialog-protocol.md`).
- Added: `agents/analyst.md`, `agents/enricher-brave.md`, `agents/enricher-web.md`.
- Added: `scripts/fetch_kagi_api.py` (stdlib, Python 3.9+; режимы `--list-categories`, `--build-clusters`, `--self-check`, `--check-freshness`), `scripts/category_groups.json`.
- Added: `docs/УСТАНОВКА.md`, `docs/НАСТРОЙКА.md`, `.claude-plugin/marketplace.json`, `LICENSE` (MIT), CI `.github/workflows/plugin-validate.yml`.
