# Validated human-style evidence

Read this reference only when a user supplies detector screenshots, ratios,
segment labels or a draft they explicitly confirm passed.

Detector feedback is evidence about one text, detector version and run. Use it
to compare writing decisions inside that sample. Do not turn it into a promise
of permanent detector performance.

## Evidence handling

Record four things before revising:

1. the exact draft or hash that was tested
2. the reported aggregate result, without inventing missing percentages
3. the exact paragraph range marked stronger or weaker
4. whether the result came from a local API response, screenshot or user report

Preserve a user-confirmed stronger passage verbatim by default. Change it only
for factual accuracy, protected literals or an explicit user request.

## Observed WorkBuddy case

This case produced a useful multi-round comparison in September 2026. It is a
case study, not a universal formula.

| Round | Measured or reported result | Main writing behavior |
| --- | --- | --- |
| v1 | Screenshot showed 100% AI features | Abstract framework, evenly structured headings, repeated summaries and several checklist-like conclusions. |
| v2 | Screenshot showed 0% human, 57.69% suspected AI and 42.31% AI | Added conversational phrases, but kept the same lesson-first structure and symmetrical advice. Surface tone changed more than paragraph function. |
| v3 | Screenshot showed 15.62% human, 84.38% suspected AI and 0% AI | One concrete correction passage performed better; surrounding installation, explanation and troubleshooting remained broad. |
| v4 | Screenshot showed 44.58% human, 55.42% suspected AI and 0% AI | The opening through the first task prompt performed better. It used a narrow task, raw material, exact input and a real distinction between audiences. Later prose returned to meta-explanation and exhaustive coverage. |
| v5 | User explicitly confirmed that the article passed Zhuque; exact ratios were not recorded | Preserved the confirmed opening, then used a plausible wrong output, factual correction, saved artifact and final file check. It removed most explanation-of-explanation and stopped on a concrete action. |

## What worked in the confirmed passage

### Title and opening

The title names a moment and an action: the product has just been installed and
the reader needs a first sentence. It avoids promising mastery, speed or a
complete transformation.

The opening starts with that sentence, then immediately tests its missing
information. This creates a small problem the reader can see before the article
offers advice. When adapting this move, use a request that belongs to the real
task. Do not invent a dramatic mistake only to make the opening stronger.

### Content logic

The article follows one small task from start to finish:

1. begin with words the reader might actually type
2. expose the missing information in that request
3. define one narrow deliverable
4. give the minimum verified setup needed to start
5. provide raw, imperfect source material
6. state audience, length and factual boundaries
7. show a plausible output that changes the facts
8. correct the exact claims that drifted
9. save the accepted result as a named artifact
10. inspect the artifact rather than trusting the chat transcript

Each paragraph changes the state of the task. The prose rarely pauses to
announce a lesson.

### Material selection

The source material contains ordinary unfinished states: a colleague has not
replied, customer questions were collected but not resolved, and a proposal is
only an outline. These details make factual checking possible. They also keep
the article from converting every action into an achievement.

Do not manufacture such details. Use user-provided material, a clearly labeled
fictional exercise, or verified source evidence.

### Tutorial path

The tutorial keeps one stateful path: install, provide notes, constrain the
request, inspect a flawed answer, correct it, save a file and inspect the saved
file. It does not branch into every available feature. A beginner always knows
what object is currently being handled and what to do next.

This narrow path also gives explanations a reason to exist. Markdown is
explained only when the reader is asked to save a `.md` file. The results panel
is named only when the file should appear there. Product concepts arrive at the
step where they are needed.

### Example design

The example has three layers that remain visible throughout:

1. raw notes with mixed completion states
2. a request that defines audience, format, length and factual limits
3. a plausible output that silently overstates those notes

The correction quotes the precise mismatch and supplies the true state. This
makes the example do the teaching. It is stronger than following the example
with a paragraph that restates a general prompt-writing principle.

The flawed output is plausible rather than absurd. Words such as “已完成”,
“解决了” and “顺利推进” are easy to accept during a quick read, which gives the
reader a useful checking habit.

### Paragraph function

Successful paragraphs mainly do one of these jobs:

- present an input the reader can use
- point to a visible mismatch
- correct one fact
- move to the next operation
- verify a saved result

Riskier paragraphs tended to explain why the previous example was good, repeat
the lesson, list unrelated edge cases or end with a broad claim about AI.

### Sentence rhythm

