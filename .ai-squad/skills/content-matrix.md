# Content Matrix

**Trigger**: "give me content ideas", "content matrix", "what should I post", "generate post ideas", "content plan"

**Dependencies**: Reads `about-brand.md` if it exists

## Description

Generates 32+ post ideas in a table, crossing content pillars with 8 proven formats. Justin Welsh style.

## Step 1: Gather Inputs

If `about-brand.md` exists, read it and extract pillars. If not, ask Owner:
- What does your product do?
- What are 3-4 content pillars? (main topics)

## Step 2: Build the Matrix

**X Axis (formats)**, always in this order:
1. **Actionable**: Ultra-specific how-to
2. **Motivational**: Inspiring story
3. **Analytical**: Breakdown of why something works
4. **Contrarian**: Go against common advice
5. **Observation**: Hidden or silent trend
6. **X vs Y**: Compare two tools/approaches
7. **Present vs Future**: Current state + prediction
8. **Listicle**: List of resources, tips, mistakes

**Y Axis (rows)**: 3-5 content pillars from Owner

Each cell = 1 specific, concrete idea. NOT generic.

## Step 3: Output

Markdown table in code block:

| Pillar / Format | Actionable | Motivational | Analytical | Contrarian | Observation | X vs Y | Present vs Future | Listicle |
|-----------------|------------|--------------|------------|------------|-------------|--------|-------------------|----------|
| Pillar 1 | [idea] | [idea] | [idea] | [idea] | [idea] | [idea] | [idea] | [idea] |
| Pillar 2 | [idea] | [idea] | [idea] | [idea] | [idea] | [idea] | [idea] | [idea] |
| Pillar 3 | [idea] | [idea] | [idea] | [idea] | [idea] | [idea] | [idea] | [idea] |

Below the table:
> The strongest idea is **[X]** because [reason]. Want me to develop it as a full post?

## Rules
- Minimum 3 pillars, maximum 5
- Each idea must be specific to that pillar AND that format
- Don't repeat ideas across pillars
- Concrete headlines, not generic topics
- Good: "The 3-line hook formula I stole from David Ogilvy"
- Bad: "Hooks"
