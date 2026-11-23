CORMSIS talk — Quarto / Reveal.js

From this project folder, run:
    quarto preview

This renders the talk, opens it in your browser, and updates the preview
when you save changes. Stop the preview with Ctrl+C.

Edit talk.qmd to change text, LaTeX mathematics, code, or notes.
theme.scss defines the Southampton visual theme, adapted from the linear-solvers talk.
styles.css adapts layouts for this talk. assets/ contains the original figures,
the animated GIF, vector diagrams, Southampton logo, and bundled fonts.

Render:
    quarto render

This produces _output/index.html. Open that file in a browser to present
the rendered talk.

_quarto.yml defines the project and limits rendering to talk.qmd.

Controls: arrow keys to navigate, F for fullscreen, O for overview,
S for speaker view.

The source contains all 68 Keynote slides and two added paper-link slides.
The original 16 skipped slides retain visibility="hidden", so the default
presentation has 54 slides.
Remove that attribute on a slide heading to show a skipped slide.
The slide IDs preserve the original Keynote slide numbers.

Original speaker notes are retained as supplied, including their original
slide associations. Some notes appear to refer to other slides.

Text, equations, and Python code are editable. Complex diagrams are preserved
as SVG graphics; plots and article excerpts use the original image assets.
The multigrid example remains pseudocode and is not executed.
The calibration figure on displayed slide 26 reproduces the original three
click-driven builds with one-second fades and automatic sequencing. The
right-hand statistics appear alongside the corresponding figure builds;
figure labels are enlarged for readability.
Other Keynote build animations and transitions have been flattened.
The original iterative-method GIF remains animated.

The rendered HTML embeds its images, styles, scripts, fonts, and mathematics.
Use the preview command when presenting with the speaker view.
