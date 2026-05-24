# Glassmorphism CSS

**Type:** CSS Pattern | **Use:** Glass-effect cards and overlays for modern UI design

## Description

How to implement glassmorphism — the frosted glass effect with backdrop blur, semi-transparent backgrounds, and subtle borders. Used for image cards, modals, and overlays in the Imaginarium gallery.

## Core Glassmorphism Recipe

```css
.glass {
  background: rgba(18, 18, 42, 0.6);      /* Semi-transparent dark */
  backdrop-filter: blur(12px);             /* Frosted glass effect */
  -webkit-backdrop-filter: blur(12px);     /* Safari support */
  border: 1px solid rgba(255, 255, 255, 0.08); /* Subtle edge */
  border-radius: 12px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3); /* Depth shadow */
}
```

## Card Glass (Image Cards)

```css
.imageCard {
  background: rgba(18, 18, 42, 0.5);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border: 1px solid rgba(168, 85, 247, 0.15); /* Purple tint */
  border-radius: var(--radius-md, 12px);
  overflow: hidden;
  transition: 
    border-color 200ms ease,
    box-shadow 200ms ease,
    transform 200ms ease;
}

.imageCard:hover {
  border-color: rgba(168, 85, 247, 0.4);
  box-shadow: 0 0 24px rgba(168, 85, 247, 0.2);
  transform: translateY(-2px);
}
```

## Modal Glass (Image Overlay)

```css
.modalOverlay {
  position: fixed;
  inset: 0;
  background: rgba(10, 10, 20, 0.85);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modalContent {
  background: rgba(18, 18, 42, 0.7);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: var(--radius-lg, 16px);
  padding: var(--spacing-xl, 24px);
  max-width: 90vw;
  max-height: 90vh;
  overflow: auto;
}
```

## Toggle/Panel Glass

```css
.panel {
  background: rgba(18, 18, 42, 0.4);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(6, 182, 212, 0.15); /* Cyan tint */
  border-radius: var(--radius-md, 12px);
  padding: var(--spacing-lg, 20px);
}
```

## CSS Modules Pattern

```css
/* ImageCard.module.css */
.card {
  composes: glass from global;
  /* Additional card-specific styles */
}

.cardImage {
  width: 100%;
  display: block;
  border-radius: var(--radius-md, 12px) var(--radius-md, 12px) 0 0;
}

.cardContent {
  padding: var(--spacing-md, 16px);
}
```

## Fallback for No Backdrop-Filter Support

```css
@supports not (backdrop-filter: blur(12px)) {
  .glass {
    background: rgba(18, 18, 42, 0.9); /* More opaque, no blur */
  }
}
```

## Readability Over Images

When displaying text over artwork:
```css
.textOverlay {
  background: linear-gradient(
    to top,
    rgba(10, 10, 20, 0.9) 0%,
    rgba(10, 10, 20, 0.5) 50%,
    transparent 100%
  );
  padding: var(--spacing-lg, 20px);
  /* Ensures text is readable regardless of image brightness */
}
```

## Gotchas

- **Safari requires -webkit- prefix** — always include `-webkit-backdrop-filter`
- **Performance on mobile** — heavy blur can cause jank on low-end devices. Use `blur(8px)` max on mobile.
- **Not a replacement for contrast** — glassmorphism can reduce text readability. Always check WCAG AA contrast.
- **Nested glass** — avoid stacking multiple glass elements (performance killer).
- **Firefox support** — backdrop-filter works in Firefox 103+. For older versions, use the fallback.
- **Testing** — verify the effect on both light and dark images. Dark images can make glass cards invisible.
