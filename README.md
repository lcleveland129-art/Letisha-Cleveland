# Joesiah & Malani: Noah's Bloodline (Book 1)

By LeTisha C. Cleveland. This is the Amazon KDP paperback production files: 8.5 × 11 in, premium color, white paper, with bleed.

## Deliverables (`deliverables/`)

| # | File | What it is |
|---|------|-----------|
| 1 | `01_KDP_Interior_Joesiah_Malani_Book1.pdf` | **Upload this to KDP** as the paperback interior (31 pages, 8.625 × 11.25 in with bleed, all fonts embedded) |
| 1b | `01b_KDP_Interior_Joesiah_Malani_Book1_SMALL.pdf` | Same interior, smaller file (18 MB; pictures more compressed, still 300 DPI). Good for sharing and previewing; also KDP-compliant. |
| 2 | `02_Editable_Manuscript_Joesiah_Malani_Book1.docx` | Editable manuscript in the same page order. Fonts: Literata and Cinzel (free; in `tools/fonts/`). |
| 3 | `03_QC_Report.md` / `.docx` | Page-by-page quality-control report: what was wrong, what was corrected, and the KDP checks |
| 4 | `04_Open_Issues_For_Approval.md` / `.docx` | Decisions and replacement artwork still needed from the author |
| 5 | `05_KDP_Cover_Joesiah_Malani_Book1.pdf` | **Upload this to KDP** as the full-wrap cover (17.325 × 11.25 in, for 32 pages, white paper, premium color) |

## Other folders

- `artwork/corrected/` – the 13 illustrations after frame removal, chapter and page-number relettering, and enlargement to 302 DPI (`ill-00` … `ill-12`).
- `source/` – the original uploaded interior and cover PDFs, unchanged.
- `tools/` – scripts that rebuild everything from `tools/content.py`, which holds the edited manuscript text:

```bash
python3 tools/process_images.py <folder with extracted img-000.jpg…> artwork/corrected tools/fonts
python3 tools/build_interior.py tools tools/fonts artwork/corrected deliverables/01_KDP_Interior_Joesiah_Malani_Book1.pdf
python3 tools/build_cover.py <back.jpg> <front.jpg> tools/fonts <outdir> 32   # images: pdfimages -j source/original_JOESIAH_MALANI_COVER_UPLOAD_DRAFT.pdf cimg
python3 tools/build_docx.py tools artwork/corrected deliverables/02_Editable_Manuscript_Joesiah_Malani_Book1.docx
```
(The original illustrations are extracted from the source PDF with `pdfimages -j source/original_Joesiah_Malani_Final.pdf img`.)
