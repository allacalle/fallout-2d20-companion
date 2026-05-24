# Direction Picker — Visual Style Selection

When the Designer agent begins work on a new project or major redesign, they MUST select a visual direction BEFORE creating DESIGN.md.

## THE 5 DIRECTIONS

Each direction ships a deterministic palette + font stack. No freestyle.

---

### 1. Editorial Monocle
**Vibe**: Sophisticated magazine, cultural authority, editorial typography
- **Colors**: Black `#0A0A0A`, Cream `#F5F0E8`, Accent Red `#C41E3A`, Secondary Gray `#6B6B6B`
- **Fonts**: Playfair Display (headings), Inter (body)
- **Spacing**: Generous whitespace, asymmetric grids
- **Use for**: Blogs, magazines, portfolios, cultural brands

### 2. Modern Minimal
**Vibe**: Clean, functional, "it just works"
- **Colors**: White `#FFFFFF`, Near-black `#1A1A1A`, Accent Blue `#2563EB`, Light Gray `#F3F4F6`
- **Fonts**: Inter (headings), Inter (body) — single typeface
- **Spacing**: Systematic 4px/8px grid
- **Use for**: SaaS, tools, dashboards, developer products

### 3. Warm Soft
**Vibe**: Approachable, friendly, human-centered
- **Colors**: Warm White `#FFFDF7`, Soft Brown `#8B6F47`, Accent Coral `#E8836B`, Sage `#A8B5A2`
- **Fonts**: DM Sans (headings), Source Sans 3 (body)
- **Spacing**: Rounded corners, soft shadows, generous padding
- **Use for**: Lifestyle brands, wellness, education, community

### 4. Tech Utility
**Vibe**: Developer-first, dark mode, information-dense
- **Colors**: Dark `#0D1117`, Surface `#161B22`, Accent Green `#3FB950`, Text `#E6EDF3`, Muted `#8B949E`
- **Fonts**: JetBrains Mono (code + headings), Inter (body)
- **Spacing**: Compact, tabular data, monospace accents
- **Use for**: Dev tools, APIs, terminals, data products

### 5. Brutalist Experimental
**Vibe**: Bold, unconventional, anti-design
- **Colors**: White `#FFFFFF`, Black `#000000`, Accent Yellow `#FFD600`, Accent Pink `#FF6B9D`
- **Fonts**: Space Grotesk (headings), IBM Plex Mono (body)
- **Spacing**: Harsh borders, overlapping elements, intentional asymmetry
- **Use for**: Creative agencies, art projects, disruptive startups

---

## HOW TO USE

1. Read the project brief / PRODUCT.md
2. Identify the project's audience and purpose
3. Select the direction that best matches
4. Use the EXACT colors and fonts from that direction in DESIGN.md
5. Document your choice: "Visual Direction: [name] — because [reason]"

## RULES

- **Do NOT mix directions** — Pick ONE and stick with it
- **Do NOT invent new colors** — Use the palette as-is
- **You MAY adjust ONE accent color** if the brand requires it (document why)
- **WCAG AA contrast** must still pass — verify all text/background combos

## OUTPUT IN DESIGN.md

```yaml
visual_direction:
  name: "Modern Minimal"
  reason: "SaaS dashboard targeting developers — needs clean, functional aesthetic"
  palette:
    primary: "#FFFFFF"
    surface: "#1A1A1A"
    accent: "#2563EB"
    muted: "#F3F4F6"
  typography:
    headings: "Inter"
    body: "Inter"
```

---

*Inspired by alchaincyf/huashu-design and nexu-io/open-design*
