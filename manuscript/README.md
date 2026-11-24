# The Finance Blue Book

Editing manuscript for a trade book, not for self-publishing.

**Title.** The Finance Blue Book

**Subtitle.** What the MBA finance course teaches, and what the case leaves out

**Author.** Ashok Paudel

The cases are original. They use the classroom form of an MBA finance course (a firm, a decision, exhibits, a question you answer before the explanation). They are not Harvard Business School cases and not ESMT Berlin cases.

Every euro is produced by `ledger/ledger.py`. If the prose and the ledger disagree, the ledger wins.

## Read it in this order

1. `00_front_matter.md`
2. `01_a_later_euro.md` through `12_a_priced_choice.md`
3. `13_blue_pages.md`
4. `14_sources_and_notes.md`
5. `15_one_hour.md` last, with the folder shut

## Check the figures

```bash
python3 ledger/ledger.py
python3 ledger/check_manuscript.py
```
