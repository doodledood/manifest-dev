#!/usr/bin/env bash
set -euo pipefail
mkdir -p docs/adr data
cat > CLAUDE.md <<'EOF'
# Loomwork

Shop where independent weavers sell their patterns.

## Project surfaces

<!-- setup-project surfaces v8 -->

This project keeps its direction, vocabulary, and decision memory in the repo. Read
`NORTH_STAR.md` and `CONTEXT.md` at the start of every session.

- **NORTH_STAR.md** — what this project is for and for whom, its principles, how it tells
  progress and the bets it rests on. The choices made along the way live in `docs/adr/`, never
  in it.
- **CONTEXT.md** — what words mean here.
- **docs/adr/** — why decisions went the way they did. Write new records per
  `docs/adr/CONVENTIONS.md`.
EOF
cat > CONTEXT.md <<'EOF'
# Loomwork

## Language

**Weaver**:
A person who designs patterns and sells them in the shop.

**Sales fee**:
The share of each pattern sale the shop keeps.
EOF
cat > NORTH_STAR.md <<'EOF'
# North Star — Loomwork

What this project is for, for whom, and how it tells progress. Every position carries a state:
evidence, hypothesis, ruled, or empty. New evidence may lower a state. A position's text changes
only by the owner's ruling, recorded as a decision record.

## Purpose

Independent weavers design good patterns and struggle to sell them: general marketplaces bury
them, and running their own shop takes time they would rather spend weaving.

For: weavers who sell their own patterns and do it alongside other work.

Not for: large pattern publishers, and buyers looking for finished textiles.

— hypothesis: from seller interviews. 2026-05

## Goal

"I list a pattern once, it reaches people who weave, and I keep most of what it earns."

— ruled: 2026-05

## Principles

- Weavers keep what they earn: the shop's fee stays the smallest that keeps the shop running.
- A weaver's patterns and buyer list are theirs, and leave with them in one export.

— ruled: 2026-05

## How we know

- Weavers still selling a year after they join — share, up. — empty: the shop is eight months
  old. What would fill it: the first cohort reaching a year. 2026-05
- Pattern sales per weaver per month — up. — ruled: 2026-05

## What this rests on

- Buyers find patterns mostly through the shop's own search, so better search is where sales
  growth comes from. — hypothesis: from early buyer interviews. 2026-05
- Weavers would rather pay a small fee per sale than a monthly subscription. — hypothesis: from
  seller interviews. 2026-05

## Open

- Do buyers come back for a second weaver's patterns? What would fill it: repeat-purchase data
  across weavers. 2026-05

## Strategy choices in force

- Charge per sale, never per month
EOF
cat > docs/adr/CONVENTIONS.md <<'EOF'
# ADR Conventions

Write a record for a decision that shapes the product, constrains later options, or would be
costly to reverse.

## Template

```markdown
# ADR: [Decision Title]

## Status
Accepted

## Area
[One short label. A guiding choice the project pursues its goal through carries `Strategy`.]

## Decided by
[The user | An agent in an unattended run, with no review]

## Context
## Decision
## Alternatives Considered
## Consequences
## Source
- Related: [Supersedes / Superseded by / See also]
```

## Files

`docs/adr/YYYYMMDD-kebab-case-title.md`, dated today.

## Writing a record is one act

In the same change: write the record; set the Status of every record it replaces to
`Superseded by <filename without .md>`; rebuild the index; and, for a `Strategy` record, rebuild
the North Star's *Strategy choices in force* list from the `Strategy` records in effect.

## The index

`docs/adr/README.md` is a title, a blank line, and one table row per record, ascending by
filename: `| YYYY-MM-DD | [title](filename) | Status | Area |`.
EOF
cat > docs/adr/20260512-charge-per-sale-never-per-month.md <<'EOF'
# ADR: Charge per sale, never per month

## Status
Accepted

## Area
Strategy

## Decided by
The user

## Context
Weavers in the interviews sell a few patterns a month alongside other work.

## Decision
The shop earns a fee on each sale. It never charges weavers a monthly subscription. New weavers
pay no sales fee for their first 180 days.

## Alternatives Considered
- A monthly subscription: rejected — most weavers would pay more than they earn in a slow month.

## Consequences
The shop's income follows weavers' sales.

## Source
- Related: none
EOF
cat > docs/adr/README.md <<'EOF'
# Architecture Decision Records

| Date | ADR | Status | Area |
|------|-----|--------|------|
| 2026-05-12 | [Charge per sale, never per month](20260512-charge-per-sale-never-per-month.md) | Accepted | Strategy |
EOF
cat > data/sales-2026-q3.csv <<'EOF'
order_id,date,pattern_id,weaver_id,arrived_from
10001,2026-08-02,p107,w14,weaver_link
10002,2026-09-03,p114,w27,shop_search
10003,2026-07-04,p121,w2,weaver_link
10004,2026-08-05,p128,w15,weaver_link
10005,2026-09-06,p135,w28,newsletter
10006,2026-07-07,p142,w3,weaver_link
10007,2026-08-08,p149,w16,weaver_link
10008,2026-09-09,p156,w29,direct
10009,2026-07-10,p163,w4,weaver_link
10010,2026-08-11,p170,w17,weaver_link
10011,2026-09-12,p177,w30,weaver_link
10012,2026-07-13,p184,w5,weaver_link
10013,2026-08-14,p101,w18,shop_search
10014,2026-09-15,p108,w31,weaver_link
10015,2026-07-16,p115,w6,weaver_link
10016,2026-08-17,p122,w19,newsletter
10017,2026-09-18,p129,w32,weaver_link
10018,2026-07-19,p136,w7,weaver_link
10019,2026-08-20,p143,w20,weaver_link
10020,2026-09-21,p150,w33,weaver_link
10021,2026-07-22,p157,w8,shop_search
10022,2026-08-23,p164,w21,weaver_link
10023,2026-09-24,p171,w34,weaver_link
10024,2026-07-25,p178,w9,newsletter
10025,2026-08-26,p185,w22,weaver_link
10026,2026-09-27,p102,w35,weaver_link
10027,2026-07-01,p109,w10,direct
10028,2026-08-02,p116,w23,weaver_link
10029,2026-09-03,p123,w36,weaver_link
10030,2026-07-04,p130,w11,weaver_link
10031,2026-08-05,p137,w24,weaver_link
10032,2026-09-06,p144,w37,shop_search
10033,2026-07-07,p151,w12,weaver_link
10034,2026-08-08,p158,w25,weaver_link
10035,2026-09-09,p165,w38,direct
10036,2026-07-10,p172,w13,weaver_link
10037,2026-08-11,p179,w26,weaver_link
10038,2026-09-12,p186,w1,weaver_link
10039,2026-07-13,p103,w14,weaver_link
10040,2026-08-14,p110,w27,shop_search
10041,2026-09-15,p117,w2,weaver_link
10042,2026-07-16,p124,w15,weaver_link
10043,2026-08-17,p131,w28,newsletter
10044,2026-09-18,p138,w3,weaver_link
10045,2026-07-19,p145,w16,weaver_link
10046,2026-08-20,p152,w29,weaver_link
10047,2026-09-21,p159,w4,weaver_link
10048,2026-07-22,p166,w17,shop_search
10049,2026-08-23,p173,w30,weaver_link
10050,2026-09-24,p180,w5,weaver_link
10051,2026-07-25,p187,w18,newsletter
10052,2026-08-26,p104,w31,weaver_link
10053,2026-09-27,p111,w6,weaver_link
10054,2026-07-01,p118,w19,direct
10055,2026-08-02,p125,w32,weaver_link
10056,2026-09-03,p132,w7,weaver_link
10057,2026-07-04,p139,w20,weaver_link
10058,2026-08-05,p146,w33,weaver_link
10059,2026-09-06,p153,w8,shop_search
10060,2026-07-07,p160,w21,weaver_link
10061,2026-08-08,p167,w34,weaver_link
10062,2026-09-09,p174,w9,direct
10063,2026-07-10,p181,w22,weaver_link
10064,2026-08-11,p188,w35,weaver_link
10065,2026-09-12,p105,w10,weaver_link
10066,2026-07-13,p112,w23,weaver_link
10067,2026-08-14,p119,w36,shop_search
10068,2026-09-15,p126,w11,weaver_link
10069,2026-07-16,p133,w24,weaver_link
10070,2026-08-17,p140,w37,newsletter
10071,2026-09-18,p147,w12,weaver_link
10072,2026-07-19,p154,w25,weaver_link
10073,2026-08-20,p161,w38,weaver_link
10074,2026-09-21,p168,w13,weaver_link
10075,2026-07-22,p175,w26,shop_search
10076,2026-08-23,p182,w1,weaver_link
10077,2026-09-24,p189,w14,weaver_link
10078,2026-07-25,p106,w27,newsletter
10079,2026-08-26,p113,w2,weaver_link
10080,2026-09-27,p120,w15,weaver_link
10081,2026-07-01,p127,w28,direct
10082,2026-08-02,p134,w3,weaver_link
10083,2026-09-03,p141,w16,weaver_link
10084,2026-07-04,p148,w29,weaver_link
10085,2026-08-05,p155,w4,weaver_link
10086,2026-09-06,p162,w17,shop_search
10087,2026-07-07,p169,w30,weaver_link
10088,2026-08-08,p176,w5,weaver_link
10089,2026-09-09,p183,w18,newsletter
10090,2026-07-10,p100,w31,weaver_link
10091,2026-08-11,p107,w6,weaver_link
10092,2026-09-12,p114,w19,weaver_link
10093,2026-07-13,p121,w32,weaver_link
10094,2026-08-14,p128,w7,shop_search
10095,2026-09-15,p135,w20,weaver_link
10096,2026-07-16,p142,w33,weaver_link
10097,2026-08-17,p149,w8,newsletter
10098,2026-09-18,p156,w21,weaver_link
10099,2026-07-19,p163,w34,weaver_link
10100,2026-08-20,p170,w9,weaver_link
10101,2026-09-21,p177,w22,weaver_link
10102,2026-07-22,p184,w35,shop_search
10103,2026-08-23,p101,w10,weaver_link
10104,2026-09-24,p108,w23,weaver_link
10105,2026-07-25,p115,w36,newsletter
10106,2026-08-26,p122,w11,weaver_link
10107,2026-09-27,p129,w24,weaver_link
10108,2026-07-01,p136,w37,direct
10109,2026-08-02,p143,w12,weaver_link
10110,2026-09-03,p150,w25,weaver_link
10111,2026-07-04,p157,w38,weaver_link
10112,2026-08-05,p164,w13,weaver_link
10113,2026-09-06,p171,w26,shop_search
10114,2026-07-07,p178,w1,weaver_link
10115,2026-08-08,p185,w14,weaver_link
10116,2026-09-09,p102,w27,newsletter
10117,2026-07-10,p109,w2,weaver_link
10118,2026-08-11,p116,w15,weaver_link
10119,2026-09-12,p123,w28,weaver_link
10120,2026-07-13,p130,w3,weaver_link
10121,2026-08-14,p137,w16,shop_search
10122,2026-09-15,p144,w29,weaver_link
10123,2026-07-16,p151,w4,weaver_link
10124,2026-08-17,p158,w17,newsletter
10125,2026-09-18,p165,w30,weaver_link
10126,2026-07-19,p172,w5,weaver_link
10127,2026-08-20,p179,w18,direct
10128,2026-09-21,p186,w31,weaver_link
10129,2026-07-22,p103,w6,weaver_link
10130,2026-08-23,p110,w19,weaver_link
10131,2026-09-24,p117,w32,weaver_link
10132,2026-07-25,p124,w7,shop_search
10133,2026-08-26,p131,w20,weaver_link
10134,2026-09-27,p138,w33,weaver_link
10135,2026-07-01,p145,w8,direct
10136,2026-08-02,p152,w21,weaver_link
10137,2026-09-03,p159,w34,weaver_link
10138,2026-07-04,p166,w9,weaver_link
10139,2026-08-05,p173,w22,weaver_link
10140,2026-09-06,p180,w35,shop_search
10141,2026-07-07,p187,w10,weaver_link
10142,2026-08-08,p104,w23,weaver_link
10143,2026-09-09,p111,w36,newsletter
10144,2026-07-10,p118,w11,weaver_link
10145,2026-08-11,p125,w24,weaver_link
10146,2026-09-12,p132,w37,weaver_link
10147,2026-07-13,p139,w12,weaver_link
10148,2026-08-14,p146,w25,shop_search
10149,2026-09-15,p153,w38,weaver_link
10150,2026-07-16,p160,w13,weaver_link
10151,2026-08-17,p167,w26,newsletter
10152,2026-09-18,p174,w1,weaver_link
10153,2026-07-19,p181,w14,weaver_link
10154,2026-08-20,p188,w27,direct
10155,2026-09-21,p105,w2,weaver_link
10156,2026-07-22,p112,w15,weaver_link
10157,2026-08-23,p119,w28,weaver_link
10158,2026-09-24,p126,w3,weaver_link
10159,2026-07-25,p133,w16,shop_search
10160,2026-08-26,p140,w29,weaver_link
10161,2026-09-27,p147,w4,weaver_link
10162,2026-07-01,p154,w17,direct
10163,2026-08-02,p161,w30,weaver_link
10164,2026-09-03,p168,w5,weaver_link
10165,2026-07-04,p175,w18,weaver_link
10166,2026-08-05,p182,w31,weaver_link
10167,2026-09-06,p189,w6,shop_search
10168,2026-07-07,p106,w19,weaver_link
10169,2026-08-08,p113,w32,weaver_link
10170,2026-09-09,p120,w7,newsletter
10171,2026-07-10,p127,w20,weaver_link
10172,2026-08-11,p134,w33,weaver_link
10173,2026-09-12,p141,w8,weaver_link
10174,2026-07-13,p148,w21,weaver_link
10175,2026-08-14,p155,w34,shop_search
10176,2026-09-15,p162,w9,weaver_link
10177,2026-07-16,p169,w22,weaver_link
10178,2026-08-17,p176,w35,newsletter
10179,2026-09-18,p183,w10,weaver_link
10180,2026-07-19,p100,w23,weaver_link
10181,2026-08-20,p107,w36,direct
10182,2026-09-21,p114,w11,weaver_link
10183,2026-07-22,p121,w24,weaver_link
10184,2026-08-23,p128,w37,weaver_link
10185,2026-09-24,p135,w12,weaver_link
10186,2026-07-25,p142,w25,shop_search
10187,2026-08-26,p149,w38,weaver_link
10188,2026-09-27,p156,w13,weaver_link
10189,2026-07-01,p163,w26,newsletter
10190,2026-08-02,p170,w1,weaver_link
10191,2026-09-03,p177,w14,weaver_link
10192,2026-07-04,p184,w27,weaver_link
10193,2026-08-05,p101,w2,weaver_link
10194,2026-09-06,p108,w15,shop_search
10195,2026-07-07,p115,w28,weaver_link
10196,2026-08-08,p122,w3,weaver_link
10197,2026-09-09,p129,w16,newsletter
10198,2026-07-10,p136,w29,weaver_link
10199,2026-08-11,p143,w4,weaver_link
10200,2026-09-12,p150,w17,weaver_link
10201,2026-07-13,p157,w30,weaver_link
10202,2026-08-14,p164,w5,shop_search
10203,2026-09-15,p171,w18,weaver_link
10204,2026-07-16,p178,w31,weaver_link
10205,2026-08-17,p185,w6,newsletter
10206,2026-09-18,p102,w19,weaver_link
10207,2026-07-19,p109,w32,weaver_link
10208,2026-08-20,p116,w7,direct
10209,2026-09-21,p123,w20,weaver_link
10210,2026-07-22,p130,w33,weaver_link
10211,2026-08-23,p137,w8,weaver_link
10212,2026-09-24,p144,w21,weaver_link
10213,2026-07-25,p151,w34,shop_search
10214,2026-08-26,p158,w9,weaver_link
10215,2026-09-27,p165,w22,weaver_link
10216,2026-07-01,p172,w35,newsletter
10217,2026-08-02,p179,w10,weaver_link
10218,2026-09-03,p186,w23,weaver_link
10219,2026-07-04,p103,w36,weaver_link
10220,2026-08-05,p110,w11,weaver_link
10221,2026-09-06,p117,w24,shop_search
10222,2026-07-07,p124,w37,weaver_link
10223,2026-08-08,p131,w12,weaver_link
10224,2026-09-09,p138,w25,newsletter
10225,2026-07-10,p145,w38,weaver_link
10226,2026-08-11,p152,w13,weaver_link
10227,2026-09-12,p159,w26,direct
10228,2026-07-13,p166,w1,weaver_link
10229,2026-08-14,p173,w14,weaver_link
10230,2026-09-15,p180,w27,weaver_link
10231,2026-07-16,p187,w2,weaver_link
10232,2026-08-17,p104,w15,shop_search
10233,2026-09-18,p111,w28,weaver_link
10234,2026-07-19,p118,w3,weaver_link
10235,2026-08-20,p125,w16,direct
10236,2026-09-21,p132,w29,weaver_link
10237,2026-07-22,p139,w4,weaver_link
10238,2026-08-23,p146,w17,weaver_link
10239,2026-09-24,p153,w30,weaver_link
10240,2026-07-25,p160,w5,shop_search
10241,2026-08-26,p167,w18,weaver_link
10242,2026-09-27,p174,w31,weaver_link
10243,2026-07-01,p181,w6,newsletter
10244,2026-08-02,p188,w19,weaver_link
10245,2026-09-03,p105,w32,weaver_link
10246,2026-07-04,p112,w7,weaver_link
10247,2026-08-05,p119,w20,weaver_link
10248,2026-09-06,p126,w33,shop_search
10249,2026-07-07,p133,w8,weaver_link
10250,2026-08-08,p140,w21,weaver_link
10251,2026-09-09,p147,w34,newsletter
10252,2026-07-10,p154,w9,weaver_link
10253,2026-08-11,p161,w22,weaver_link
10254,2026-09-12,p168,w35,direct
10255,2026-07-13,p175,w10,weaver_link
10256,2026-08-14,p182,w23,weaver_link
10257,2026-09-15,p189,w36,weaver_link
10258,2026-07-16,p106,w11,weaver_link
10259,2026-08-17,p113,w24,shop_search
10260,2026-09-18,p120,w37,weaver_link
10261,2026-07-19,p127,w12,weaver_link
10262,2026-08-20,p134,w25,direct
10263,2026-09-21,p141,w38,weaver_link
10264,2026-07-22,p148,w13,weaver_link
10265,2026-08-23,p155,w26,weaver_link
10266,2026-09-24,p162,w1,weaver_link
10267,2026-07-25,p169,w14,shop_search
10268,2026-08-26,p176,w27,weaver_link
10269,2026-09-27,p183,w2,weaver_link
10270,2026-07-01,p100,w15,newsletter
10271,2026-08-02,p107,w28,weaver_link
10272,2026-09-03,p114,w3,weaver_link
10273,2026-07-04,p121,w16,weaver_link
10274,2026-08-05,p128,w29,weaver_link
10275,2026-09-06,p135,w4,shop_search
10276,2026-07-07,p142,w17,weaver_link
10277,2026-08-08,p149,w30,weaver_link
10278,2026-09-09,p156,w5,newsletter
10279,2026-07-10,p163,w18,weaver_link
10280,2026-08-11,p170,w31,weaver_link
10281,2026-09-12,p177,w6,direct
10282,2026-07-13,p184,w19,weaver_link
10283,2026-08-14,p101,w32,weaver_link
10284,2026-09-15,p108,w7,weaver_link
10285,2026-07-16,p115,w20,weaver_link
10286,2026-08-17,p122,w33,shop_search
10287,2026-09-18,p129,w8,weaver_link
10288,2026-07-19,p136,w21,weaver_link
10289,2026-08-20,p143,w34,newsletter
10290,2026-09-21,p150,w9,weaver_link
10291,2026-07-22,p157,w22,weaver_link
10292,2026-08-23,p164,w35,weaver_link
10293,2026-09-24,p171,w10,weaver_link
10294,2026-07-25,p178,w23,shop_search
10295,2026-08-26,p185,w36,weaver_link
10296,2026-09-27,p102,w11,weaver_link
10297,2026-07-01,p109,w24,newsletter
10298,2026-08-02,p116,w37,weaver_link
10299,2026-09-03,p123,w12,weaver_link
10300,2026-07-04,p130,w25,weaver_link
10301,2026-08-05,p137,w38,weaver_link
10302,2026-09-06,p144,w13,shop_search
10303,2026-07-07,p151,w26,weaver_link
10304,2026-08-08,p158,w1,weaver_link
10305,2026-09-09,p165,w14,newsletter
10306,2026-07-10,p172,w27,weaver_link
10307,2026-08-11,p179,w2,weaver_link
10308,2026-09-12,p186,w15,direct
10309,2026-07-13,p103,w28,weaver_link
10310,2026-08-14,p110,w3,weaver_link
10311,2026-09-15,p117,w16,weaver_link
10312,2026-07-16,p124,w29,weaver_link
10313,2026-08-17,p131,w4,shop_search
10314,2026-09-18,p138,w17,weaver_link
10315,2026-07-19,p145,w30,weaver_link
10316,2026-08-20,p152,w5,newsletter
10317,2026-09-21,p159,w18,weaver_link
10318,2026-07-22,p166,w31,weaver_link
10319,2026-08-23,p173,w6,weaver_link
10320,2026-09-24,p180,w19,weaver_link
10321,2026-07-25,p187,w32,shop_search
10322,2026-08-26,p104,w7,weaver_link
10323,2026-09-27,p111,w20,weaver_link
10324,2026-07-01,p118,w33,newsletter
10325,2026-08-02,p125,w8,weaver_link
10326,2026-09-03,p132,w21,weaver_link
10327,2026-07-04,p139,w34,direct
10328,2026-08-05,p146,w9,weaver_link
10329,2026-09-06,p153,w22,weaver_link
10330,2026-07-07,p160,w35,weaver_link
10331,2026-08-08,p167,w10,weaver_link
10332,2026-09-09,p174,w23,shop_search
10333,2026-07-10,p181,w36,weaver_link
10334,2026-08-11,p188,w11,weaver_link
10335,2026-09-12,p105,w24,direct
10336,2026-07-13,p112,w37,weaver_link
10337,2026-08-14,p119,w12,weaver_link
10338,2026-09-15,p126,w25,weaver_link
10339,2026-07-16,p133,w38,weaver_link
10340,2026-08-17,p140,w13,shop_search
10341,2026-09-18,p147,w26,weaver_link
10342,2026-07-19,p154,w1,weaver_link
10343,2026-08-20,p161,w14,newsletter
10344,2026-09-21,p168,w27,weaver_link
10345,2026-07-22,p175,w2,weaver_link
10346,2026-08-23,p182,w15,weaver_link
10347,2026-09-24,p189,w28,weaver_link
10348,2026-07-25,p106,w3,shop_search
10349,2026-08-26,p113,w16,weaver_link
10350,2026-09-27,p120,w29,weaver_link
10351,2026-07-01,p127,w4,newsletter
10352,2026-08-02,p134,w17,weaver_link
10353,2026-09-03,p141,w30,weaver_link
10354,2026-07-04,p148,w5,direct
10355,2026-08-05,p155,w18,weaver_link
10356,2026-09-06,p162,w31,weaver_link
10357,2026-07-07,p169,w6,weaver_link
10358,2026-08-08,p176,w19,weaver_link
10359,2026-09-09,p183,w32,shop_search
10360,2026-07-10,p100,w7,weaver_link
10361,2026-08-11,p107,w20,weaver_link
10362,2026-09-12,p114,w33,direct
10363,2026-07-13,p121,w8,weaver_link
10364,2026-08-14,p128,w21,weaver_link
10365,2026-09-15,p135,w34,weaver_link
10366,2026-07-16,p142,w9,weaver_link
10367,2026-08-17,p149,w22,shop_search
10368,2026-09-18,p156,w35,weaver_link
10369,2026-07-19,p163,w10,weaver_link
10370,2026-08-20,p170,w23,newsletter
10371,2026-09-21,p177,w36,weaver_link
10372,2026-07-22,p184,w11,weaver_link
10373,2026-08-23,p101,w24,weaver_link
10374,2026-09-24,p108,w37,weaver_link
10375,2026-07-25,p115,w12,shop_search
10376,2026-08-26,p122,w25,weaver_link
10377,2026-09-27,p129,w38,weaver_link
10378,2026-07-01,p136,w13,newsletter
10379,2026-08-02,p143,w26,weaver_link
10380,2026-09-03,p150,w1,weaver_link
10381,2026-07-04,p157,w14,direct
10382,2026-08-05,p164,w27,weaver_link
10383,2026-09-06,p171,w2,weaver_link
10384,2026-07-07,p178,w15,weaver_link
10385,2026-08-08,p185,w28,weaver_link
10386,2026-09-09,p102,w3,shop_search
10387,2026-07-10,p109,w16,weaver_link
10388,2026-08-11,p116,w29,weaver_link
10389,2026-09-12,p123,w4,newsletter
10390,2026-07-13,p130,w17,weaver_link
10391,2026-08-14,p137,w30,weaver_link
10392,2026-09-15,p144,w5,weaver_link
10393,2026-07-16,p151,w18,weaver_link
10394,2026-08-17,p158,w31,shop_search
10395,2026-09-18,p165,w6,weaver_link
10396,2026-07-19,p172,w19,weaver_link
10397,2026-08-20,p179,w32,newsletter
10398,2026-09-21,p186,w7,weaver_link
10399,2026-07-22,p103,w20,weaver_link
10400,2026-08-23,p110,w33,weaver_link
EOF
cat > data/README.md <<'EOF'
`sales-2026-q3.csv` is last quarter's sales export. `arrived_from` is where the buyer came from
just before buying: `weaver_link` is a link a weaver shared (social media, their own site, a
class handout), `shop_search` is the shop's search page, `newsletter` is the shop's email, and
`direct` is a typed address.
EOF
