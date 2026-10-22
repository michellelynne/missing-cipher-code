---
name: interest-to-company-research
description: Turn a personal interest into a wide list of real companies that hire software engineers, working category by category across the industry's value chain and returning a filled table plus an alphabetized company list. Use when someone wants to widen a "dream company" into a "dream industry," is filling in the Find Your Dream Pretty Good Job worksheet, or asks which companies work in a field they care about.
---

# SKILL: Interest-to-Company Market Research

**From:** Expand on Interests (Find Your Dream Pretty Good Job Worksheet)

## When to load this skill

Load this skill when the reader names one or more interests, hobbies, or passions and wants
to know which companies sit behind them. Also load it when they say they only have one dream
company and want more options.

## What this skill produces

Two artifacts, in this order:

1. **The interest table.** One table per interest, with a row for each category below and
   three to five real companies in each cell.
2. **The alphabetized company list.** Every company from every table, deduplicated and sorted,
   ready to paste into the Company List worksheet.

## The categories

The worksheet in the book prints a few of these as examples. This skill is not limited to that
set, and should run the full list.

Note that the first two categories describe **who a company sells to** and the rest describe
**where it sits in the industry**. Those are different questions, so companies will land in
more than one row. That overlap is expected and is handled at the deduplication step. Do not
try to force each company into a single row.

### Always run these

| Category | What belongs here |
|---|---|
| B2B | Companies selling into businesses in this space |
| B2C | Companies selling directly to consumers in this space |
| Education | Schools, training providers, certification bodies, courseware |
| Vendors and Suppliers | Companies selling the parts, tools, materials, or data others use |
| Retail and E-commerce | Companies selling the finished thing to buyers |
| Media, Community, and Publishing | Magazines, review sites, reference databases, forums, and the platforms built around the interest |
| Data, Analytics, and Marketplaces | Companies whose product is the data *about* the field, or the market connecting its buyers and sellers |
| Nonprofits, Associations, and Public Sector | Governing bodies, standards organizations, advocacy groups, and the agencies that regulate the space |
| Events, Venues, and Experiences | Gyms, festivals, tournaments, tours, conventions, and the ticketing and booking behind them |

The last four are the rows readers consistently cannot generate on their own, and Media and
Data are usually where the surprises are. Give them real effort rather than filling them last.

### Run these when the interest warrants

| Category | Include it when |
|---|---|
| Agencies and Consultancies | The industry buys services rather than building in-house. These firms appear in neither a B2B nor a B2C framing and are easy to miss entirely. |
| Hardware and Manufacturing | The interest involves physical goods. Often carries embedded and device roles rather than web ones, which suits some readers and not others. |

Skip a conditional category rather than padding it. Say it was skipped and why.

## How to run it

**Step 1. Get the interest.** Ask for the interest in the reader's own words. Do not tidy it
into a market category. "Rock climbing" is a better input than "outdoor recreation," because
the specific version surfaces companies the general version hides.

**Step 2. Work one category at a time.** Say what kind of company each category is looking for
in this specific interest before naming any. Working category by category is what makes the
list wide instead of five variations on the same obvious company.

**Step 3. Check that each company actually employs software engineers.** A company that
outsources all of its technology is not a target. If the answer is uncertain, keep the company
and mark it `[verify]`.

**Step 4. Name the less obvious ones.** For each category, include at least one company the
reader is unlikely to have thought of, and add a short clause on why it belongs there. The
obvious companies are already in their head. The point of the table is the rest.

**Step 5. Derive anything the categories missed.** The list above is a starting frame, not a
complete map of any particular industry. Walk the value chain for this specific interest from
raw input to end customer and name any position the categories did not cover. Add those as
extra rows, named for what they actually are. Every industry has at least one.

**Step 6. Let thin rows be thin.** Some categories genuinely have few companies for a given
interest. Report the short row honestly rather than padding it with companies that only
loosely belong. A padded row costs the reader research time later.

**Step 7. Produce the alphabetized list.** Deduplicate across categories. Where a company
appears in more than one category, keep it once and note the categories in parentheses.

**Step 8. Close with the reframe.** State how many companies came out of one interest, and
point out that the goal has moved from one dream company to a dream industry.

## Worked example

For the interest **music**, the less obvious rows fill in like this:

- **Media, Community, and Publishing:** Bandcamp, Genius, Discogs. Reference databases and
  catalog search at real scale.
- **Data, Analytics, and Marketplaces:** Chartmetric, Luminate, royalty and rights platforms.
  The product is the data about the industry, and the engineering is heavy.
- **Nonprofits, Associations, and Public Sector:** ASCAP, BMI, SoundExchange. Rights
  organizations running large payment and matching systems.
- **Events, Venues, and Experiences:** Dice, Bandsintown, Eventbrite. Ticketing, discovery,
  and the systems behind live shows.

None of these are the companies an engineer names when asked to think of a music company, and
all of them hire.

## Prompt the reader can run directly

> You are a market research assistant. I am a software engineer looking for companies to
> target in my job search. My interest is [INTEREST].
>
> Build a table with one row for each of these categories: B2B, B2C, Education, Vendors and
> Suppliers, Retail and E-commerce, Media and Community and Publishing, Data and Analytics and
> Marketplaces, Nonprofits and Associations and Public Sector, and Events and Venues and
> Experiences. Add rows for Agencies and Consultancies and for Hardware and Manufacturing if
> they are relevant to this interest.
>
> In each row, name three to five real companies that work in [INTEREST] in that category and
> that employ software engineers. Include at least one company in each row that a person
> outside the industry would not think of, with a short note on why it belongs. If a category
> genuinely has few companies for this interest, give me the short row rather than padding it.
>
> Then walk the value chain for [INTEREST] from raw input to end customer and tell me about any
> kind of company those categories missed.
>
> Then give me every company from the table in one alphabetized list, deduplicated, noting
> where a company appeared in more than one category.
>
> Do not invent companies. If you are not confident a company is real, currently operating, or
> employs engineers, mark it [verify] rather than dropping it.

## What to tell the reader

- **Verify before you invest time.** Company names, ownership, and whether a company still
  exists all change. Anything marked `[verify]` is a research task, not a fact.
- **A gut reaction is allowed here.** Scan the finished list and notice which companies pull
  at you. That reaction is the input to the filtering worksheets, which is where the
  data-driven decision actually gets made.
- **Run this more than once.** Each interest gets its own table. The lists are supposed to
  overlap; the overlap is a signal.
- **The unfamiliar rows are the point.** A reader who recognizes every company on the finished
  list has widened nothing.

## What this skill does not do

It does not rank companies, evaluate their benefits, or decide where to apply. It widens the
field. Filtering is a separate skill, and it comes after the reader knows what they are
filtering for.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*
