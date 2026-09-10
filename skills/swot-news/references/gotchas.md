# Kagi News API — ловушки

Проверено живьём 2026-07-02, спека: https://news.kagi.com/api/openapi

**`from`/`to` в `/api/search` → HTTP 500 в любом ISO-формате.** Полнотекст по title+summary
всех ~188 категорий работает (`totalCount`/`hasMore`), но окно задать нельзя — дефолт
«свежие батчи». Бывает 429 без документированных цифр.

**`lang=ru` заявлен в preTranslated, но отдаёт английский контент** с
`translationAvailable: false` — перевод батча доезжает не всегда и не сразу. Скилл остаётся
на `en`.

**Категория адресуется UUID, слаг даёт 404.** UUID берётся из
`/api/batches/latest/categories`. Картинки историй:
`/api/batches/{batch}/categories/{cat_uuid}/stories` отдаёт `primary_image`/`secondary_image` —
объекты `{url, caption, credit, link}` через прокси kagiproxy.com; у статей-источников есть
`image`/`image_caption`.

**Картинки доезжают в батч с задержкой в часы:** через ~1.5 ч — пусто, через ~20 ч — 12/12.
Потребителям нужна graceful degradation, а не ожидание.

**`totalStories` врёт на `offset=0`** — там он равен длине страницы (fast path); истинный
тотал виден только при `offset>0`.

**`batchId` принимает и UUID, и dateSlug** (`2026-07-01.1`) — доступ к историческим батчам
без поиска UUID. `/api/batches?from&to` даёт список с флагом `isComplete`; батчей бывает
2 в день (`.2`).

**Числовые rate-лимиты документированы только для SSE-переводов** (30 req/min с IP,
10 одновременных). Core-эндпоинты без лимитов: ~40 запросов в 8 потоков проходят.

**Данные под CC BY-NC 4.0** — атрибуция обязательна.
