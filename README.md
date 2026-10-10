# Smart Search (Scraper)

A Dify tool plugin that turns a single question into a **multi-round, LLM-driven web
research pass** and returns a structured, balanced summary.

It runs the same plan → search → judge → re-search → report pipeline as
[Smart Search (Full)](https://github.com/Kagurazaka135/dify-smart-search-full), but
instead of calling a paid search API it **reads public search result pages directly**
(Bing / DuckDuckGo HTML). That means it works out of the box with **no search API key**.

## What it does

```
[1] Query expansion    -> the workspace LLM proposes 2-3 search angles
[2] Search             -> reads public result pages (Bing, then DuckDuckGo)
[3] Quality scoring    -> the LLM counts relevant hits and rates sufficiency
                          -> "not enough" and rounds remain? go back to [1] with new angles
[4] Content fetch      -> optional, opt-in: pull page text from high-quality URLs
[5] Structured summary -> positive / negative / neutral points, each with sources
```

Every LLM call runs through Dify's **reverse invocation**: the plugin uses the
workspace's own models and credentials, and never holds an LLM API key of its own.

## Parameters

| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `query` | string | yes | — | The question or topic to research. |
| `model` | model-selector | yes | — | Workspace LLM used for expansion, scoring and summarization. |
| `max_rounds` | number | no | `3` | Maximum search rounds before the plugin stops refining. |
| `fetch_content` | boolean | no | `false` | Fetch and read page text from top result URLs. |

## Output

```json
{
  "search_process": [
    {"round": 1, "queries": ["..."], "relevant": 5, "verdict": "not enough"}
  ],
  "supporting": [{"point": "...", "sources": ["https://..."]}],
  "opposing": [{"point": "...", "sources": ["https://..."]}],
  "neutral_facts": [{"fact": "...", "source": "https://..."}],
  "summary": "200-300 word synthesis with a confidence judgement.",
  "confidence": "high | medium | low"
}
```

## Setup

1. Install the plugin in a self-hosted Dify.
2. **No credentials are required.** The provider is usable as soon as it is installed.
3. Add the `Smart Search` tool to an agent or workflow, pick a model, and run it.

The plugin degrades gracefully across backends: if Bing returns nothing or is
unreachable, it tries DuckDuckGo.

## A note on the approach

This plugin **reads search engine result pages directly instead of using an official
search API**. That is a deliberate design choice: it needs no API key and no account.
It also means it may be outside the terms of service of the sites it reads, so it is
intended for **personal and self-hosted use**. If you need a version that only talks
to official search APIs, use
[Smart Search (Full)](https://github.com/Kagurazaka135/dify-smart-search-full).

## Outbound network access

The plugin makes outbound requests **only** to the following destinations:

- Search result pages:
  - `https://cn.bing.com`
  - `https://html.duckduckgo.com`
- Result-page URLs, **only when `fetch_content` is enabled**.

No other host is contacted.

## The two versions

This plugin is one half of a pair. Its sibling, **Smart Search (Full)**
([repository](https://github.com/Kagurazaka135/dify-smart-search-full)), runs the
exact same plan → search → judge → re-search → report pipeline, but swaps the search
layer out. Pick whichever trade-off fits your setup:

| | **Scraper** (this plugin) | **Full** |
|---|---|---|
| Search layer | Reads public result pages directly (HTML) | Official search APIs |
| Backends | Bing / DuckDuckGo | Serper / SerpApi / Google CSE / Bing / SearXNG |
| Credentials | **None** | At least one API key |
| `fetch_content` | Fetches directly, no `robots.txt` check | Honors `robots.txt` |
| Intended for | Personal & self-hosted use | Marketplace / general use |

Want a version that only talks to official APIs — and can be published to the
marketplace? Use the Full version. This one trades that compliance for zero setup:
no keys, no accounts.

## License

MIT
