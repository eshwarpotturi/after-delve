# After Delve

A data story on the words that spread through research abstracts after ChatGPT, and how that vocabulary keeps changing.

- **Tech** (`index.html`): 736,000 computer-science and electrical-engineering abstracts on arXiv, January 2019 to September 2026. Three sets of marker words peak in turn, in 2024, 2025 and 2026.
- **Biomedical** (`biomedical/index.html`): 10.4 million PubMed abstracts via Europe PMC, with views by country, publisher and journal.

Both pages are self-contained HTML with their data embedded, so GitHub Pages serves them as they are (`.nojekyll` is included). To view locally, open either file in a browser. There is nothing to build or install.

## Repository layout

```
index.html              Tech page
biomedical/index.html   Biomedical page
data/tech/              arXiv pipeline: scripts, word families, monthly counts
data/biomedical/        Europe PMC pipeline: scripts and monthly counts
```

## Data and scripts

The scripts are plain Python that read and write files in the current directory, so run them from inside their own folder. They are a record of how the numbers were produced. They are not packaged and do not run end to end without the raw inputs, which are not committed (see below).

### `data/tech/`

Outputs committed: `counts.json` (monthly totals, per-word counts and wave groupings behind the page) and `families.json` (inflected forms merged into one family, such as delve/delves).

Pipeline, in order:

1. `pass1.py` reads the arXiv metadata parquet files (`pq/*.parquet`) with DuckDB and builds document-frequency counts by subject group and year.
2. `pass2.py` picks candidate marker words that rose sharply in 2024 to 2026 against 2021 to 2022, adds a hand-picked list and control words such as "however", and stores per-document word sets.
3. `select.py` compares tech with other fields to choose the final words.
4. `placebo.py` runs the same test on pre-ChatGPT years (2019, 2022, 2025 against each other) to show how many words rise by chance.
5. `forms.py` and `families.py` group inflected forms into families.
6. `agg.py` aggregates monthly counts for the three word waves (`agg.json`).
7. `prep.py` smooths the rates, sets the pre-2023 baseline and writes `page_data.json` for the page.

### `data/biomedical/`

Outputs committed: `counts.json` (monthly and yearly counts by word, country, publisher and journal).

Pipeline, in order:

1. `sample.py` downloads a sample of abstracts from the Europe PMC REST API (one day a month for 2021, 2022, 2024 and 2025) into `sample/`.
2. `discover.py` finds words whose use rose after 2022 in that sample.
3. `pull.py` queries Europe PMC for hit counts by word, month, year, country and journal and caches them in `cache.json`. It also writes `config.json`.
4. `crossref.py` looks up each top journal's publisher through the Crossref API (`publishers.json`).
5. `build.py` assembles the counts into `data.json`.
6. `prep.py` smooths the series, computes baselines and peaks, and prepares the page data.

### Requirements

Python 3 with `duckdb` for the tech scripts. The biomedical scripts use only the standard library. Both need network access to fetch their sources.

## Sources

- [arXiv metadata snapshot](https://huggingface.co/datasets/librarian-bots/arxiv-metadata-snapshot) (28 September 2026)
- [Europe PMC](https://europepmc.org/)
- [Crossref](https://www.crossref.org/)

The method follows Kobak et al., [Delving into ChatGPT usage in academic writing through excess vocabulary](https://arxiv.org/abs/2406.07016).

## Notes

A marker word shows wording that became common after AI writing tools spread. It is not evidence of misconduct.

A personal demo. Not an official product of any organisation.