The passed draft varies sentence length because actions require different
amounts of explanation. Short lines appear at real turns in the task. Longer
sentences carry setup or factual contrast. Rhythm was not created by random
splitting, fragments or deliberate mistakes.

### Voice

The useful tone is direct and ordinary: “没整理过也没关系”, “别替我加业绩”,
or “先发一次看看”. These phrases remain attached to a concrete action. Casual
wording alone did not improve earlier drafts when the structure stayed
formulaic.

The article addresses the reader at the exact moment an action is needed. It
does not maintain a chatty tone in every sentence. Direct instructions,
observations and short explanations alternate according to the task.

### Transitions and layout

Transitions are operational: “现在到输入框里”, “接着”, “先发一次看看”,
“改完以后” and “文件出现以后”. Each one changes the task state. Avoid adding
transitions whose only purpose is to make the article sound organized.

Quoted blocks separate copyable input from explanation. Links sit beside the
installation or results-panel claim they support. Short paragraphs reduce the
chance that an instruction, reason and warning blur together.

### Factual boundaries

The article labels its work record as fictional, points product-specific claims
to official pages and refuses to supply an unknown reason for delay. It also
distinguishes collection from resolution, waiting from confirmation, and an
outline from a completed plan.

These distinctions contribute to both trust and voice. Human-sounding prose is
not a substitute for source discipline. Preserve uncertain states instead of
turning every step into a success story.

### Reader value

The reader leaves with four reusable objects: sample raw notes, a constrained
request, a factual correction and a saved-file instruction. Advice is attached
to something that can be copied, inspected or changed.

### Ending

The passed version stops after a practical next use. It does not repeat the
opening, declare that the reader has mastered the product or turn the exercise
into a general philosophy.

The final paragraph extends the same workflow to next week and to a company
template. It adds one realistic variation, then stops. It does not introduce a
new feature list near the end.

## What did not work in earlier rounds

- Changing “formal” words into casual words while keeping a lesson-first,
  evenly balanced structure.
- Adding rhetorical questions in repeated groups. The questions signalled a
  planned teaching pattern without advancing the task.
- Explaining why an example was natural immediately after the example had
  already made the point.
- Covering installation, Skills, prompts, files, troubleshooting and advanced
  usage as equally sized sections. Breadth weakened the single beginner path.
- Ending each section with a takeaway and ending the article with another
  summary. The conclusion had already been reached several times.
- Using vague success phrases where the source described waiting, partial work
  or an unknown cause.

## Transfer checklist

Use this checklist when applying the case to another AI-tech tutorial:

- Does the title name the reader's current situation and first useful action?
- Does the opening reveal a concrete missing input, risk or mismatch?
- Is there one deliverable that runs through the article?
- Does every product concept appear at the step where the reader needs it?
- Are examples labeled as real, fictional or sourced?
- Does the example contain enough unfinished or uncertain state to support a
  meaningful check?
- Does feedback quote the wrong claim and replace it with the known fact?
- Does each paragraph change the task, inspect a result or protect a fact?
- Are copyable inputs visually separate from commentary?
- Does the workflow end with the actual artifact the reader will use?
- Does the final paragraph stop after one practical extension?

Do not require every article to match every item. Select the items that fit the
article type, evidence and reader task.

## Revision method for new detector evidence

### 1. Build a contrast map

For the stronger and weaker passages, note:

- what concrete object is present
- what the reader can do next
- whether a fact changes during the paragraph
- whether the paragraph demonstrates or explains
- whether the ending advances the task or summarizes it

Use the contrast to choose edits. Do not copy sentence shapes mechanically.

### 2. Preserve the fact spine

List the source facts, technical literals, commands, dates, links and explicit
uncertainties. Run `integrity_check.py` after revision when an original exists.

### 3. Change paragraph function first

Replace weak functions rather than individual words:

- generic benefit -> observable result
- abstract advice -> exact input or comparison
- explanation after example -> next operation
- three parallel questions -> one visible mismatch
- exhaustive troubleshooting -> the failure at the current step
- repeated conclusion -> stop after the artifact is verified

### 4. Keep readable syntax

Do not add typos, random slang, broken grammar or arbitrary sentence fragments.
Readability and factual precision take priority over detector feedback.

### 5. Re-evaluate honestly

Run local lint and integrity checks first. Run Zhuque when configured. If the
user tests externally, ask for the aggregate result and marked segment range.
Report only the measured result for that exact draft.

Stop after three detector-guided rounds by default, or sooner when another
rewrite would damage facts or readability.
