English · [Русский](README.md)

# You know what happened in the world, and not what any of it changes for you

The Kagi News sections you picked are read by parallel analysts through a file holding your
profile, and the daily note gets only the delta — what appeared, what escalated, what is fading.

```
claude plugin marketplace add https://github.com/beCyborg/jadlis-start.git
claude plugin install swot-news@jadlis
```

No keys needed — there is a single source and it is the public Kagi News API; before the first
issue, though, run the onboarding `/swot-news:setup` in the folder where the notes will live.

![The general news stream passes through a file with your profile, and out come a short daily issue and a topic card](docs/img/hero-jadlis-swot-news.webp)

In words: on the left the general news stream, in the middle the file with your profile, on the
right a short daily issue and a card for a topic that has held for more than one day.

This is my workbench published as it is, not a product: whatever I stopped using, I removed.

## Before → after

| By hand | With an AI chat | With this plugin |
|---|---|---|
| **Whose importance this is.** A feed sorts by importance in general, and your part in the event is not in it. | It retells and shortens whatever you bring it: it has no profile to select against. | Every story passes through `Контекст.md` — occupation, location, priorities, interests and non-interests — and reaches the issue only if it changes something for you. |
| **The same topic every day.** It comes back indistinguishable from yesterday, and you cannot tell whether it moved or stood still. | It works the topic out from scratch again, with no yesterday's version beside it. | It matches the topic against the base cards and the watchlist and writes a delta: new, escalation, fading; what did not change goes out in a single line. |
| **What is left the next morning.** The tabs are closed, nothing remains. | The analysis stays in the chat log and is lost right there. | The issue and the cards are Markdown files in your folder; a topic that holds for more than a day becomes a card with a history, and an abandoned one archives itself. |
| **A day with no news.** You scroll anyway: you cannot see in advance that nothing came out. | It answers any request, even when there is nothing to answer about. | It compares the fresh batch `batch_id` with the last issue: batch no newer — no file is created, one line goes to the chat. |
| **Who presses the button.** The ritual rests on you and breaks in the first busy week. | It needs a live dialogue: without your answers the turn does not end. | The daily skill has the question tool switched off inside the skill itself, and the turn has to finish on its own — so it can go into `/schedule`. |

## How it works

![Config and a freshness check, then clusters fan out to parallel analysts, and out come the daily issue and the cards](docs/img/how-jadlis-swot-news.webp)

Going in — the fresh Kagi News batch across the sections you picked, and your `Контекст.md`.
Inside — a config gate and a batch freshness check, then the categories fan out into clusters,
one analyst per cluster, while the "monitor daily" topics go to the enricher out on the web.
Coming out — the daily issue, updated base cards, and a digest in the chat.

In words: config → batch freshness check → collection by category → analysts and the enricher in
parallel → the delta assembled → the issue file → cards and watchlist → the digest.

Collecting the data is one script on the Python standard library: it pulls the batch by a pinned
`batch_id` so that `/latest` cannot switch mid-collection, and lays the categories out into cluster
files in the system temp folder. Those files are never read into the main context — an analyst gets
a path and walks it with grep and offsets. There are one to four analysts, one per cluster; each
returns candidates with two scores, force of impact and likelihood, and with a delta status against
the topics already known.

Filing the day's findings into the base is a separate step, and its order of operations is fixed:
first the watchlist cleanup, then matching against the cards, then promoting a watchlist topic into
a card, then new topics and the fading check. A topic left unmentioned for long enough is first
marked as fading and then archived — the file itself is never deleted. The issue is written in one
of two markup modes: the onboarding checks whether the folder sits inside an Obsidian vault and
turns on either wikilinks with callouts, or plain Markdown.

## Installing and the first run

**a) Text to paste to an agent.** Copy the whole thing into a Claude Code chat:

