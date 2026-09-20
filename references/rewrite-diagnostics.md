# Rewrite diagnostics

Map signals to writing problems before editing.

## Uniform sentence rhythm

Possible issue: multiple sentences have the same grammatical function and length.

Good moves:
- remove a redundant sentence
- convert one sentence into a concrete example
- combine cause + consequence where natural

Bad move: randomly split sentences to manufacture variance.

## Formulaic transitions

Possible issue: logic is announced rather than demonstrated.

Good moves:
- delete the transition if sequence is obvious
- replace it with the actual causal relationship

## Abstract density

Possible issue: many claims use words like “提升、赋能、效率、体验、能力、价值” without observable behavior.

Good move: describe what the user can now do, how long it took, what changed, or what failed.

## Repeated conclusion

Possible issue: paragraph says the same thing as its first sentence.

Good move: cut the final summary or replace it with a consequence.

## Detector-risk segment with heavy technical literals

Do not distort code/API text. Rewrite surrounding explanation first. If the technical material itself is flagged, preserve it and document the constraint.

## Example followed by explanation of the example

Possible issue: the prose gives a useful example, then repeats its meaning in a
teacherly paragraph.

Good moves:
- let the example stand when the reader can infer the point
- move directly to the next action or decision
- explain only the ambiguity that could cause a real mistake

## Exhaustive tutorial coverage

Possible issue: one section tries to anticipate every failure, which turns a
small task into a checklist.

Good moves:
- keep the failure that naturally occurs at the current step
- solve that failure before introducing another
- defer unrelated features until the reader reaches them

## Symmetrical rhetorical questions

Possible issue: three or more questions repeat the same grammar and feel
constructed.

Good moves:
- replace the set with one concrete discrepancy
- show the incorrect output and ask the reader to compare it with the source
