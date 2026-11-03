# Style Guide

This is the living style guide for the book. It keeps formatting and usage stable across
chapters, because drift is easy. Add to it freely. Anything general that is not covered here
gets flagged as a question rather than guessed at.

These are defaults, not absolutes. The author may approve an exception to any rule when it
reads better; once approved, that instance is settled and is not flagged again in later reviews.

The review skills check the manuscript against this file. Every style rule lives here, not in
the skills, so changing a rule means changing it in one place.

Sections marked *(optional)* apply only when the book has that feature. Delete what does not
apply, and replace every example with one from the book.

---

## Base style

- **Reference manual:** Chicago Manual of Style. Where this guide is silent, Chicago decides.
- **Spelling:** American English.
- **Latin abbreviations:** none in the manuscript. Use "and so on," "for example," "that is,"
  and "namely" instead of etc., e.g., i.e., and viz.
- **Inclusive language:** no content that disparages any group.
- **Scope:** these rules govern the manuscript and its deliverables. Working support files
  (tracking files, notes, review skills) are exempt.
- **Tracking files refer to chapters by number only** ("Chapter 4"), never by title, so a retitled
  chapter never forces edits across the support files.

## Audience and voice

- **Core reader:** [describe the reader the book is written for, for example "the mid-level
  engineer working toward senior"]. The main "you" always means this reader.
- **Secondary readers:** [for example, managers or experienced practitioners]. They are reached
  through callouts, never by bending the main "you."
- **Person:** the body addresses the reader as "you." "We" suits summaries and walkthroughs
  where the author and reader move through material together; "you" suits direct instruction.
  First person ("I") is for the author's own stories.
- **Shifts in person:** a personal story in first person is fine. An instruction that slides
  from "you" to "engineers" (or any third-person group) mid-paragraph is not.
- **Callouts:** [format for secondary-audience callouts].

## Acronyms and defined terms

- **First use in the book:** spell out the term with the acronym in parentheses, once, at its
  first appearance anywhere in the book. After that, the acronym stands alone in every chapter.
- **Casing of the spelled-out form:** lowercase for generic terms, capitalized only for proper
  names (role-based access control (RBAC), but Health Insurance Portability and Accountability
  Act (HIPAA)).
- **No expansion needed:** acronyms common enough that readers know them (for example AI).
  List the book's exemptions here: [list].
- **Not first use:** front-of-chapter learning lists, quoted material, and the glossary. An
  acronym may appear bare there; the spelled-out first use belongs in the body.
- **Defined terms:** bold the term on the sentence that defines it, and only there. Later
  mentions stay roman. A term defined in more than one chapter keeps its bold only at its first
  definition in the book.
- **Bold, never quotation marks:** write **cost of labor**, not "cost of labor." Quotation
  marks are for quoted speech.
- **Glossary entries** *(optional)*: lead with the acronym and put the expansion in parentheses:
  RBAC (role-based access control). Headwords are capitalized only when the term is capitalized
  in running text. Each entry carries a tag for the chapter where the term first appears in the
  teaching content: `[First use: Ch. N]`. A passing mention does not count.

## Capitalization

- **Role and job titles:** capitalize when they name the role (Designer, Backend Engineer).
  Lowercase the work itself (design, backend development).
- **Levels and ranks:** capitalize as part of a full title ("promoted to Senior Software
  Engineer," "Senior Engineers are proactive"). Lowercase everywhere else: the level alone, as a
  modifier, or in a compound ("promoted to senior," "the senior role," "senior-level skills").
- **Leave alone:** quotes, headings, table labels, worksheet names, and captions as written.
- **Brand, company, and product names:** roman, never italic. Follow the company's own
  capitalization where it is a normal word, but do not reproduce all-caps styling unless the
  name is an acronym. No trademark or registered symbols in running text.
- **Titles of works:** italic (books, films, TV series, podcasts, albums, and websites that are
  publications rather than companies).

## Word list

House spellings and forms. Add to this list as decisions are made.

| Use | Not | Note |
|---|---|---|
| [codebase] | [code base] | |
| [one-on-one] | [1:1] | |
| [versus] | [vs., vs] | in prose and headings |
| ["and" in headings] | ["&"] | "&" only in proper names that include it |

- **Hyphenation:** hyphenate a compound modifier before a noun (open-source project); leave it
  open as a noun (contribute to open source).
- **Fixed forms:** where a term has several parts of speech, list each form and where it goes,
  and do not introduce a new form. [Example: production readiness (noun), production-readiness
  (modifier), production-ready (adjective), productionize (verb).]
- **Do not vary a term for variety.** If the same thing is meant, use the same word.
- **Never change a form inside a verbatim quotation.**

## Punctuation

- **Em dashes:** do not use them. Recast with a period, colon, semicolon, or parentheses. En
  dashes stay correct for number and date ranges, and hyphens stay correct in compound
  modifiers.
- **Colons and semicolons** are not em dash replacements in every sentence. A paragraph where
  most sentences are split by one reads like the same rhythm in disguise.
- **Slashes** (Chicago 6.106): no space between single words (Impact/Effort, and/or). A space on
  each side when either side is an open compound (High Impact / Low Effort). Never lopsided
  spacing. A division slash in a formula, URLs, and file paths are exempt. Style the same term
  the same way everywhere, including tables, headings, and captions.

## Numbers

- **Prose:** spell out whole numbers from zero through one hundred, and round multiples of
  hundred, thousand, and so on. Use numerals for exact numbers above one hundred.
- **Data:** always numerals for percentages, money, and measurements (18%, $10,000, 100 miles).
- **Approximation:** "~" is acceptable shorthand for "about" in prose, tables, and worksheets.
  Be consistent within a section.
- **References:** chapters, tables, and figures always use numerals (Chapter 4, Table 1.1).
- **Time of day:** [house choice, for example 24-hour clock with a time zone, except idiomatic
  times such as "a 3 AM page"].
- **Casing in shorthand:** "OK," not "ok"; consistent case in units and shorthand ("5K," not
  "5k").

## Lists

- **Numbered lists** are for sequences: steps in order, ranked items, and anything the text
  refers back to by number. **Bulleted lists** are for sets where order does not matter.
- Do not number an unordered set to make it look organized.
- Keep each item to about two or three lines. An item that needs a paragraph belongs in prose.
- Bookend every list with body text: a lead-in before, a sentence after. Never open or close a
  section with a bare list.
- Break lists longer than about ten items into labeled groups. Nest one level at most.
- End punctuation: none on fragments, periods on complete sentences, consistent within a list.

## Headings

- **Levels:** the chapter heading uses Title style. Main sections use Heading 1, their
  subsections Heading 2, and so on. The chapter heading and its sections never share a level.
- **One child is not a section:** a heading with subheadings must have more than one. Fold a lone
  subheading into its parent or add a sibling.
- **Capitalization:** Title, Heading 1, and Heading 2 take headline style (capitalize the first
  and last word and every major word, including short verbs such as Is and Be; lowercase
  articles, coordinating conjunctions, prepositions of any length, and "to" in an infinitive;
  capitalize the first word after a colon). Heading 3 and below take sentence case.
- **Phrasal verbs keep the capital:** "Follow Up," "Roll Back."
- **No terminal periods** on headings. Question marks are fine.
- **Fixed section labels** keep their form at any level (see Chapter format).
- **Worksheet headings** *(optional)* that name a user action read as steps and take sentence
  case; headings that name a criterion or category take headline style.

## Chapter format

Fill this in for the book. The review skills check every chapter against it.

- **Chapter title line:** [for example, the chapter number, a space, and the title, in Title
  style: "10 Building the Shelter"].
- **Chapter file name:** [for example, "Chapter N: Title," matching the title text exactly].
- **Chapter start and end markers:** [how the manuscript marks where a chapter begins and ends;
  anything outside them is notes, not manuscript].
- **Sections in order** (mark each required or optional):
  1. [Front-of-chapter learning list, for example "Chapter Skills"]
  2. Chapter body, with worksheets *(optional)* at point of use
  3. Summary
  4. [End-of-chapter elements, for example discussion questions or exercises]
  5. Endnotes
- **Fixed section labels:** [list them exactly, for example Summary, Endnotes]. They carry
  navigation rather than voice, so a reader meets the same word in every chapter.

### Front-of-chapter learning list *(optional)*

- A list of short gerund phrases, one per line, no end punctuation, no "I can" prefix.
- If a phrase needs a comma or a clause, it is too long; tighten it or split it.
- Each phrase names something the chapter actually teaches.
- **Book-level skills summary** *(optional)*: if the book collects every chapter's skills in one
  place (a self-assessment or index), each entry is a two- or three-word title plus a short
  definition completing a silent "I can" (never written), with [four or five] entries per chapter.
  Every copy of the summary is identical.

### Summary

- Heading: "Summary." Not "Wrapping Up," "Key Takeaways," or a variant.
- Required in every chapter.
- Three jobs, in this order: recap what the reader learned, say why it matters to them, and
  introduce the next chapter topic. The handoff is the part most often left out.
- Short: a few paragraphs at most. It restates; it does not teach.
- It is the last prose before the back matter. A worksheet or other element placed after it
  pushes the handoff out of the reader's path.
- The final chapter closes the book instead of introducing a next chapter.

### End-of-chapter elements *(optional)*

Describe each one the book uses: heading, format, and count. For example:

- **Discussion questions:** numbered list, mixed levels (recall, application, and position), a
  few per chapter. Each is answerable from this chapter alone and opens a discussion rather than
  having one correct answer.
- **Practice or interview questions:** numbered list, about six, mixed formats (behavioral,
  situational, direct, and example-based), each with a short follow-up.
- **Answer rubrics:** for each practice question, what the answer must contain, what separates a
  stronger answer from a weaker one, and the most common weak answer. Descriptive, never a
  numeric score.

### Chapter titles

- A title tells the reader what they get, not only the topic.
- It sounds like the book rather than a syllabus, and survives being said out loud.
- It does not collide with a heading inside the same chapter.
- Fixed section labels stay plain; voice belongs in chapter titles.

## References, figures, and tables

- **Chapter references:** "Chapter 4," capital C, numeral.
- **Cross-references to sections:** set the name in quotation marks, not italics: see "Test
  Early and Often" later in this chapter. Every cross-reference names its destination; "later in
  the book" is not a destination.
- **Figures and tables:** numbered chapter.position, each type counted separately (Figure 3.1,
  Figure 3.2, Table 3.1). Numbers restart in each chapter. Every figure and table has a caption,
  and every caption is mentioned in the text.
- **Worksheet images** *(optional)* are not figures and are not counted.
- **Image specifications:** [the publisher's resolution, minimum size, file format, and file
  naming]. Images should be black-and-white safe.
- **Tables** are typeset as tables, not produced as images.

## Citations and endnotes

- **Style:** Chicago notes, as endnotes at the end of each chapter, numbered in reading order
  with plain integers (1, 2, 3), restarting at 1 in each chapter.
- **Completeness:** each note carries every element its source type needs: author, full title
  with subtitle, container, volume and issue where they exist, date, page range for articles, and
  a URL or DOI.
- **Access dates:** every online source carries a full access date ("accessed October 10,
  2026"), placed after the publication date and before the URL or DOI.
- **Superscripts:** at the point of the claim, after closing punctuation ("The claim.1," not
  "The claim1."). Every superscript has exactly one note and every note exactly one superscript.
  When a note is added, removed, or moved, renumber the body to match.
- **Repeated sources:** a source cited again in a later chapter repeats the full citation, worded
  the same way. Within a chapter, use Chicago short forms.
- **Source preference:** primary sources (peer-reviewed studies, original research) over secondary
  ones (reports, summaries, explainers). When a secondary source is the only option, say so in
  the note.
- **Paraphrase:** a sentence that keeps a source's distinctive wording or sentence shape becomes a
  direct quote or is rewritten in the author's own words.
- **URLs:** never inline in body text. A URL that backs a claim goes in the endnote. A resource the
  reader might want to explore goes in Further Reading.

## Further Reading *(optional)*

- Each entry gets one sentence on what the item is, with no commentary.
- Every major topic in a chapter has at least one deeper resource.
- Do not repeat a topic already covered under another chapter.
- Every resource is checked as available (in print, live, or for sale) before it is listed.
- Selection priorities: [the author's priorities, for example authors and hosts from
  underrepresented groups first, with canonical works included when their absence would be
  conspicuous].

## Quotations

- **Published sources:** quoted exactly, attributed, and endnoted. Never change words inside a
  verbatim quotation, hyphenation included.
- **Rendering:** [how quotes are set, for example epigraphs centered and italic, with attribution
  on the line below in italic only, no dash before the name, and any superscript after the name].

### Interview quotes *(optional)*

- **Attribution:** [named, or unattributed epigraphs]. [Whether they carry endnote markers.]
- **Rendering:** [for example italic and centered, with quotes from published sources set bold,
  italic, and centered so a reader can tell the two apart at a glance].
- **Allowed cleanup, and nothing else:** drop filler and repeated words, fix an obvious
  transcription error, fix a verb tense or word form so the sentence reads correctly (no brackets
  needed), add or replace words in [brackets], and cut. Mark a cut inside a sentence with "…". A
  cut that falls after a complete sentence is not marked: end the sentence with a period and start
  the next with a capital. Any other rewording, reordering, or added word is a fidelity problem.
  Prefer the speaker's own sentences to a quote stacked with ellipses.
- **One home per quote:** no interview quote appears in more than one chapter.
- **Sources:** every quote traces to a transcript, or to the author's written notes when there is
  no recording.

## Worked examples, prompts, and AI *(optional)*

- **Worked examples** (sample outputs, templates) are not styled as quotes. Use indented or boxed
  text.
- **Prompts** for an AI tool: [rendering, for example bold, prefixed with "Prompt:"]. A prompt
  assigns the AI a role in the second person ("You are a research assistant"), never the first
  ("I am a contractor").
- **"AI"** in body text means using a large language model unless stated otherwise. Use "LLM" only
  when discussing the technology itself.

## Worksheets *(optional)*

- Designed to be written in directly, with write-in space shown as blank lines.
- If a response needs a different tool or medium, name it.
- Questions are distinct (not bundled), include a "why" follow-up where useful, and follow the order
  of the chapter content they relate to.
- Each worksheet has an accessible, fillable version, and the book says where to find it.

## Running example *(optional)*

- Name: [the book's recurring example]. Always written in full, never abbreviated.
- Details established anywhere in the book become locked canon: names of pages, screens, people,
  roles, data, numbers, and timeline. The canon file is: [file name].
- **People and roles:** [the fixed set of roles, and the words never used for them]. Check both
  directions: a generic word where a role is meant, and a role word where the sentence is about
  something outside the example.
- **Retired names:** [names no longer used, and their replacements].

## Tools and products *(optional)*

- A named commercial tool gets a three-to-five-word gloss on first mention in the book, and nothing
  else: no endnote, no glossary entry, no URL ("using Playwright, a browser automation tool").
- Vendor-neutral standards with stable documentation get an endnote and, where the reader needs to
  carry the term, a glossary entry.
- Never give a version number; it dates the printing.
- In an appendix, describe the problem a tool solves, not its category. A reader with the problem may
  not know the pattern name.
- Tools appendix format: [describe, for example a definition list with an endorsement mark, the tool
  name, what it is for, a bare domain, and the chapter reference].

## Fiction *(optional)*

Chicago is the usual reference for fiction too. Most of this guide still applies; the sections on
citations, Further Reading, worksheets, learning lists, and tools usually do not.

### Story bible

Details established anywhere in the manuscript are locked canon unless the author changes them on
purpose. The story bible is: [file name]. It records:

- **Characters:** full name and every nickname and who uses it, age and birthday (ages advance
  with the timeline), physical details (eyes, hair, height, scars, handedness), family and
  relationships, job and history, speech habits and verbal tics, and what each character knows
  and when they learned it.
- **Timeline:** dates or story days for each scene, day of the week, season, weather, travel and
  healing times, and how long ago past events happened.
- **Places:** names, layouts (which room is upstairs, which way a window faces), distances, and
  what is where.
- **Objects:** who has what, and where it is when last seen.
- **World rules:** magic, technology, laws, money, and anything else that limits what characters
  can do. A rule broken once needs a reason on the page.
- **Point of view:** whose point of view each scene or chapter uses.

### Point of view and tense

- Point of view: [first, close third, omniscient, or rotating, and the rule for switching, such as
  one per scene or one per chapter].
- Tense: [past or present]. Flashbacks: [how they are marked].
- Head-hopping (a scene slipping into another character's thoughts) is a defect unless the book is
  omniscient.

### Dialogue

- Punctuation follows Chicago: comma inside the closing quotation mark before a tag ("I know," she
  said.), a new paragraph for each new speaker, and an action beat in place of a tag where it helps.
- Tags: "said" and "asked" by default. Flag said-bookisms (hissed, chortled, ejaculated) and adverbs
  propping up a tag ("said angrily").
- Interrupted speech ends with an em dash or the book's chosen mark; trailing speech ends with an
  ellipsis.
- Fragments, slang, dialect, and grammar errors inside dialogue are voice, not defects, as long as
  they are consistent for that character.
- Thoughts: [italic, or tagged without italics].

### Fiction prose patterns

- Filter words between the reader and the experience: saw, heard, felt, noticed, realized,
  wondered, seemed. "She heard the door slam" becomes "The door slammed."
- Telling an emotion the scene already shows, or naming an emotion the scene never earns.
- Anachronisms in historical or period settings: words, objects, and attitudes that do not fit the
  time.
- Scene breaks: [the mark used, such as a centered ornament]. Each scene has a change: something
  is learned, decided, lost, or won.

## Prose patterns

These are style rules about sentences rather than words. Exclusions for every pattern below:
verbatim quotes, front-of-chapter learning lists, end-of-chapter question sets, worksheets, and AI
prompts. The author's stories get a lighter touch: "I think" inside an anecdote is voice; "I think"
in front of an instruction is a hedge. A rewrite must not introduce a different pattern from this
section.

### Sentence endings

- Do not end a sentence (or the clause before a colon or semicolon) on a preposition: about, at,
  by, for, from, in, into, of, on, over, through, to, toward, under, with. "A tool you can rely on"
  becomes "a reliable tool."
- Do not end on do, does, did, or doing standing in for a verb said earlier ("more than you think
  you do"). Use the real verb or recast. "What they do" at the end is usually a vague verb with a
  better replacement.
- Not defects: phrasal verbs (set up, log in, follow up, roll back, figure out) and short questions
  that would sound stilted rearranged ("Who did you work with?").

### Repetitive phrasing

- Repeated openers: consecutive sentences or paragraphs that start the same way ("Another," "This,"
  "It is," "When you"), and openers the author leans on everywhere.
- Ordinal scaffolding: processes narrated with "First," "Next," "Then," "After that," "Finally." One
  sequence is fine; a book where every process reads this way has a tic.
- Pet phrases: "make sure," "it's important to," "at the end of the day," and similar, when they
  recur across chapters or more than twice in a section.
- Repeated frames: the same move opening or closing several sections, such as a rhetorical question
  or "Imagine."
- Echoes: the same distinctive word twice within a few sentences by accident.
- Overused words: a word or phrase the chapter leans on even when the uses are far apart (count
  them; anything well above the rest of the book is worth a look).
- Repeated points: the same idea made twice in different words, in a section summary that only
  restates the section, or in a closing that repeats the opening.
- Repeated sentence shape: a run of sentences with the same length and structure, such as several
  "X is Y. It does Z." pairs in a row.
- Fiction: repeated gestures and beats (nodding, sighing, smiling, shrugging, looking, a breath
  someone did not know they were holding) and a character's tic used so often it stops being
  characterization.
- Not defects: deliberate parallel structure, a refrain used on purpose, and fixed terms that must
  stay identical.
- Vary the fixes rather than trading one habit for another: tie a step to its trigger, show cause
  and effect, lead with the stakes, let a strong topic sentence carry the order, merge two
  sentences that open the same way, or move a true procedure into a numbered list.

### AI tells

- Contrast framing: "It's not X, it's Y," "not just X, but Y," where nobody claimed X.
- Reflexive triplets: three items where the honest count is two or four.
- Stock vocabulary: delve, crucial, pivotal, robust, seamless, landscape, realm, tapestry, foster,
  elevate, empower, unlock, game-changer, deep dive, at its core, navigate (outside literal
  navigation), and leverage as a verb.
- Hedge-then-assert openers: "While X is important, Y..." and "Although many believe X..."
- Closing summary lines: a paragraph that ends by restating its own point in a neat sentence.
- Rhetorical questions answered in the next sentence.
- Punctuation stand-ins: colons and semicolons splitting nearly every sentence in a paragraph.
- Generic examples: "Imagine a team that..." where a real story or the running example would carry
  real detail.
- Uniform rhythm: runs of sentences, or paragraphs, of the same length and shape.
- Not defects: a single contrast used for emphasis, a list that really has three items, and a
  flagged word used in its technical sense.

### Signposting

- Allowed: the chapter opening's short preview, the Summary's recap and handoff, and a
  cross-reference that names its destination.
- Not allowed: narrating the current section ("In this section, we will..."), "In this chapter"
  past the opening, transition announcements ("Now that we've covered X, let's turn to Y," "Let's
  dive in"), vague pointers ("as mentioned earlier," "more on this later"), and a first sentence
  that restates the heading above it.

### Filler and wordiness

- Intensifiers: really, very, just, actually, basically, simply, literally, truly, definitely,
  certainly, totally, extremely, incredibly, quite, rather, and "pretty" as an adverb.
- Hedges: kind of, sort of, a bit, a little, somewhat, perhaps, tend to, "you may want to
  consider," "you might want to," "it can be helpful to," "try to."
- Throat-clearing: "It's worth noting that," "Keep in mind that," "Remember that," "The thing is,"
  "Needless to say," "Of course," "Obviously," "Clearly," "Interestingly," "In fact."
- Wordy phrases: in order to (to), due to the fact that (because), at this point in time (now), a
  number of (several), the majority of (most), is able to (can), for the purpose of (for), with
  regard to or in terms of (about), on a daily basis (daily).
- Empty openings: "There are many engineers who..." (Many engineers...), "It is the manager who
  decides" (The manager decides), "What this means is."
- Weak verb plus noun: make a decision (decide), conduct an analysis (analyze), provide support
  (support).
- Redundant pairs: first and foremost, each and every, end result, future plans, past experience,
  completely eliminate, basic fundamentals, close proximity, and any modifier on an absolute ("very
  unique").
- Filler transitions: Additionally, Furthermore, Moreover, Ultimately, Essentially, That said, With
  that in mind.
- Asides to the reader: "As you can see," "As you know," "You might be wondering."

### Author's known habits

Patterns this author knows they overuse. The chapter review asks for these at the start of every
review and checks each one in every chapter. Add to the list whenever an editor or reviewer points
out a new one.

| Habit | What to look for | Preferred fix |
|---|---|---|
| [Too many rhetorical questions] | [Clusters of questions in body prose standing in for guidance; worksheet prompts are exempt] | [Keep the ones doing real work; turn the rest into statements or concrete examples] |
| [habit] | [what it looks like] | [fix] |

### Vocabulary and register

- Prefer the precise word to a colloquial one ("get," "do," "hard") where a more specific word fits
  the register of professional nonfiction.
- A comparison, distinction, or threshold is always resolved ("the line between X and Y is the
  level" says what the level is).

## Accessibility

- Every image has real alt text: for a figure, what it shows and the point it makes; for a
  worksheet, its title, every field, and any filled-in example; for a chart, the trend and key
  numbers. Decorative images are marked decorative.
- Alt text follows one pattern across the book: what it is, what it shows, why it matters.
- Tables and code are real text, not images.
- Meaning is never carried only by color, highlighting, position, or shape. Say it in words.
- No empty headings, no images inside headings, no skipped heading levels.
- No bare URLs in body text, and no symbols or arrows that carry meaning on their own.

## Reminders for front matter *(optional)*

Things the preface or introduction must explain once it is written: [for example, where quotes come
from, what "AI" means in the book, and how the book is organized].

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*
