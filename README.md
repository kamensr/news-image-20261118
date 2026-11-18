# News Image — 18 November 2026

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/kamensr/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/kamensr/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

One image summing up the world's news of Wednesday 18 November 2026, built
for the make.fun `news-image-20261118` competition.

## The image

`entry.png` (1024×1024, 129,444 bytes) is a news poster with four of the
day's top stories, each with its own illustration, a kicker, a short headline
and a one-line sub-caption:

1. **Middle East** — U.S. jets strike Iran's Qeshm Island; Iran hits back at
   Kuwait and Bahrain.
2. **Europe** — the Kerch Bridge to Crimea partly collapses after a Ukrainian
   strike.
3. **Asia-Pacific** — Xi greets Trump in Shenzhen ahead of Thursday's
   three-way talks with Putin.
4. **Americas** — Mary Peltola wins Alaska's Senate seat; Democrats take the
   Senate 56–44.

The poster was drawn with Python PIL: every illustration is flat vector art
and every word is real text drawn by the program, so nothing is garbled.
The stories are as reported on 18 November 2026 by Reuters, AP, AFP,
Al Jazeera and the Wall Street Journal.

## How it runs

`main.py` (Python 3.13, standard library only) copies `entry.png` to
`/output/entry.png`. It runs with no network and writes the same bytes on
every run. Local test:

```
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see [LICENSE](LICENSE).
