# Architecture report

Write one static HTML file. Load Tailwind from its CDN and Mermaid 11 as an ESM import
from a CDN, and add no other scripts.

## Layout

The header holds the repo name, the date, and a legend for the diagram marks. It has no
introduction.

Each candidate is one card:

- a short title that names the deepening;
- a badge for strength and a tag for the dependency category;
- the files, in monospace;
- a before-and-after visual in two columns, about 320px tall;
- the problem in one sentence and the solution in one sentence;
- wins as bullets of at most six words;
- a one-line ADR warning when one applies.

End with the top recommendation: the candidate's name, one sentence on why, and a link
to its card.

## Visuals

Pick the visual that fits the relationship, and vary them across candidates:

- a Mermaid flowchart or sequence diagram for calls and dependencies;
- positioned boxes and SVG arrows when Mermaid's layout gets in the way;
- stacked bands for the layers a call passes through;
- two rectangles per module that compare interface size with implementation size;
- a call tree collapsed into one box.

If a visual needs a paragraph to explain it, redraw the visual.

## Style

Use stone and slate with generous whitespace, one accent of emerald or indigo, red for
leakage, and amber for warnings. The page should look like an editorial layout and not a
dashboard.

## Wording

Use only these terms: module, interface, implementation, depth, deep, shallow, seam,
adapter, leverage, locality. Do not write component, service, unit, API, signature,
boundary, layer, or wrapper. State each win in those terms, such as "bugs concentrate in
one module", and never as "easier to maintain" or "cleaner code". Write no introduction,
hedging, or explanatory paragraphs.
