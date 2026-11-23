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

The source contains 69 slides, including two paper-link slides.
Thirteen slides have visibility="hidden", so the default presentation has 56 slides.
Remove that attribute on a slide heading to show a skipped slide.
The slide IDs preserve the original Keynote slide numbers.

Some of the inherited speaker notes refer to other slides.

Text, equations, and Python code are editable. Complex diagrams are preserved
as SVG graphics; plots and article excerpts use the original image assets.
The multigrid example remains pseudocode and is not executed.
The calibration figure on displayed slide 30 reproduces the original three
click-driven builds with one-second fades and automatic sequencing. The
right-hand statistics appear alongside the corresponding figure builds;
figure labels are enlarged for readability.
Displayed slides 13, 14, 25, 37, 39, 45 and 48 each have a single click-driven
reveal. Transitions between slides are instant.
The opening movie on slide 3 stops after two Gauss–Seidel steps. Advance once
to reveal the exact solution. Regenerate the movie and matching still with
`python3 scripts/plot_stopped_solve.py` (NumPy, Matplotlib, LaTeX with dvipng, and FFmpeg).
To regenerate the three-method animation on displayed slide 18, run
`python3 scripts/plot_affine_iterations.py` with NumPy, Matplotlib and Pillow
installed, then render the talk.

The rendered HTML embeds its images, styles, scripts, fonts, and mathematics.
Use the preview command when presenting with the speaker view.

Website deployment

The Deploy compiled talk to personal website workflow publishes the standalone
index.html to talks/osaka_talk_2026/ on the github.io branch of
jcockayne/jcockayne.github.io. It runs on main when the talk or its build files
change, and can also be run manually from GitHub Actions.

The workflow uses the WEBSITE_DEPLOY_KEY repository secret. Its public key is
registered with write access as a deploy key on jcockayne/jcockayne.github.io.
The /talks/ listing is maintained in talks/index.html in the website repository.

To prepare a deployment locally, use Quarto 1.10.18, Python 3.9+ and a checkout
of the website's github.io branch. Replace WEBSITE_CHECKOUT with its path:

    python3 scripts/build_website_talk.py --website-dir WEBSITE_CHECKOUT

This renders in a temporary folder, checks that resources are embedded, and
writes only talks/osaka_talk_2026/index.html in the website checkout.
