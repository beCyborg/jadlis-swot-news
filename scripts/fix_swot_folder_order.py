#!/usr/bin/env python3
"""Чинит порядок папки выпусков в data.json плагина Obsidian manual-sorting.

Плагин держит порядок custom-сортировки в
`<vault>/.obsidian/plugins/manual-sorting/data.json`. Выпуски, созданные
автопрогоном при закрытом Obsidian, в этот порядок не попадают, а сам порядок
со временем накапливает инверсии. Скрипт пересобирает `children` папки выпусков
из реального содержимого, сортируя по ISO-дате из имени файла DESC (новые
сверху); файлы без даты в имени уходят вниз. Чистая сортировка по имени не
годится: кириллица в Unicode старше латиницы, и заметки с кириллическими
именами всплывали бы над `SWOT_*`.

Гвард: при запущенном Obsidian плагин держит порядок в памяти и перезапишет
файл при любом событии в vault — в этом случае ничего не правим (при открытом
Obsidian плагин сам ставит новые файлы наверх, `newItemPlacement: top`).

Пути берутся из конфига `.swot-news/config.json` (`base_dir`, `issues_dir`);
корень vault определяется как ближайший предок `base_dir` с папкой `.obsidian`.
Шаг выполняется, только если в конфиге `obsidian.enabled = true`.

Использование:
    python3 fix_swot_folder_order.py [--config <путь>] [--force]

Exit-коды: 0 — порядок записан, уже корректен, шаг пропущен (Obsidian запущен /
`obsidian.enabled = false` / плагин не установлен); 1 — ошибка (нет конфига,
нет папки выпусков и т.п.).

Только стандартная библиотека, Python 3.9+.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

CONFIG_RELPATH = Path(".swot-news") / "config.json"
PLUGIN_DATA_RELPATH = Path(".obsidian") / "plugins" / "manual-sorting" / "data.json"

for _stream in (sys.stdout, sys.stderr):  # Windows-консоль по умолчанию не UTF-8
    try:
        _stream.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001 — на старых Python метода нет, это не фатально
        pass


def find_config(explicit=None):
    """--config → env SWOT_NEWS_CONFIG → ./.swot-news/config.json → вверх по дереву."""
    if explicit:
        p = Path(explicit).expanduser()
        return p if p.is_file() else None
    env = os.environ.get("SWOT_NEWS_CONFIG")
    if env:
        p = Path(env).expanduser()
        if p.is_file():
            return p
    here = Path.cwd().resolve()
    for d in [here, *here.parents][:8]:
        p = d / CONFIG_RELPATH
        if p.is_file():
            return p
    for p in sorted(here.glob(f"*/{CONFIG_RELPATH.as_posix()}")):
        if p.is_file():
            return p
    return None


def vault_root_of(base_dir: Path):
    """Ближайший предок base_dir (включая её саму) с папкой .obsidian."""
    for d in [base_dir, *base_dir.parents]:
        if (d / ".obsidian").is_dir():
            return d
    return None


def obsidian_running() -> bool:
    try:
        return subprocess.run(
            ["pgrep", "-x", "Obsidian"], capture_output=True
        ).returncode == 0
    except (OSError, ValueError):  # нет pgrep (Windows) — считаем, что не запущен
        return False


def sort_key(name: str):
    m = re.search(r"\d{4}-\d{2}-\d{2}", name)
    return (m.group(0) if m else "0000-00-00", name)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", help="путь к .swot-news/config.json")
    ap.add_argument("--force", action="store_true",
                    help="править data.json даже при запущенном Obsidian")
    args = ap.parse_args()

    cfg_path = find_config(args.config)
    if cfg_path is None:
        print("Конфиг swot-news не найден — шаг пропущен.", file=sys.stderr)
        return 1
    try:
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"Не удалось прочитать {cfg_path}: {e}", file=sys.stderr)
        return 1

    if not cfg.get("obsidian", {}).get("enabled"):
        print("obsidian.enabled = false — порядок папки не трогаем.")
        return 0

    base_dir = Path(cfg.get("base_dir", cfg_path.parent.parent)).expanduser()
    issues_dir = base_dir / cfg.get("issues_dir", "Выпуски")
    if not issues_dir.is_dir():
        print(f"Нет папки выпусков: {issues_dir}", file=sys.stderr)
        return 1

    vault = vault_root_of(base_dir)
    if vault is None:
        print("Vault Obsidian не найден (нет .obsidian над base_dir) — шаг пропущен.")
        return 0

    data_json = vault / PLUGIN_DATA_RELPATH
    if not data_json.is_file():
        print("Плагин manual-sorting не установлен — шаг пропущен.")
        return 0

    if obsidian_running() and not args.force:
        print("Obsidian запущен — data.json не трогаем (плагин перезапишет из памяти; "
              "новые файлы он ставит наверх сам). Разовая починка: закрыть Obsidian "
              "и перезапустить скрипт, либо --force после отключения плагина.")
        return 0

    try:
        folder_key = issues_dir.relative_to(vault).as_posix()
    except ValueError:
        print("Папка выпусков вне vault — шаг пропущен.")
        return 0

    try:
        data = json.loads(data_json.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"Не удалось прочитать {data_json}: {e}", file=sys.stderr)
        return 1

    actual = sorted(
        (f"{folder_key}/{n}" for n in os.listdir(issues_dir) if not n.startswith(".")),
        key=lambda p: sort_key(os.path.basename(p)),
        reverse=True,
    )

    entry = data.setdefault("customOrder", {}).setdefault(
        folder_key, {"children": [], "sortOrder": "custom"}
    )
    if entry.get("children") == actual:
        print(f"Порядок уже корректен ({len(actual)} файлов).")
        return 0

    before = len(entry.get("children", []))
    entry["children"] = actual

    fd, tmp = tempfile.mkstemp(dir=str(data_json.parent), prefix=".data.json.")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, data_json)
    except BaseException:
        os.unlink(tmp)
        raise
    print(f"Порядок пересобран: было {before}, стало {len(actual)} (DESC по дате в имени).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
