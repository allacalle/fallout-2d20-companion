# Post Writer

**Trigger**: "write a post", "LinkedIn post", "social media content", "draft a post"

**Dependencies**: Requires `about-brand.md` and `brand-voice.md` (run brand-voice-builder first if they don't exist)

## Description

Writes LinkedIn/Twitter posts in your brand voice.

## Step 1: Verify Dependencies

Read `about-brand.md` and `brand-voice.md`. If missing, tell Owner to run brand-voice-builder first.

## Step 2: Gather Inputs

Ask the Owner:
1. **What topic?** (or paste notes/transcripts)
2. **Which platform?** LinkedIn, Twitter, Instagram
3. **Do you have reference posts?** (optional)

## Step 3: Research & Plan

Before writing:
- Find relevant data/statistics
- Identify contrarian angles
- Find real examples or case studies

Present 3 possible angles and let Owner choose.

## Step 4: Write the Draft

Rules:
- Read `brand-voice.md` for tone, rhythm, hook style
- Respect opening and closing patterns
- Avoid EVERYTHING that says "we never do"
- Adapt length to platform:
  - **LinkedIn**: 150-300 words
  - **Twitter**: 280 chars (or 3-5 tweet thread)
  - **Instagram**: 100-200 words + visual suggestion

Output in code block for direct copy:

````
[Complete post with exact line breaks as they should appear]
````

## Step 5: Iterate

> How does this feel? Tell me what to change, or say "ready to publish" and I'll save the final version.

Max 3 revision rounds.

## Step 6: Save

If Owner approves, save as `.empresa/content/posts/[date]-[topic].md`

## Rules
- Always read about-brand.md and brand-voice.md
- Output in code block
- English unless brand-voice.md specifies otherwise
- Don't add hashtags unless the brand uses them
- Don't add engagement bait CTAs if not in the voice
