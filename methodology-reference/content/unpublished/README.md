# Chapters kept out of the published methodology

These historical drafts are not built into the public pages. The current short operating guide is `content/system-setup.md`; do not use these drafts as execution instructions. They describe how the evidence base is operated, which a reader of the method does not need. They were removed after the first review round to shorten the published text.

| File | What it covers |
|---|---|
| `continue-with-ai.md` | Setting up and running the AI-plus-human system that extends the evidence base. |
| `rulesets-and-learning.md` | How the extraction and search instructions are versioned, and the review loop after each sweep. |

To publish one again: move it back to `content/`, add its slug to `EVIDENCE_CH` in `build/chapters.py` and to the slug list in `content/CONTRACT.md`, and run the build. The build does not read this folder, so text here is not checked and may fall behind the repositories it describes.
