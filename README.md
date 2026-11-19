# News Image — 18 November 2026 (v2)

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/kamensr/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/kamensr/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

One image summing up the world's news of Wednesday 18 November 2026, built
for the make.fun `news-image-20261118` competition. This is the v2 entry: a
dense winner-format poster with **49 verified stories across 7 regions**,
replacing the 4-story v1.

## The image

`entry.png` (1024×1024) is a broadsheet-style poster, drawn entirely with
Python PIL — flat vector illustrations and real text, no AI photos, so
nothing is garbled:

- **Kicker + masthead** — "Wednesday 18 November 2026 · 49 stories ·
  7 regions · every one from this Wednesday".
- **UTC timeline** — 10 dated moments from 00:48 (Romania quake) to 20:48
  (Carney meets Trump).
- **4 feature stories** (1–4), each with a flat illustration, region/beat
  tags, a CLAIM/CONFIRMED label and a source tag:
  1. U.S. jets strike Iran's Qeshm Island; Iran hits back at Kuwait and
     Bahrain (includes Iran's MQ-9 downing claim, labelled CLAIM).
  2. Kerch Bridge hit again — the third strike in three days.
  3. Xi greets Trump in Shenzhen; the first-ever Trump–Xi–Putin summit is
     set for Thursday.
  4. Israeli tanks cross the Yellow Line in central Gaza.
- **12 mini stories** (5–16) with small flat icons: Peltola wins Alaska;
  Hegseth's surprise Caracas deal; Brazil's fiscal package; Carney–Trump
  (no deal); U.S. pending home sales at a record low; Voyager 1 passes one
  light-day; OpenAI launches GPT-6.2 Astra and Sol; Ebola tops 5,600 dead
  in DR Congo; Fiji's drought disaster; drone strikes on Odesa; markets
  (S&P down a fifth straight day); COP31 crunch time.
- **World map** with 12 numbered pins matching story numbers.
- **"Also on Wednesday 18 November"** — 33 numbered one-liners (17–49):
  Anthropic's $83 IPO pricing, the EU's €45bn Ukraine loan, UK inflation
  at 3.6%, quakes in Romania/Peru/Flores/PNG, Cyclone Akvan, Florida and
  Malaysia floods, the Earthshot Prizes in Mumbai, the MT TARA GAS strike,
  Microsoft's seven in-house models, Nvidia's fall, Fed's Waller on a
  half-point hike, Ethiopia–Eritrea tensions, the Manila child-protection
  conference, Canary Islands arrivals, UWCL and CONCACAF results, and more.
- **DATE CHECK** — big stories deliberately left out because they broke
  before the 18th (measles status loss, Russian jets over Japan, the An-12
  crash, the Prague train collision, the WHO Gaza flood warning, the Rugby
  League World Cup final).

Every story was verified against reporting dated 18 November 2026
(Reuters, AP, AFP, Al Jazeera, BBC, NAR, NASA, USGS, IMD, NWS, CDC, WHO,
ONS, FT, Euronews, ANI, RNZ Pacific). One-sided accounts are labelled
CLAIM; everything else is CONFIRMED by the cited source.

## How it runs

`main.py` (Python 3.13, standard library only) copies `entry.png` to
`/output/entry.png`. It runs with no network and writes the same bytes on
every run. Local test:

```
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`generate.py` is the PIL script that drew `entry.png` (run it with
`python3 generate.py` to reproduce the poster; it needs Pillow and the
DejaVu/Liberation fonts).

## License

MIT — see [LICENSE](LICENSE).
