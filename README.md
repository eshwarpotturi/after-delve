# After Delve

A data story on the words that spread through research abstracts after ChatGPT, and how that vocabulary keeps changing.

- **Tech** (`index.html`): 736,000 computer-science and electrical-engineering abstracts on arXiv, January 2019 to September 2026. Three sets of marker words peak in turn, in 2024, 2025 and 2026.
- **Biomedical** (`biomedical/index.html`): 10.4 million PubMed abstracts via Europe PMC, with views by country, publisher and journal.

Both pages are self-contained HTML, so GitHub Pages serves them as they are.

## Data and scripts

- `data/tech/` holds the counts behind the tech page and the scripts that read the arXiv metadata snapshot, picked the words and ran the pre-ChatGPT placebo test.
- `data/biomedical/` holds the counts behind the biomedical page and the scripts that sampled abstracts and pulled counts from Europe PMC.

Sources: [arXiv metadata snapshot](https://huggingface.co/datasets/librarian-bots/arxiv-metadata-snapshot) (28 September 2026), [Europe PMC](https://europepmc.org/), [Crossref](https://www.crossref.org/). The method follows Kobak et al., [Delving into ChatGPT usage in academic writing through excess vocabulary](https://arxiv.org/abs/2406.07016).

A marker word shows wording that became common after AI writing tools spread. It is not evidence of misconduct.

A personal demo. Not an official product of any organisation.
