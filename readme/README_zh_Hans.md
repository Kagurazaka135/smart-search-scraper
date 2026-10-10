# 智能搜索（裸爬版）

一个 Dify 工具插件：把单个问题变成**多轮、LLM 驱动的网页调研**，输出结构化、平衡的汇总。

它跟[智能搜索（满血版）](https://github.com/Kagurazaka135/dify-smart-search-full)跑同一套
「拆词 → 搜索 → 评质 → 重搜 → 汇总」流水线，但**不调付费搜索 API，而是直接读取公开搜索结果页**
（Bing / DuckDuckGo HTML）。所以它**开箱即用、零搜索 API key**。

## 它做什么

```
[1] 拆词       -> 让工作区 LLM 生成 2-3 个搜索角度
[2] 搜索       -> 直接读取公开结果页（先 Bing，再 DuckDuckGo）
[3] 评质       -> LLM 统计相关条数并给出"够/勉强/不够"
                  -> 不够且还有轮数？带着新角度回到 [1]
[4] 抓正文     -> 可选、需显式开启：从高质量结果 URL 取正文
[5] 结构化汇总 -> 正/反/中性观点，每条带来源
```

所有 LLM 调用都走 Dify 的**反向调用**：插件用工作区自己的模型和凭据，
自身不持有任何 LLM 密钥。

## 参数

| 名称 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `query` | string | 是 | — | 要调研的问题或主题。 |
| `model` | model-selector | 是 | — | 用于拆词、评质、汇总的工作区 LLM。 |
| `max_rounds` | number | 否 | `3` | 停止细化前的最大搜索轮数。 |
| `fetch_content` | boolean | 否 | `false` | 是否抓取并阅读高质量结果的正文。 |

## 输出

```json
{
  "search_process": [
    {"round": 1, "queries": ["..."], "relevant": 5, "verdict": "not enough"}
  ],
  "supporting": [{"point": "...", "sources": ["https://..."]}],
  "opposing": [{"point": "...", "sources": ["https://..."]}],
  "neutral_facts": [{"fact": "...", "source": "https://..."}],
  "summary": "200-300 字的综合判断。",
  "confidence": "high | medium | low"
}
```

## 配置

1. 在自建 Dify 里安装本插件。
2. **无需任何凭据**——装完即可用。
3. 把 `Smart Search` 工具加进 agent 或 workflow，选好模型即可运行。

插件会在后端间优雅降级：Bing 无结果或不可达时，自动尝试 DuckDuckGo。

## 关于实现方式

本插件**直接读取搜索引擎结果页，而不是调用官方搜索 API**。这是刻意的取舍：
它不需要 API key、不需要账号。也正因如此，它可能落在被读取站点的服务条款之外，
**定位是个人自用 / 自建环境**。如果你需要一个只走官方搜索 API 的版本，请用
[智能搜索（满血版）](https://github.com/Kagurazaka135/dify-smart-search-full)。

## 出站访问域名

插件**只会**向以下目标发起出站请求：

- 搜索结果页：
  - `https://cn.bing.com`
  - `https://html.duckduckgo.com`
- 结果页 URL，**仅在开启 `fetch_content` 时**。

不访问任何其他主机。

## 两个版本

本插件是一对姊妹插件中的"裸爬版"。另一位是**智能搜索（满血版）**
（[仓库](https://github.com/Kagurazaka135/dify-smart-search-full)），
跑**完全相同**的「拆词 → 搜索 → 评质 → 重搜 → 汇总」流水线，只把搜索层换掉。
按自己的场景挑取舍：

| | **裸爬版**（本插件） | **满血版** |
|---|---|---|
| 搜索层 | 直接读公开结果页（HTML） | 官方搜索 API |
| 后端 | Bing / DuckDuckGo | Serper / SerpApi / Google CSE / Bing / SearXNG |
| 凭据 | **零凭据** | 需至少一个 API key |
| `fetch_content` | 直接抓取，不查 `robots.txt` | 遵守 `robots.txt` |
| 定位 | 个人自用 / 自建环境 | 上架 marketplace / 通用 |

想要只走官方 API、能上架的版本 → 用满血版；本插件用它换零配置：不要 key、不要账号。

## 许可证

MIT
