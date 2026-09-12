# Listing texts

    description-en.txt               Steam Workshop, BBCode
    description-ru.txt               Steam Workshop, BBCode
    description-paradoxmods-en.txt   Paradox Mods, plain text
    description-paradoxmods-ru.txt   Paradox Mods, plain text
    short-description-en.txt         one-paragraph summary
    short-description-ru.txt         one-paragraph summary

The Paradox Mods files are **generated** from the Steam ones by
`tools/bbcode_to_plain.py`; edit the BBCode version and re-run it rather than
editing them directly, or the two will drift apart.

The preview image is `thumbnail.png` in the repository root, built by
`tools/make_thumbnail.py`. It is 1280x1280 and around 40 KB, well under the
Workshop's 1 MB limit. The same script writes `thumbnail-200px.png`, which
exists only to check that the image still reads at the size Steam actually
renders previews at in listings - that constraint is why the image is two
words and one chart rather than anything detailed.

Both bar groups in the chart are the real numbers: 12 systems on zoom step 9
in vanilla, and 1/1/3/4/2/1 across steps 7..12 with the mod.
