# Fact integrity

## Fact classes

### F1 — protected factual literals

Never casually rewrite:
- exact numbers
- dates
- prices
- percentages
- benchmark scores
- version strings
- model names
- command lines
- API routes
- URLs
- configuration keys

### F2 — product behavior

Describe only from current evidence. Qualify platform/account/plan/date when behavior may vary.

### F3 — personal experience

Only the user can supply the underlying experience. Do not manufacture:
- “我用了三天”
- “我踩了这个坑”
- “我客户反馈”
- “我测试了 20 次”

### F4 — interpretation

Make the boundary explicit:
- fact: “官方文档新增了 X”
- interpretation: “这意味着团队可能更重视 Y”

Do not present interpretation as a documented motive.
