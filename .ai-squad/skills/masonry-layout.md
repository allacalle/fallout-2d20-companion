# Masonry Layout

**Type:** CSS Pattern | **Use:** Responsive masonry grid for image galleries

## Description

How to implement a responsive masonry layout where images of varying aspect ratios flow naturally into columns — 3 columns on desktop, 2 on tablet, 1 on mobile.

## CSS-Only Masonry (Recommended)

### Using CSS Columns
```css
.masonryGrid {
  column-count: 3;
  column-gap: 16px;
}

.masonryItem {
  break-inside: avoid;
  margin-bottom: 16px;
}

/* Tablet */
@media (max-width: 1024px) {
  .masonryGrid {
    column-count: 2;
  }
}

/* Mobile */
@media (max-width: 640px) {
  .masonryGrid {
    column-count: 1;
  }
}
```

### Using CSS Grid (alternative)
```css
.masonryGrid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-auto-rows: 8px; /* small row height for fine-grained spanning */
  gap: 16px;
}

.masonryItem {
  /* Each item needs a calculated grid-row span based on its height */
  /* This requires JS to measure and set the span */
}
```

## CSS Modules Pattern

```css
/* Gallery.module.css */
.masonryGrid {
  column-count: 3;
  column-gap: var(--spacing-md, 16px);
}

.masonryItem {
  break-inside: avoid;
  margin-bottom: var(--spacing-md, 16px);
  border-radius: var(--radius-sm, 8px);
  overflow: hidden;
  transition: transform 200ms ease, box-shadow 200ms ease;
}

.masonryItem:hover {
  transform: scale(1.02);
  box-shadow: 0 0 20px var(--accent-purple, #a855f7);
}

@media (max-width: 1024px) {
  .masonryGrid { column-count: 2; }
}

@media (max-width: 640px) {
  .masonryGrid { column-count: 1; }
}
```

## Component Usage

```tsx
<div className={styles.masonryGrid}>
  {images.map((image) => (
    <div key={image.id} className={styles.masonryItem}>
      <ImageCard image={image} />
    </div>
  ))}
</div>
```

## Breakpoints

| Breakpoint | Width | Columns |
|-----------|-------|---------|
| Desktop | > 1024px | 3 |
| Tablet | 640-1024px | 2 |
| Mobile | < 640px | 1 |

## Gotchas

- **Column order vs row order** — CSS columns fill top-to-bottom, then left-to-right. This means newest items may not be at the top-left. If chronological order matters (newest first), consider CSS Grid with JS measurement instead.
- **break-inside: avoid** — prevents items from being split across columns. Essential.
- **Image loading** — images load asynchronously, which can cause layout shift. Use `aspect-ratio` or placeholder heights if possible.
- **Firefox column-count** — works well, but test for edge cases with very tall images.
- **prefers-reduced-motion** — disable hover animations for users who prefer reduced motion.

## When to Use JS Masonry

Use JavaScript-based masonry (measuring heights) only if:
- You need strict row-order (newest items always first, left-to-right)
- You have very varied image heights that break column aesthetics
- You need drag-and-drop reordering

For this project, CSS columns are sufficient and simpler.
