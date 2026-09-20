# Trend Discovery

The goal is not “the most viral AI news.” It is a current signal that can become an ordinary person's specific problem and useful action.

## Evidence types

Collect four kinds of signals and keep their labels: `news`, `use_case`, `pain_point`, `behaviour`. Release announcements, community posts and product launches are different evidence, even when they refer to the same event.

## Source roles

- Official product pages and changelogs verify what a product does and who can use it.
- X, Reddit, open forums and public video/social posts reveal discussion and concrete use reports. Attribute these to the post; do not generalize from a handful of authors.
- GitHub releases/issues and Product Hunt help find tools and developer activity. High stars or launch votes do not automatically make a topic useful to ordinary readers.
- Hacker News is a lower-weight technical discovery signal.
- Chinese self-media and community sources are first-class inputs when accessible: Xiaohongshu, Zhihu, Weibo, Douyin, Bilibili, public WeChat article search, Toutiao public hot list, Juejin AI hot list and 36Kr search. The adapter must identify which platform each signal came from.
- Some Chinese endpoints return a hot list without publication times. Keep those records marked undated and out of the current-trend shortlist; the existence of a row in today's search does not prove the post itself is new.
- Public Chinese sources may use an existing read-only OpenCLI adapter or a documented public endpoint. Do not bypass logins, CAPTCHAs or platform restrictions; do not read creator backends or publish content as part of trend collection.
- WeChat Channels currently has no public read-only search command in the available adapter. Report it unavailable instead of implying that public videos were sampled.

## Collection windows

Default to 72 hours. Expand to 7 days only when the available set is too small. Support 24h, 3d, 7d and 30d. Always return the actual window, `collected_at`, successful sources, unavailable sources and errors.

## Pipeline

1. Collect small result sets from independent adapters. Each adapter returns `items`, `status`, `reason` and `collected_at`.
2. Normalize into the `TrendItem` schema. Unknown engagement values stay null.
3. Remove duplicate URLs and near-identical titles.
4. Cluster related evidence around an event or use case. Do not make one official release plus five reposts look like six independent trends.
5. Rank ordinary-person usefulness. Keep scores and evidence visible.
6. Transform the cluster into a person, problem, AI action and result. Reject a cluster if this cannot be stated with evidence and a plausible practical path.
7. Return up to ten candidates without padding. Separate `trend`, `hybrid` and `evergreen`.

## Safe degradation

Sources are optional and fail independently. A timeout, absent command, API token requirement, login wall, CAPTCHA or rate limit marks only that source unavailable. Continue with the other sources. If no viable current signal remains, say so and offer clearly labeled evergreen opportunities.

The local adapters use public endpoints and, when installed, OpenCLI read commands with the user's existing login state. They do not create or reuse credentials, solve CAPTCHAs, bypass access controls or perform write actions. Check each platform's current limits before adding a new adapter.
