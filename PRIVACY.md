# Privacy Policy

## Data handled by this plugin

Smart Search (Scraper) is a tool plugin for Dify. It performs web search on behalf of
the user and produces a structured summary. To do this it processes:

- **The search query** the user submits, together with any derived search keywords.
- **Public search results** read from search result pages (title, snippet, URL).
- **Public page text** retrieved from result URLs, and only when the user explicitly
  enables the `fetch_content` option.

## Where data is sent

- **Search result pages**: `https://cn.bing.com` and `https://html.duckduckgo.com`.
  The search keywords are sent as query parameters to these pages.
- **The workspace language model** selected in the `model` parameter. Query expansion,
  quality scoring and summarization are performed by that model through Dify's
  reverse-invocation mechanism. The plugin never stores or sees any model API key.
- **Target pages**, only when `fetch_content` is enabled: the plugin requests the
  result URL and reads its visible text.

## What is stored

The plugin is **stateless**. It does not persist queries, results, or page content,
and it does not run any analytics or telemetry. All processing happens in-memory for
the duration of a single tool call.

## Credentials

This plugin requires **no credentials**. It holds no search API keys and no account
of its own.

## Contact

Open an issue in the plugin's repository for any privacy question.