```
You are the installer. Install the plugin swot-news from the jadlis marketplace on this machine.
First check the interpreter: python3 --version; not found — python --version, then py -3 --version.
If the version is below 3.9, or none of the commands worked, stop and tell me: without Python
the plugin cannot collect the news.
Then run exactly these commands, verbatim, shortening nothing:
1. claude plugin marketplace add https://github.com/beCyborg/jadlis-start.git
2. claude plugin install swot-news@jadlis
3. claude plugin list — show me the line about swot-news and its version.
This plugin asks for no keys: the news source is a public API with no key.
Do not run the onboarding /swot-news:setup yourself — I will run it from my own working folder.
Before each command show it to me in full and wait for "yes". If I say "no", do not run it,
tell me what you skipped, and move on.
If a command returns an error, stop, show me the output, and do not move to the next one.
```

**b) Commands by hand.**

```
claude plugin marketplace add https://github.com/beCyborg/jadlis-start.git
claude plugin install swot-news@jadlis
claude plugin list
```

The first command installs nothing — it adds the marketplace. Only the second one installs, and one
line removes it: `claude plugin uninstall swot-news@jadlis --keep-data`.

**c) The short command.** There is no entry skill under the bare plugin name here: `/swot-news` will
not be found, the commands are written in their full form. Open Claude Code in the folder where the
issues will live and go through the onboarding once:

```
/swot-news:setup
```

Then, in the same folder, the daily run:

```
/swot-news:daily-news-swot
```

If they are not found, check the plugin name with `claude plugin list`. Nothing is configured at
install time: every setting appears during the onboarding and lands in `.swot-news/config.json`
next to your notes. The daily skill looks for that file from the working folder upwards through the
folder tree, and one level inwards as well — so it has to be run in that same folder, in a subfolder
of it, or in the folder above. Working from somewhere else entirely — the path to the config is set
by the `SWOT_NEWS_CONFIG` environment variable. The Kagi batch comes out once a day, around noon
UTC; running it makes sense once the batch is out.

## Limits, cost, updating

**What it does not do.** It does not go looking for news itself: there is one source, the public
Kagi News API, and what is not in its batch will not be in the issue either. It does not cross-verify
claims: the enricher goes to the web only for the topics in the "monitor daily" section, and only to
see whether the status has changed since yesterday. It does not translate the batch — `lang=ru` on
that API returns English content, so the analysis runs on the English batch while the issue is
written in Russian. It does not create an issue until a fresh batch is out; if you need one anyway —
`/swot-news:daily-news-swot --force`. It does not write outside your working folder, apart from the
system temp folder that holds the cluster files for the length of a run. And it does not send your
profile anywhere: `Контекст.md` is read locally and only ever reaches the prompts of subagents
inside your own session.

**What you need.** No keys: the Kagi News API is public, status beta. You need Python 3.9 or newer,
and only as an interpreter — the script is written on the standard library and installs no
dependencies. Optional: the Brave Search MCP for the daily enrichment — without it the enricher
switches to Exa, without both to the built-in web search, and with an empty "monitor daily" section
it does not start at all; Obsidian — the onboarding notices the vault on its own and turns on
wikilinks, callouts and the `.base` dashboard. Kagi News data comes under CC BY-NC 4.0:
non-commercial use with attribution, and the attribution already sits in the footer of every issue —
it must not be removed from the template.

[уточнить] — I have never run this on Windows or Linux, even though the script handles `py -3` and
fixes the console encoding itself.

**How tokens get spent.** The heaviest part of a run is the analysts themselves: one to four of
them, one per cluster, plus the enricher — all in a single parallel pass. That is why the cluster
files never reach the main context; the subagents are handed paths only. Three knobs in the config
and in the Context make a run cheaper: fewer clusters, fewer entries in the issue budget, and an
empty "monitor daily" section — then the enricher never starts.

**Verified where I work:** my Mac, my subscription, my settings. Where else this works — [уточнить].

**Terms of use.** There is no license: all rights reserved by the author. You may read it and use it
personally. Commercial use, republishing and bundling it into your own products — by arrangement
with me.

**Updating.** With a third-party marketplace, auto-update is off on your side: until you run the
first command you keep the version you installed.

```
claude plugin marketplace update jadlis
claude plugin update swot-news@jadlis
claude plugin list
```

Reinstall, if something ended up crooked:

```
claude plugin uninstall swot-news@jadlis --keep-data && claude plugin install swot-news@jadlis
```
