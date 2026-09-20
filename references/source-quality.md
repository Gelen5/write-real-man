# Source quality

Use separate evidence lanes for **what is true** and **what people are discussing**. A popular post does not verify product behavior; an official announcement does not prove public demand.

## Product facts — primary sources first

Prefer whenever available:
- official documentation
- official release notes / changelogs
- official GitHub repositories
- original paper / preprint
- official company or maintainer post
- direct API response / product UI observed by the user

## Use-case evidence — original users and practitioners

Useful for behavior and community context:
- repository issues / discussions
- maintainer or developer posts
- reproducible independent benchmarks with methodology
- high-quality technical writeups that link primary sources

## Trend signals — communities, search and activity

Use only as an attributed signal, not a population-level claim:
- Reddit threads
- X discussions
- Chinese creator and social platforms: Xiaohongshu, Zhihu, Weibo, Douyin, Bilibili, public WeChat article search, Toutiao, Juejin and 36Kr
- forum reactions
- anecdotal user reports

Record platform, URL, posted date, collection time and available engagement counts. Missing metrics stay `null`. One high-engagement post can be a useful lead, but it is not cross-platform confirmation.

Keep domestic platform results distinct from global communities. Search ranks, likes, views and hot-list values describe what one platform surfaced; they do not estimate all users. Public WeChat search may return relative dates such as “3 days ago”; normalize them against collection time and retain the original text for audit. If a platform provides no publication date, mark it undated and do not claim that it is a current trend.

## Avoid as sole evidence

- unattributed SEO aggregators
- content farms
- reposts that hide the original source
- AI summaries without citations

## Freshness

For model/API/tool behavior, record the source date. A 2025 tutorial is not sufficient evidence for a 2026 product behavior claim when newer official docs exist.

For candidate discovery use `72h` by default. If the sample is sparse, expand to `7d` and label that window in the output. Official sources establish release details and limits; they do not establish heat by themselves.
