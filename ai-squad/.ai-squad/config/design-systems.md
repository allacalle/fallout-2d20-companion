# Design Systems Library

72 pre-built design systems for instant visual consistency. Use with the Designer agent and Direction Picker.

## HOW TO USE

1. Designer selects a design system that matches the project
2. Apply its tokens in DESIGN.md
3. Reference this file for exact values

---

## PRODUCT DESIGN SYSTEMS

### Developer Tools
| System | Primary | Accent | Font | Vibe |
|--------|---------|--------|------|------|
| **Linear** | `#5E6AD2` | `#5E6AD2` | Inter | Fast, minimal, purple |
| **Vercel** | `#000000` | `#0070F3` | Geist | Bold, black, geometric |
| **Supabase** | `#3ECF8E` | `#3ECF8E` | Inter | Green, open, modern |
| **Cursor** | `#A390D0` | `#A390D0` | Inter | AI-first, soft purple |
| **Anthropic** | `#D97757` | `#D97757` | Tiempos | Warm, intellectual |
| **Raycast** | `#FF6363` | `#FF6363` | Inter | Red, productive |
| **GitHub** | `#238636` | `#238636` | Mono | Green, developer |
| **Sentry** | `#362D59` | `#FB6429` | Rubik | Purple-orange, error tracking |
| **PostHog** | `#1D4AFF` | `#1D4AFF` | Inter | Blue, analytics |
| **Resend** | `#000000` | `#FF6D00` | Inter | Black-orange, email |
| **Cohere** | `#3E62E6` | `#3E62E6` | Inter | Blue, NLP |
| **Mistral** | `#FF6F00` | `#FF6F00` | Inter | Orange, French AI |
| **ElevenLabs** | `#7C3AED` | `#7C3AED` | Inter | Purple, voice AI |
| **X.AI** | `#000000` | `#FFFFFF` | Inter | Black-white, minimal |
| **Lovable** | `#E11D48` | `#E11D48` | Inter | Rose, friendly AI |
| **Clay** | `#FF6B35` | `#FF6B35` | Inter | Orange, CRM |
| **Composio** | `#6366F1` | `#6366F1` | Inter | Indigo, integrations |

### SaaS & Productivity
| System | Primary | Accent | Font | Vibe |
|--------|---------|--------|------|------|
| **Stripe** | `#635BFF` | `#00D924` | Stripe Inhouse | Purple-green, payments |
| **Notion** | `#000000` | `#000000` | Inter | Black, wiki |
| **Airbnb** | `#FF385C` | `#FF385C` | Cereal | Pink-red, travel |
| **Figma** | `#F24E1E` | `#0ACF83` | Inter | Multi-color, design |
| **Slack** | `#4A154B` | `#4A154B` | Lato | Purple, chat |
| **Spotify** | `#1DB954` | `#1DB954` | Circular | Green, music |
| **Webflow** | `#4353FF` | `#4353FF` | Inter | Blue, no-code |
| **Sanity** | `#F03E2D` | `#F03E2D` | Inter | Red, CMS |
| **Cal.com** | `#292929` | `#111827` | Cal Sans | Dark, scheduling |
| **ClickHouse** | `#FFCC00` | `#FFCC00` | Inter | Yellow, database |
| **MongoDB** | `#00ED64` | `#00ED64` | Euclid | Green, document DB |
| **Replicate** | `#000000` | `#FFFFFF` | Inter | Black-white, AI models |

### Hardware & Consumer
| System | Primary | Accent | Font | Vibe |
|--------|---------|--------|------|------|
| **Apple** | `#000000` | `#0071E3` | SF Pro | Minimal, premium |
| **Tesla** | `#CC0000` | `#CC0000` | Tesla | Red, electric |
| **Xiaohongshu** | `#FE2C55` | `#FE2C55` | PingFang | Pink-red, social |

---

## DIRECTION × SYSTEM MAPPING

| Direction | Best Matching Systems |
|-----------|----------------------|
| **Editorial Monocle** | Stripe, Airbnb, Apple, Notion, Spotify |
| **Modern Minimal** | Linear, Vercel, GitHub, Raycast, Supabase |
| **Warm Soft** | ElevenLabs, Lovable, Cal.com, Sanity |
| **Tech Utility** | Sentry, PostHog, ClickHouse, MongoDB, Composio |
| **Brutalist Experimental** | Figma, Resend, X.AI, Tesla |

---

## QUICK TOKEN FORMAT

For each system, use in DESIGN.md:

```yaml
design_system:
  name: "Linear"
  source: "https://linear.app"
  colors:
    primary: "#5E6AD2"
    surface: "#FFFFFF"
    background: "#F7F8FA"
    text: "#1A1A2E"
    muted: "#8A8F98"
  typography:
    headings: "Inter"
    body: "Inter"
    code: "JetBrains Mono"
  spacing:
    unit: 4
    scale: [4, 8, 12, 16, 24, 32, 48, 64]
  radius:
    small: 4
    medium: 8
    large: 12
```

---

*Inspired by nexu-io/open-design and VoltAgent/awesome-design-md*
