# Mode Toggle Theatrical

**Type:** UX Pattern | **Use:** Dramatic full-screen transition between Studio and Gallery modes

## Description

How to implement a theatrical, immersive mode switch between "Estudio" (painter/creator mode) and "Galería" (visitor/contemplation mode). This is not a simple tab switch — it's an atmospheric transformation.

## The Two Modes

### 🎨 Modo Estudio (Pintor)
- **Atmosphere:** Íntimo, creativo, personal
- **Layout:** Input grande protagonista, preview de creación, botones Guardar/Descartar
- **Colors:** Slightly warmer tones, focused lighting feel
- **Typography:** More casual, inviting

### 🖼️ Modo Galería (Visitante)
- **Atmosphere:** Solemne, contemplativo, museístico
- **Layout:** Una obra a la vez, navegación, mini-grid, contador
- **Colors:** Darker, more dramatic, museum lighting
- **Typography:** More formal, museum-plaque style

## Toggle Component

```tsx
<ModeToggle 
  currentMode="studio" | "gallery"
  onToggle={(mode) => setMode(mode)}
/>
```

### Visual Design
- Two buttons with personality: 🎨 "Estudio" / 🖼️ "Galería"
- Active mode has glow/underline/highlight
- Inactive mode is muted
- Positioned top-center or top-right, always visible
- Click triggers full-screen transition animation

## Transition Animation

### Sequence (duration: ~600-800ms)
1. **Fade out** current mode content (200ms)
2. **Color wash** — background transitions to new mode palette (300ms)
3. **Fade in** new mode content (200ms)
4. **Subtle scale** — new content scales from 0.95 to 1.0 (300ms, overlaps with fade)

### CSS Implementation
```css
.mode-transition {
  transition: opacity 200ms ease, transform 300ms ease;
}

.mode-transition.entering {
  opacity: 0;
  transform: scale(0.95);
}

.mode-transition.entered {
  opacity: 1;
  transform: scale(1);
}

.mode-transition.exiting {
  opacity: 0;
}
```

### Background Transition
```css
.app-bg {
  transition: background-color 400ms ease;
}

.app-bg.studio {
  background-color: var(--bg-studio); /* slightly warmer */
}

.app-bg.gallery {
  background-color: var(--bg-gallery); /* darker, dramatic */
}
```

## State Preservation

- When switching modes, preserve:
  - Current gallery position (which artwork was being viewed)
  - Any unsaved draft in Studio (warn before switching)
  - Like counts (already in DB)
- Do NOT reset the gallery index on mode switch

## Accessibility

- `prefers-reduced-motion`: Skip animation, instant switch
- `aria-pressed` on toggle buttons
- Announce mode change to screen readers: `aria-live="polite"`
- Focus management: focus moves to primary element of new mode
- Keyboard accessible: Tab to toggle, Enter/Space to activate

## Implementation Pattern

```tsx
function App() {
  const [mode, setMode] = useState<'studio' | 'gallery'>('gallery');
  const [isTransitioning, setIsTransitioning] = useState(false);

  const handleToggle = (newMode: 'studio' | 'gallery') => {
    setIsTransitioning(true);
    setTimeout(() => {
      setMode(newMode);
      setTimeout(() => setIsTransitioning(false), 400);
    }, 200);
  };

  return (
    <div className={`app-bg ${mode}`}>
      <ModeToggle currentMode={mode} onToggle={handleToggle} />
      <div className={`mode-transition ${isTransitioning ? 'exiting' : 'entered'}`}>
        {mode === 'studio' ? <StudioView /> : <GalleryView />}
      </div>
    </div>
  );
}
```

## Gotchas

- **Don't block interaction for too long** — 800ms max transition
- **Don't lose user state** — if they were mid-generation, warn or preserve
- **Mobile consideration** — transition should feel smooth on slow devices
- **Double-tap protection** — disable toggle during animation
- **URL state** — optionally reflect mode in URL: `/studio` vs `/gallery`
