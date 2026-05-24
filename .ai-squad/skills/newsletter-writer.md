# Newsletter Writer

**Trigger**: "write newsletter", "weekly newsletter", "email newsletter", "email marketing"

**Dependencies**: Reads `about-brand.md` and `brand-voice.md` if they exist

## Description

Writes newsletters/email marketing in your brand voice. Proven 5-section structure.

## Step 1: Gather Inputs

1. **Main topic for this edition?**
2. **Specific audience?** (devs, founders, marketers)
3. **Tone check?** Anything special this week?

## Step 2: Structure

**Subject Line** (3 options):
- Must be < 50 characters
- Curiosity + benefit
- No empty clickbait

**Opening** (1-2 paragraphs):
- Personal or contextual hook
- Why it matters NOW
- Max 100 words

**Body** (3-4 sections):
1. **Main Idea**: Your core thought
2. **Data/Evidence**: Data that supports it
3. **Example/Story**: Real case or analogy
4. **Actionable**: What to do with this info

**CTA** (1 paragraph):
- What you want them to do
- Link if applicable
- No more than 1 CTA

**Close** (1 paragraph):
- Memorable takeaway
- Personal, not corporate

## Step 3: Write

Rules:
- Conversational tone, not academic
- Short paragraphs (1-3 lines)
- Bold for scanning
- Max 600-800 words total

Output in code block:

```
Subject: [3 options]

[Full newsletter body]
```

## Step 4: Save

If approved: `.empresa/content/newsletters/[date]-[topic].md`

## Rules
- Always in second person ("you")
- No corporate jargon
- Every paragraph must earn its place
- If brand-voice.md exists, follow its rules
