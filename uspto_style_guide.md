# USPTO Patent Application Style Guide & Formatting Requirements

This comprehensive style guide outlines structural, textual, and visual rules required for formal compliance with United States Patent and Trademark Office (USPTO) filing standards. Adhering to these mechanics ensures clean electronic capture, passes administrative reviews, and prevents formal formatting rejections.

---

## 1. Document Text & Layout Standards

The written specification narrative must be completely pristine, readable, and structured to support direct digital reproduction.

* **Format Options:** Native `.docx` is preferred for nonprovisional applications to avoid surcharges. The `pandoc` pipeline generates both `.pdf` and `.docx` using `.tex` as a template applied to `.md` sources.
* **Margins:** Every sheet of the specification, abstracts, and claims must maintain strict **1-inch (2.54 cm)** margins on the top, bottom, left, and right (or `left=1in, top=0.75in, bottom=0.75in, right=0.75in` via standard LaTeX geometry).
* **Line Spacing:** All specification text blocks must be strictly **1.5 or double-spaced**. Single spacing is a critical non-compliance error.
* **Font and Typography:** Use 12pt, standard fonts (like Times New Roman).
* **Section Headings:** Section headings must be unnumbered and UPPERCASE. Unused declaratory sections (e.g., Federally Sponsored Research, Joint Research Agreements) must be marked "Not Applicable."
* **Drafting Marks and Artifacts:** The final document must be entirely free of word-processor drafting indicators, alterations, or markup.

> **Programmatic Tip (DOCX Ingestion):** To guarantee technical terms or unconventional technical words (e.g., *WDM*, *vortices*, *Fermion*) don't pollute final application exports with red or blue spell-check lines, inject the following OpenXML settings directly into the document structure:
> * `<w:hideSpellingErrors/>`
> * `<w:hideGrammaticalErrors/>`

---

## 2. Structure & Segregation of Drawings

The written narrative and the visual sheets are treated as separate physical entities by the USPTO.

* **Complete Isolation:** Visual diagrams, block architectures, or flowcharts (**FIG. 1, FIG. 2**, etc.) must **never be embedded inline** within the specification text.
* **Dedicated Layout:** All figures must be grouped on their own dedicated, blank sheets of paper positioned at the very end of the application packet, completely segregated from the text.
* **Page Separation:** Every distinct figure page should be isolated from the prior block using an explicit `\newpage` or openxml page-break macro to guarantee the rendering pipeline splits the canvas cleanly.
* **Abstract:** The `ABSTRACT OF THE DISCLOSURE` must sit on its own separate page, placed immediately after the claims and before the `\section*{Drawings}` section. It must be strictly under 150 words in a single paragraph.

---

## 3. Drawing Sheet Rules & Annotations

Annotations within the visual drawing sheets follow a completely reversed set of enclosure rules compared to the text body.

* **Visual Style:** Use black ink on white paper with no color, shading, or grayscale. Solid, dashed, or broken lines only.
* **Bare Reference Numerals:** All reference numbers placed inside shape matrices, blocks, or line pointers **must be completely bare** (e.g., render as `104`, `105`, `201`).
* **No Outlines or Enclosures:** On the drawing sheets themselves, reference characters must *never* be enclosed inside parentheses, brackets, outlines, or inverted commas.
* **Structural Hardware vs Abstract:** Under 37 CFR 1.83, physical hardware claims must be depicted using structural schematics, cross-sections, or isometric views showing every specified feature. Abstract logical flows (data flows, algorithms) may remain as block diagrams.

> **The Exception Rule:** Parentheses are strictly reserved for text callouts inside the written *Claims* narrative when referencing structural parts; they are illegal on the actual diagram canvas.

* **Text inside Drawings:** Flow sheets and block diagrams are permitted to contain a few short, descriptive catchwords indispensable for basic system understanding (e.g., `"NIR Pump"`, `"Log Detector"`, `"Resin Matrix"`), but any associated reference numbers must also remain bare.

---

## 4. List Architecture & Indentation

Standard automated graphical bullet formats are heavily penalized or completely blocked during ingestion due to translation errors.

### In the Detailed Description

* **Discouraged Formats:** Graphical bullet points (such as `•`, `*`, or custom dashes) are highly discouraged. They frequently trip parsing scripts or cause character corruption in the USPTO electronic database.
* **Compliant Fallback:** Replace all bullet lists with standard lowercase alphanumeric listings enclosed in parentheses.
* *Example format:* `(a) Optical Mode`, `(b) RF Tomography Mode`.

### In the Claim Listing

* **Banned Formats:** Automated bullet loops and itemization structures are completely banned in the claims section.
* **Compliant Indentation:** Pluralities of elements, steps, or multi-part dependencies must be separated using a standard line break combined with a manual **tab indentation** or a LaTeX `\indent` block, ending with a semicolon. The structure relies entirely on clear hierarchical line blocks to keep elements readable.

---

## 5. Mathematical Formula Formatting

Complex variables and continuous operators should be cleanly separated from regular prose and presented in standalone display mathematical blocks using correct symbolic notation.

For instance, continuous logic operators or underlying hardware equations must be rendered as clean math blocks:

$$eml(x,y) = \exp(x) - \ln(y)$$

---

## 6. General Drafting Tone & Modularity

When drafting or modifying patent applications, maintain a broad defensive scope.
* **Functional Over Specific:** Define components functionally (e.g., "near-infrared (NIR) light source" operating in the 800nm-1550nm spectrum) rather than limiting to specific embodiments (like 1064nm lasers).
* **Emphasize Modularity:** Explicitly emphasize system modularity to maximize the protective envelope.

---

## 7. Provisional vs. Nonprovisional Ingestion Mechanics

Filing requirements shift drastically depending on which priority target phase you are navigating.

| Requirement | Provisional Phase (OPAP Review) | Nonprovisional Phase (Substantive Exam) |
| --- | --- | --- |
| **Primary Check Focus** | Basic administrative completeness (legibility, fee, cover sheet, reproduction capability). | Full formatting verification under strict **37 CFR 1.84** rules. |
| **Drawing Flexibility** | Exceptional leniency. Embedded figures, informal hand sketches, and drawing numerals inside parentheses are accepted without loss of priority date. | Zero tolerance. Embedded diagrams or enclosed numerals cause immediate structural rejections and require corrected replacement sheets. |
| **Surcharge Penalties** | No format-based surcharge penalties. Documents can be cleanly processed and uploaded in native PDF format. | Imposes steep surcharges (up to $400) if filed via standard PDF instead of native DOCX format. |