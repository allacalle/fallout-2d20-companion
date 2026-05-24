# Gallery Navigation

**Type:** UX Pattern | **Use:** Single-artwork-at-a-time gallery browsing with navigation

## Description

How to implement immersive gallery navigation where the visitor sees one artwork at a time, navigates with arrows/swipe, and can jump to any artwork via a mini-grid.

## Core Pattern

The gallery is a **slideshow experience**, not a grid. One artwork fills the viewport at a time.

### Navigation Methods
1. **Arrow buttons** — `←` anterior, `→` siguiente (visible on screen)
2. **Keyboard** — ArrowLeft / ArrowRight keys
3. **Swipe** — Touch swipe left/right on mobile
4. **Mini-grid** — Bottom strip showing thumbnails, click to jump

### State Management
```ts
interface GalleryState {
  currentIndex: number;    // 0-based index of current artwork
  totalWorks: number;      // Total count for counter
  artworks: Image[];       // All artworks (loaded once)
  isTransitioning: boolean; // Prevent interaction during animation
}
```

### Counter Display
```
"Obra 7 de 42"
```
- Always visible below the artwork
- Updates on navigation

### Circular Navigation
- Last artwork → next → first artwork
- First artwork → previous → last artwork

## Component Structure

```tsx
<GalleryView>
  <ArtworkDisplay artwork={artworks[currentIndex]} />
  <NavigationArrows 
    onPrev={() => navigate(currentIndex - 1)}
    onNext={() => navigate(currentIndex + 1)}
  />
  <Counter current={currentIndex + 1} total={artworks.length} />
  <MiniGrid 
    artworks={artworks}
    currentIndex={currentIndex}
    onSelect={(index) => navigate(index)}
  />
</GalleryView>
```

## Keyboard Navigation

```ts
useEffect(() => {
  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === 'ArrowLeft') onPrev();
    if (e.key === 'ArrowRight') onNext();
    if (e.key === 'Escape') onClose(); // if in modal
  };
  window.addEventListener('keydown', handleKeyDown);
  return () => window.removeEventListener('keydown', handleKeyDown);
}, [currentIndex]);
```

## Swipe (Touch) Navigation

```ts
// Use touch events or a lightweight library
// Detect swipe direction: deltaX > 50 = next, deltaX < -50 = prev
// Do NOT use heavy libraries — vanilla touch events are enough
```

## Mini-Grid

- Horizontal scrollable strip at bottom of screen
- Shows all artwork thumbnails (small, ~80px height)
- Current artwork highlighted with border/glow
- Click any thumbnail → jump to that artwork
- Smooth scroll to keep selected thumbnail visible

## Accessibility

- `aria-label` on navigation: "Anterior obra", "Siguiente obra"
- `role="region"` + `aria-roledescription="carousel"` on gallery
- `aria-live="polite"` on artwork display (announces change to screen readers)
- Focus moves to artwork after navigation
- Keyboard navigation must work (tab + arrows)
- Respect `prefers-reduced-motion` — disable transitions

## URL State (Optional but Recommended)

```
/gallery/7  → shows artwork with id 7
```
- Enables sharing direct links to specific artworks
- Use React Router or hash-based routing
- On page load, parse URL and set currentIndex

## Gotchas

- **Preload adjacent artworks** — preload next and previous images for instant navigation
- **Disable buttons during transition** — prevent rapid-fire navigation
- **Handle empty gallery** — show EmptyState, not broken navigation
- **Image loading** — show skeleton/placeholder while image loads
- **Mobile viewport** — account for browser chrome/URL bar height
