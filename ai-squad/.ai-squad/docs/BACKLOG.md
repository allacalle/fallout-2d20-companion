# BACKLOG — Sprint #1: Imaginarium MVP

**Project:** experimento-b7-imaginarium
**Sprint:** #1 (MVP — Full Implementation)
**Date:** 2026-05-22
**Status:** READY FOR PARALLEL EXECUTION

---

## Objective

Implement the complete Imaginarium MVP: a two-mode (Studio/Gallery) AI art gallery with React 19 + Vite 6 frontend, Express 4 + TypeScript backend, Supabase PostgreSQL database, 4 REST endpoints, Pollinations + HuggingFace image generation, seed data (5 artworks), autoplay slideshow, theatrical mode toggle, and WCAG AA accessibility.

---

## BACKEND Tasks

### BE-01: Project Setup — Express + TypeScript + tsx

- **File:** `backend/package.json`, `backend/tsconfig.json`, `backend/.env.example`
- **Locked against:** ADR-001 (stack), ADR-007 (dev setup)
- **Acceptance criteria:**
  - `package.json` with dependencies: `express@4`, `cors`, `postgres`, `@supabase/storage-js`, `dotenv`, `typescript`, `tsx`, `@types/express`, `@types/node`, `@types/cors`
  - `tsconfig.json` with `target: ES2020`, `module: ESNext`, `moduleResolution: bundler`, `esModuleInterop: true`, `strict: true`, `outDir: dist`, `rootDir: src`
  - `scripts`: `"dev": "tsx watch src/index.ts"`, `"build": "tsc"`, `"start": "node dist/index.js"`, `"seed": "tsx seed/load.ts"`
  - `.env.example` with `DATABASE_URL`, `HF_API_TOKEN`, `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `FRONTEND_URL`, `PORT`, `NODE_ENV`
  - `backend/src/index.ts` creates Express app, listens on `process.env.PORT || 3001`
  - `npm run dev` starts server with hot reload on port 3001

### BE-02: Database Connection Module

- **File:** `backend/src/db.ts`
- **Locked against:** ADR-002 (Supabase PostgreSQL via `postgres`), API_CONTRACT.md §6 (schema)
- **Acceptance criteria:**
  - Exports a `postgres` client initialized from `process.env.DATABASE_URL`
  - Connection pool configured with default settings (Postgres.js handles pooling)
  - Exports `initSchema()` function that runs `CREATE TABLE IF NOT EXISTS images (...)` with all columns per API_CONTRACT.md §6.1
  - Schema includes: `id SERIAL PRIMARY KEY`, `prompt TEXT NOT NULL`, `image_url TEXT NOT NULL`, `description TEXT NOT NULL DEFAULT ''`, `created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()`, `likes INTEGER NOT NULL DEFAULT 0`, `is_seed BOOLEAN NOT NULL DEFAULT false`, `signature_hash TEXT`
  - Creates index `idx_images_created_at ON images (created_at DESC)` if not exists
  - `ALTER TABLE ... ADD COLUMN IF NOT EXISTS` for `is_seed` and `signature_hash` (idempotent migration)
  - Connection test on startup — logs error and exits if `DATABASE_URL` is missing or connection fails

### BE-03: Seed Data Loading

- **File:** `backend/seed/artworks.json`, `backend/seed/load.ts`
- **Locked against:** ADR-009 (JSON seed file, 5 artworks, is_seed + signature_hash)
- **Acceptance criteria:**
  - `backend/seed/artworks.json` contains exactly 5 curated artworks with fields: `prompt`, `image_url` (real Pollinations URLs), `description` (poetic Spanish text)
  - `load.ts` reads JSON, generates random 8-char hex `signature_hash` per artwork (`crypto.randomBytes(4).toString('hex')`)
  - Checks if table is empty: `SELECT COUNT(*) FROM images`
  - If empty: inserts all 5 artworks with `is_seed = true`, `signature_hash`, `description`
  - If not empty: skips (idempotent — does not duplicate)
  - Runnable via `npm run seed` or called automatically from `initSchema()` on first startup
  - Each seed artwork has a valid Pollinations URL (URL-encoded prompt)

### BE-04: GET /api/images Endpoint

- **File:** `backend/src/routes/images.ts` → `GET /api/images`
- **Locked against:** API_CONTRACT.md §1.1, ADR-003 (REST style)
- **Acceptance criteria:**
  - Returns `ImageListItem[]` ordered by `created_at DESC` (newest first)
  - Response shape: `{ id, prompt, image_url, created_at, likes, is_seed }` — **NO `description` field**
  - Returns empty array `[]` if no images exist (200 OK)
  - `created_at` formatted as ISO 8601 string (e.g., `"2026-05-22T14:30:00.000Z"`)
  - `is_seed` returned as boolean (`true`/`false`)
  - On DB error: returns 500 with `{ "error": "Error interno del servidor. Intenta de nuevo." }`
  - Uses `try/catch` + `next(err)` pattern (ADR-001: Express 4 manual error handling)

### BE-05: POST /api/images Endpoint

- **File:** `backend/src/routes/images.ts` → `POST /api/images`, `backend/src/lib/pollinations.ts`, `backend/src/lib/huggingface.ts`, `backend/src/lib/description.ts`
- **Locked against:** API_CONTRACT.md §1.2, §5 (image generation flow), ADR-004 (Pollinations + HuggingFace fallback), ADR-005 (non-blocking description), ADR-008 (storage strategy)
- **Acceptance criteria:**
  - **Validation** (API_CONTRACT.md §3.1):
    - Missing `prompt` → 400 `{ "error": "El campo 'prompt' es obligatorio." }`
    - Not a string → 400 `{ "error": "El campo 'prompt' debe ser un texto." }`
    - Empty after trim → 400 `{ "error": "El campo 'prompt' no puede estar vacío." }`
    - >500 chars after trim → 400 `{ "error": "El campo 'prompt' no puede exceder 500 caracteres." }`
  - **Primary: Pollinations** (`lib/pollinations.ts`):
    - `GET https://image.pollinations.ai/prompt/${encodeURIComponent(prompt)}`
    - Timeout: 30s via `AbortController`
    - On failure: retry once (same URL, 30s timeout)
    - On success: store URL directly in DB (no download, per ADR-008)
  - **Fallback: HuggingFace** (`lib/huggingface.ts`):
    - `POST https://router.huggingface.co/v1/images/generations`
    - Headers: `Authorization: Bearer ${process.env.HF_API_TOKEN}`, `Content-Type: application/json`
    - Body: `{ model: "black-forest-labs/FLUX.1-dev", prompt: prompt }`
    - Timeout: 30s
    - On success: upload binary to Supabase Storage bucket `images`, store public URL
    - On failure: return 502 `{ "error": "No se pudo generar la imagen. Intenta de nuevo." }`
  - **Save to DB:**
    - `INSERT INTO images (prompt, image_url, description, is_seed, signature_hash) VALUES ($1, $2, '', false, null) RETURNING id, prompt, image_url, created_at, likes, is_seed`
  - **Response:** 201 with `ImageListItem` (no `description`)
  - **Async description** (`lib/description.ts`):
    - Fire-and-forget: `GET https://text.pollinations.ai/${encodeURIComponent(prompt + " Write a poetic museum description in Spanish, 2-3 sentences.")}`
    - Timeout: 15s
    - On success: `UPDATE images SET description = $1 WHERE id = $2`
    - On failure: description remains `''` (no error returned)
  - **Error handling:** 500 for unexpected errors, 502 if both providers fail

### BE-06: GET /api/images/:id Endpoint

- **File:** `backend/src/routes/images.ts` → `GET /api/images/:id`
- **Locked against:** API_CONTRACT.md §1.3
- **Acceptance criteria:**
  - Path param `:id` parsed as integer
  - Non-integer IDs → 404 `{ "error": "Imagen no encontrada." }`
  - Query: `SELECT * FROM images WHERE id = $1`
  - If no row found → 404 `{ "error": "Imagen no encontrada." }`
  - Response shape `ImageDetail`: `{ id, prompt, image_url, description, created_at, likes, is_seed, signature_hash }`
  - `description` included (may be empty string)
  - `signature_hash` included (string or null)
  - On DB error: 500

### BE-07: PATCH /api/images/:id/like Endpoint

- **File:** `backend/src/routes/images.ts` → `PATCH /api/images/:id/like`
- **Locked against:** API_CONTRACT.md §1.4, ADR-006 (no auth, no duplicate prevention)
- **Acceptance criteria:**
  - Path param `:id` parsed as integer
  - Non-integer IDs → 404
  - Query: `UPDATE images SET likes = likes + 1 WHERE id = $1 RETURNING likes`
  - If no row affected → 404 `{ "error": "Imagen no encontrada." }`
  - Response: 200 `{ "likes": <new_count> }`
  - No auth check (ADR-006)
  - No duplicate like prevention (ADR-006)
  - On DB error: 500

### BE-08: Error Handling Middleware

- **File:** `backend/src/middleware/errorHandler.ts`
- **Locked against:** API_CONTRACT.md §4 (error handling), §8.1 (global error handler)
- **Acceptance criteria:**
  - Express error handler: `(err, _req, res, _next) => { ... }`
  - Logs error with `console.error(err)`
  - Returns 500 with `{ "error": "Error interno del servidor. Intenta de nuevo." }`
  - Handles `next(err)` calls from all route handlers
  - Sets `Content-Type: application/json` on all error responses
  - Mounted after all routes in `index.ts`

### BE-09: CORS Configuration

- **File:** `backend/src/index.ts` (CORS middleware setup)
- **Locked against:** API_CONTRACT.md §7, ADR-007 (Vite proxy in dev, CORS in prod only)
- **Acceptance criteria:**
  - In development (`NODE_ENV !== 'production'`): **NO CORS middleware** (Vite proxy handles it)
  - In production (`NODE_ENV === 'production'`): `app.use(cors({ origin: process.env.FRONTEND_URL }))`
  - `cors` package imported and used
  - `FRONTEND_URL` env var required in production
  - All endpoints support CORS with configured origin in production

---

## FRONTEND Tasks

### FE-01: Project Setup — Vite + React 19 + TypeScript

- **File:** `frontend/package.json`, `frontend/tsconfig.json`, `frontend/vite.config.ts`, `frontend/index.html`
- **Locked against:** ADR-001 (stack), ADR-007 (dev setup, Vite proxy)
- **Acceptance criteria:**
  - `package.json` with dependencies: `react@19`, `react-dom@19`, `typescript`, `vite@6`, `@vitejs/plugin-react`, `@types/react`, `@types/react-dom`
  - `tsconfig.json` with `target: ES2020`, `module: ESNext`, `jsx: react-jsx`, `strict: true`, `moduleResolution: bundler`
  - `vite.config.ts` with `@vitejs/plugin-react` and `server.proxy: { '/api': { target: 'http://localhost:3001', changeOrigin: true } }`
  - `index.html` with `<div id="root"></div>`, Google Fonts import for Playfair Display, Inter, JetBrains Mono
  - `npm run dev` starts Vite on port 5173 with HMR
  - `npm run build` produces optimized production build in `dist/`

### FE-02: Entry Point + Global Styles

- **File:** `frontend/src/main.tsx`, `frontend/src/index.css`, `frontend/src/vite-env.d.ts`
- **Locked against:** DESIGN.md §1.7 (CSS custom properties), §15 (CSS reset), §16 (Google Fonts), §2.6 (typography CSS)
- **Acceptance criteria:**
  - `main.tsx`: `createRoot(document.getElementById('root')!).render(<React.StrictMode><App /></React.StrictMode>)`
  - `index.css` includes:
    - Google Fonts `@import` (Playfair Display 400/500/600/700, Inter 400/500/600, JetBrains Mono 400/500)
    - All CSS custom properties from DESIGN.md §1.7 (colors, spacing, radius, shadows, transitions, z-index, fonts)
    - CSS reset from DESIGN.md §15 (`box-sizing`, `margin: 0`, `padding: 0`, `antialiased`)
    - Base body styles (`font-family: var(--font-sans)`, `background-color: var(--bg-primary)`, `color: var(--text-primary)`)
    - `.sr-only` utility class for screen reader text
    - `:focus-visible` global focus style (`box-shadow: 0 0 0 3px rgba(168, 85, 247, 0.5)`)
    - `@media (prefers-reduced-motion: reduce)` disabling all transitions/animations
    - Heading styles (h1-h6) from DESIGN.md §2.6
    - Glassmorphism base classes (`.glass`, `.glass-panel`, `.glass-overlay`) from DESIGN.md §4.1
    - Skeleton shimmer animation from DESIGN.md §5.12
    - `@supports not (backdrop-filter: blur(12px))` fallbacks

### FE-03: TypeScript Types

- **File:** `frontend/src/types/index.ts`
- **Locked against:** COMPONENT_CONTRACT.md §1 (type definitions), API_CONTRACT.md §2 (data shapes)
- **Acceptance criteria:**
  - `ImageListItem`: `{ id: number; prompt: string; image_url: string; created_at: string; likes: number; is_seed: boolean }`
  - `ImageDetail extends ImageListItem`: `{ description: string; signature_hash: string | null }`
  - `ImageCreate`: `{ prompt: string }`
  - `LikeResponse`: `{ likes: number }`
  - `ErrorResponse`: `{ error: string }`
  - `Mode`: `'studio' | 'gallery'`
  - `AutoplayState`: `{ isActive: boolean; isPaused: boolean; currentIndex: number; inactivityTimer: number }`
  - `AutoplayAction`: union type with `TICK`, `RESET_INACTIVITY`, `PAUSE`, `RESUME`, `NEXT`, `SET_INDEX`
  - `FetchState`: `'idle' | 'loading' | 'success' | 'error'`
  - All types exported

### FE-04: API Client Module

- **File:** `frontend/src/api/images.ts`
- **Locked against:** COMPONENT_CONTRACT.md §10 (API client), API_CONTRACT.md (endpoints)
- **Acceptance criteria:**
  - `BASE_URL = '/api'`
  - `fetchImages(): Promise<ImageListItem[]>` — GET `/api/images`, throws on `!res.ok`
  - `fetchImageDetail(id: number): Promise<ImageDetail>` — GET `/api/images/:id`, throws with error message from response
  - `createImage(prompt: string): Promise<ImageListItem>` — POST `/api/images` with `{ prompt }`, throws on error
  - `likeImage(id: number): Promise<LikeResponse>` — PATCH `/api/images/:id/like`, throws on error
  - All functions use native `fetch`, no external HTTP library
  - Error messages extracted from `{ error: string }` response body

### FE-05: AutoplayContext

- **File:** `frontend/src/context/AutoplayContext.tsx`
- **Locked against:** ADR-010 (React Context + useReducer), COMPONENT_CONTRACT.md §4.4 (autoplay state)
- **Acceptance criteria:**
  - Creates `AutoplayContext` with `createContext`
  - Provider component `AutoplayProvider` wraps children
  - `useReducer` with state shape: `{ isActive: false, isPaused: false, currentIndex: 0, inactivityTimer: 5000 }`
  - Reducer handles actions: `TICK` (advance currentIndex circularly when active), `RESET_INACTIVITY` (reset timer to 5000ms, set isActive=false), `PAUSE` (set isPaused=true), `RESUME` (set isPaused=false, reset timer), `NEXT` (advance index), `SET_INDEX` (set specific index)
  - Single `setInterval` (4s) managed in `useEffect` — fires `TICK` when `isActive && !isPaused`
  - Inactivity `setTimeout` (5s) managed in `useEffect` — fires to set `isActive=true` when timer expires
  - `document.visibilitychange` listener: pauses on `hidden`, resumes on `visible`
  - Custom hook `useAutoplay()` returns `{ state, dispatch }` from `useContext`
  - Cleanup on unmount: clears interval and timeout

### FE-06: App.tsx — Root Component

- **File:** `frontend/src/App.tsx`
- **Locked against:** COMPONENT_CONTRACT.md §2.1 (App.tsx spec), API_CONTRACT.md §1.1 (GET list)
- **Acceptance criteria:**
  - State: `mode` (default `'studio'`), `images` (default `[]`), `fetchState` (default `'idle'`), `fetchError` (default `null`), `isTransitioning` (default `false`), `transitionPhase` (default `'idle'`)
  - On mount: `useEffect` calls `fetchImages()` from API client
    - `fetchState` → `'loading'` → success: `setImages(data)`, `'success'` → error: `setFetchError(err.message)`, `'error'`
    - Cleanup: `cancelled` flag to prevent state update on unmounted component
  - `refetchImages` callback: re-fetches `GET /api/images`, updates state
  - If `images.length === 0` and `mode === 'gallery'`: force `mode` to `'studio'`
  - `handleToggle(newMode)`: theatrical transition (exit 150ms → switch mode → enter 300ms), pauses autoplay on studio switch
  - Render: `<div className={\`app-bg ${mode === 'gallery' ? 'app-bg--gallery' : ''}\`}>`
    - `<ModeToggle currentMode={mode} onToggle={handleToggle} />`
    - `mode === 'studio'` → `<StudioView onImageSaved={refetchImages} />`
    - `mode === 'gallery' && images.length === 0` → `<EmptyState onGoToStudio={() => setMode('studio')} />`
    - `mode === 'gallery' && images.length > 0` → `<GalleryView images={images} />`
  - `<AutoplayProvider>` wraps all children
  - Screen reader announcements: `aria-live="polite"` for loading/error states
  - Skip link component for accessibility

### FE-07: ModeToggle Component

- **File:** `frontend/src/components/ModeToggle.tsx`, `frontend/src/components/ModeToggle.module.css`
- **Locked against:** COMPONENT_CONTRACT.md §2.2, DESIGN.md §5.1 (visual design), DESIGN.md §13.2 (screen reader)
- **Acceptance criteria:**
  - Props: `{ currentMode: Mode; onToggle: (mode: Mode) => void }`
  - Two buttons: "🎨 Estudio" and "🖼️ Galería"
  - `role="tablist"` on container, `role="tab"` on buttons, `aria-selected` per active state
  - Active button: `background: rgba(168, 85, 247, 0.2)`, `color: var(--text-accent)`, `box-shadow: 0 0 12px rgba(168, 85, 247, 0.15)`
  - Inactive button: `color: var(--text-muted)`
  - Desktop: `position: fixed`, `top: 16px`, `left: 50%`, `transform: translateX(-50%)`, `z-index: 100`
  - Mobile (`<1024px`): `top: 12px`, `right: 12px`
  - Glassmorphism background: `rgba(20, 27, 45, 0.5)`, `backdrop-filter: blur(8px)`, `border-radius: var(--radius-full)`
  - Focus-visible: `box-shadow: 0 0 0 3px rgba(168, 85, 247, 0.5)`
  - Keyboard: Tab navigation, Enter/Space activation

### FE-08: StudioView Component

- **File:** `frontend/src/components/StudioView.tsx`, `frontend/src/components/StudioView.module.css`
- **Locked against:** COMPONENT_CONTRACT.md §2.3, DESIGN.md §5.2 (layout)
- **Acceptance criteria:**
  - Props: `{ onImageSaved: () => void }`
  - State: `previewUrl` (string | null), `isGenerating` (boolean), `generationError` (string | null)
  - Renders `<GeneratePanel onSubmit={handleSubmit} isLoading={isGenerating} />`
  - `handleSubmit(prompt)`: calls `createImage(prompt)` from API client
    - `isGenerating` → `true`
    - Success: `setPreviewUrl(data.image_url)`, `isGenerating` → `false`
    - Error (502): `setGenerationError('No se pudo generar la imagen. Intenta de nuevo.')`
    - Error (400): `setGenerationError(error.error)`
    - Error (500): `setGenerationError('Error interno del servidor. Intenta de nuevo.')`
  - If `previewUrl` set: renders `<PreviewCard imageUrl={previewUrl} onSave={handleSave} onDiscard={handleDiscard} isSaving={false} />`
  - `handleSave`: calls `onImageSaved()`, clears `previewUrl`
  - `handleDiscard`: clears `previewUrl` (image lost)
  - Layout: `max-width: 640px`, centered, `padding: 64px 24px 32px`
  - `id="studio-panel"`, `role="tabpanel"`, `aria-labelledby="studio-tab"`
  - Error message: `role="alert"`
  - Screen reader announcements for loading, complete, error states

### FE-09: GeneratePanel Component

- **File:** `frontend/src/components/GeneratePanel.tsx`, `frontend/src/components/GeneratePanel.module.css`
- **Locked against:** COMPONENT_CONTRACT.md §2.4, DESIGN.md §5.3 (visual design)
- **Acceptance criteria:**
  - Props: `{ onSubmit: (prompt: string) => void; isLoading: boolean }`
  - State: `value` (string, default `''`)
  - Single text input with placeholder `"Describe la imagen que quieres ver..."`
  - Submit button (arrow/send icon) positioned inside input on the right (absolute positioning)
  - Form submission: trims value, validates non-empty, calls `onSubmit(trimmedValue)`
  - While `isLoading`: input disabled, button disabled, shows spinner + rotating loading messages: "Tejiendo píxeles...", "El algoritmo está pintando...", "Dando vida al lienzo...", "La IA sueña con tu imagen..." (cycle every 2s)
  - Input styling: `background: var(--bg-input)`, `border: 1px solid var(--border-input)`, `border-radius: var(--radius-full)`, focus border purple
  - `role="search"`, `aria-label="Generar imagen"`, input `aria-busy={isLoading}`
  - Keyboard: Enter submits, Escape clears input
  - Button: `width: 36px`, `height: 36px`, `background: var(--accent-purple)`, `border-radius: var(--radius-full)`

### FE-10: PreviewCard Component

- **File:** `frontend/src/components/PreviewCard.tsx`, `frontend/src/components/PreviewCard.module.css`
- **Locked against:** COMPONENT_CONTRACT.md §2.5, DESIGN.md §5.4 (visual design)
- **Acceptance criteria:**
  - Props: `{ imageUrl: string; onSave: () => void; onDiscard: () => void; isSaving: boolean }`
  - Image: `width: 100%`, `aspect-ratio: 1 / 1`, `object-fit: cover`, `max-width: 512px`
  - Two buttons: "Guardar en galería" (green, `--color-success`) and "Descartar" (red, `--color-danger`)
  - Save button: `background: rgba(52, 211, 153, 0.15)`, `color: var(--color-success)`, `border-color: rgba(52, 211, 153, 0.3)`
  - Discard button: `background: rgba(248, 113, 113, 0.1)`, `color: var(--color-danger)`, `border-color: rgba(248, 113, 113, 0.2)`
  - Entry animation: `fadeInScale` (300ms, `opacity: 0→1`, `transform: scale(0.95)→scale(1)`)
  - Glass card composition (`composes: glass`)
  - `role="region"`, `aria-label="Vista previa de imagen"`
  - Buttons disabled while `isSaving`

### FE-11: GalleryView Component

- **File:** `frontend/src/components/GalleryView.tsx`, `frontend/src/components/GalleryView.module.css`
- **Locked against:** COMPONENT_CONTRACT.md §2.6, DESIGN.md §5.5 (layout), ADR-010 (autoplay integration)
- **Acceptance criteria:**
  - Props: `{ images: ImageListItem[] }`
  - State: `currentIndex` (default `0`), `detailImage` (ImageDetail | null), `detailLoading` (boolean), `detailError` (string | null)
  - On mount or `currentIndex` change: fetches `fetchImageDetail(images[currentIndex].id)`
  - Autoplay integration: consumes `AutoplayContext`, dispatches `RESET_INACTIVITY` on user navigation
  - Circular navigation: `(prev + 1) % length` and `(prev - 1 + length) % length`
  - Keyboard handler: `ArrowRight` → next, `ArrowLeft` → prev, `Home` → first, `End` → last
  - Touch swipe: tracks `touchstart`/`touchend`, horizontal swipe > 50px navigates
  - Renders: `ArtworkDisplay`, `NavigationArrows`, `Counter`, `ArtworkDescription`, `MiniGrid`
  - Autoplay progress bar: visible when `isActive && !isPaused`
  - `id="gallery-panel"`, `role="tabpanel"`, `aria-labelledby="gallery-tab"`

### FE-12: ArtworkDisplay Component

- **File:** `frontend/src/components/ArtworkDisplay.tsx`, `frontend/src/components/ArtworkDisplay.module.css`
- **Locked against:** COMPONENT_CONTRACT.md §2.7, DESIGN.md §5.6 (visual design), DESIGN.md §7 (responsive)
- **Acceptance criteria:**
  - Props: `{ image: ImageDetail }`
  - Image centered, `max-height: 80vh` (desktop) / `55vh` (mobile), `object-fit: contain`
  - Hover effect: `box-shadow: 0 0 40px rgba(168, 85, 247, 0.25)`
  - `alt={image.prompt}` for accessibility
  - Desktop (≥1024px): flex row with description panel (320px sticky right)
  - Mobile (<1024px): flex column, description below, `max-width: 90vw`
  - Wide (≥1400px): container `max-width: 1600px`, description `width: 380px`

### FE-13: NavigationArrows Component

- **File:** `frontend/src/components/NavigationArrows.tsx`, `frontend/src/components/NavigationArrows.module.css`
- **Locked against:** COMPONENT_CONTRACT.md §2.8, DESIGN.md §5.7 (visual design)
- **Acceptance criteria:**
  - Props: `{ onPrev: () => void; onNext: () => void }`
  - Two buttons: left arrow (←) and right arrow (→)
  - Desktop: `opacity: 0` default, visible on hover over artwork area
  - Mobile (<768px): always visible `opacity: 0.7`
  - Focus-visible: always visible with glow
  - Touch target: 48×48px (desktop), 44×44px (mobile)
  - Glass background: `rgba(20, 27, 45, 0.6)`, `backdrop-filter: blur(8px)`
  - Hover: `background: rgba(168, 85, 247, 0.2)`, `border-color: var(--accent-purple)`
  - `aria-label="Navegación de obras"`, buttons `aria-label="Obra anterior/siguiente"`

### FE-14: Counter Component

- **File:** `frontend/src/components/Counter.tsx`, `frontend/src/components/Counter.module.css`
- **Locked against:** COMPONENT_CONTRACT.md §2.9, DESIGN.md §5.8 (visual design)
- **Acceptance criteria:**
  - Props: `{ current: number; total: number }` (1-based index)
  - Displays `"Obra X de Y"` format
  - Current number highlighted: `color: var(--text-accent)`, `font-weight: 600`
  - Centered, `font-size: 0.875rem`, `color: var(--text-muted)`, `letter-spacing: 0.05em`
  - `aria-live="polite"`, `aria-atomic="true"`

### FE-15: ArtworkDescription Component

- **File:** `frontend/src/components/ArtworkDescription.tsx`, `frontend/src/components/ArtworkDescription.module.css`
- **Locked against:** COMPONENT_CONTRACT.md §2.10, DESIGN.md §5.9 (visual design), DESIGN.md §14 (seed badge)
- **Acceptance criteria:**
  - Props: `{ image: ImageDetail; onLike: (id: number) => Promise<void> }`
  - State: `likes` (default `image.likes`), `isLiking` (boolean), `hasLiked` (boolean)
  - Displays: prompt (italic, left purple border), poetic description (if non-empty), relative date, like button, seed badge (if `is_seed`)
  - Relative date utility: "hace X minutos/horas/días" from `image.created_at`
  - Like button (pessimistic): calls `likeImage(image.id)`, on success `setLikes(response.likes)`, `setHasLiked(true)`, on error no UI change
  - Seed badge: `✦ {signature_hash}`, monospace font, 11px, `rgba(168, 85, 247, 0.08)` background
  - Desktop: sticky right panel, `width: 320px`, `max-height: 70vh`, `overflow-y: auto`
  - Mobile: `max-width: 480px`, centered, below artwork
  - Glass card composition
  - `role="region"`, `aria-label="Descripción de la obra"`
  - Like button: `aria-pressed={hasLiked}`, `aria-label="Me inspira. N likes"`

### FE-16: MiniGrid Component

- **File:** `frontend/src/components/MiniGrid.tsx`, `frontend/src/components/MiniGrid.module.css`
- **Locked against:** COMPONENT_CONTRACT.md §2.11, DESIGN.md §5.10 (visual design)
- **Acceptance criteria:**
  - Props: `{ images: ImageListItem[]; currentIndex: number; onSelect: (index: number) => void }`
  - Horizontal scrollable strip: `overflow-x: auto`, `scroll-behavior: smooth`
  - Items: 60×60px (desktop), 52×52px (mobile), `border-radius: var(--radius-sm)`
  - Current item: `border-color: var(--accent-purple)`, `box-shadow: 0 0 12px rgba(168, 85, 247, 0.4)`
  - Click: calls `onSelect(index)`, scrolls thumbnail into view (`scrollIntoView({ behavior: 'smooth', inline: 'center' })`)
  - Thin scrollbar: purple accent, 4px height
  - `role="listbox"`, items `role="option"`, `aria-selected`, `aria-current`
  - Images: `loading="lazy"`, `alt="Obra N: {prompt}"`

### FE-17: EmptyState Component

- **File:** `frontend/src/components/EmptyState.tsx`, `frontend/src/components/EmptyState.module.css`
- **Locked against:** COMPONENT_CONTRACT.md §2.12, DESIGN.md §5.11 (visual design)
- **Acceptance criteria:**
  - Props: `{ onGoToStudio: () => void }`
  - Centered vertically/horizontally, `min-height: 60vh`
  - Decorative icon: `font-size: 4rem`, `opacity: 0.3`
  - Title: `"Un lienzo en blanco"`, serif, `1.75rem`
  - Text: `"Esta galería está esperando su primera obra. Sé el artista."`
  - CTA button: `"Crear tu primera obra"`, `background: var(--accent-purple)`, hover glow
  - `role="status"`
  - Button hover: `background: #9333ea`, `box-shadow: 0 0 24px rgba(168, 85, 247, 0.4)`, `transform: translateY(-2px)`

### FE-18: Skeleton Loading Component

- **File:** `frontend/src/components/Skeleton.tsx`, `frontend/src/components/Skeleton.module.css`
- **Locked against:** DESIGN.md §5.12 (skeleton animation), §10.2 (variants)
- **Acceptance criteria:**
  - Props: `{ variant: 'image' | 'title' | 'text' | 'text-sm' | 'thumb' }`
  - Variants:
    - `image`: 100% width, 1:1 aspect ratio
    - `title`: 70% width, 1.5rem height
    - `text`: 80% width, 1rem height
    - `text-sm`: 60% width, 0.75rem height
    - `thumb`: 60×60px
  - Shimmer animation: `skeleton-shimmer` (1.5s, purple/cyan gradient)
  - `@media (prefers-reduced-motion: reduce)`: animation disabled, solid background

### FE-19: CSS Modules — All Components

- **Files:** All `*.module.css` files for components listed above
- **Locked against:** DESIGN.md (all visual specs), COMPONENT_CONTRACT.md (all component specs)
- **Acceptance criteria:**
  - Each component has its own CSS Module file
  - All glassmorphism effects use `backdrop-filter: blur()` with `-webkit-` prefix
  - All transitions use CSS custom properties (`--transition-fast`, `--transition-base`, etc.)
  - All hover states match DESIGN.md §8 specifications
  - All focus states match DESIGN.md §9 specifications
  - All responsive breakpoints match DESIGN.md §7 (768px, 1024px, 1400px)
  - `prefers-reduced-motion` respected in all animated components
  - Touch targets ≥ 44×44px on mobile
  - Color contrast ratios meet WCAG AA (verified against DESIGN.md §1.2)

### FE-20: Utility — Relative Date

- **File:** `frontend/src/utils/relativeDate.ts`
- **Locked against:** COMPONENT_CONTRACT.md §2.10 (relative date utility)
- **Acceptance criteria:**
  - Function `relativeDate(isoString: string): string`
  - Returns: "justo ahora" (<1min), "hace X minuto(s)" (<60min), "hace X hora(s)" (<24hr), "hace X día(s)" (≥24hr)
  - Uses `new Date(isoString)` and `new Date()` for comparison
  - Pluralization: adds "s" when count > 1

### FE-21: Skip Link Component

- **File:** `frontend/src/components/SkipLink.tsx`, `frontend/src/components/SkipLink.module.css`
- **Locked against:** DESIGN.md §13.3
- **Acceptance criteria:**
  - Skip link "Ir al contenido principal" visible on focus, jumps to main content, sr-only until focused
  - `position: fixed`, `top: 0`, `left: 0`, `z-index: 9999`
  - `background: var(--accent-purple)`, `color: white`, `padding: 12px 24px`
  - `:focus` makes it visible, `:not(:focus)` applies `.sr-only`
  - Click scrolls to `#main-content` or equivalent landmark

### FE-22: Autoplay Progress Bar

- **File:** `frontend/src/components/AutoplayProgressBar.tsx`, `frontend/src/components/AutoplayProgressBar.module.css`
- **Locked against:** DESIGN.md §11.1, §11.2
- **Acceptance criteria:**
  - Visible when `isActive && !isPaused`, gradient purple→cyan, shows time remaining per artwork, pause indicator when paused
  - `position: fixed`, `bottom: 0`, `left: 0`, `width: 100%`, `height: 3px`
  - Gradient: `linear-gradient(90deg, var(--accent-purple), var(--accent-cyan))`
  - Animates from `width: 0%` to `width: 100%` over 4s (matching autoplay interval)
  - When paused: bar freezes, subtle opacity change to indicate paused state
  - `@media (prefers-reduced-motion: reduce)`: no animation, solid color

### FE-23: Theatrical Transition Color Wash Overlay

- **File:** `frontend/src/components/TransitionOverlay.tsx`, `frontend/src/components/TransitionOverlay.module.css`
- **Locked against:** DESIGN.md §6.2
- **Acceptance criteria:**
  - Full-screen overlay during mode toggle, radial gradient purple wash, fade + zoom (scale 0.97→1.0), 500ms, respects prefers-reduced-motion
  - `position: fixed`, `inset: 0`, `z-index: 200`, `pointer-events: none`
  - Background: `radial-gradient(ellipse at center, rgba(168, 85, 247, 0.3), rgba(10, 10, 20, 0.9))`
  - Animation phases: exit 150ms (fade out) → switch mode → enter 300ms (fade in + scale 0.97→1.0)
  - `@media (prefers-reduced-motion: reduce)`: instant switch, no overlay

### FE-24: Micro-interactions

- **File:** `frontend/src/components/MicroInteractions.tsx` (or add to existing components)
- **Locked against:** DESIGN.md §12.2
- **Acceptance criteria:**
  - Heart scale animation on like (0.8s): `transform: scale(1) → scale(1.3) → scale(1)` with `ease-out`
  - Green flash on save (0.5s): brief `background: rgba(52, 211, 153, 0.2)` overlay on PreviewCard
  - Subtle particle effect on seed badge hover: small purple dots floating upward, CSS-only with `::before`/`::after` pseudo-elements
  - All animations respect `prefers-reduced-motion`

---

## QA Tasks

### QA-01: Test Framework Setup

- **File:** `vitest.config.ts`, `package.json` (test scripts), test utilities
- **Locked against:** ADR-001 (testing with Vitest)
- **Acceptance criteria:**
  - Vitest installed as dev dependency
  - `vitest.config.ts` configured for both frontend and backend test discovery
  - `@testing-library/react` and `@testing-library/jest-dom` installed for frontend tests
  - `jsdom` environment configured for frontend tests
  - Test scripts: `"test": "vitest run"`, `"test:watch": "vitest"`, `"test:coverage": "vitest run --coverage"`
  - Test directory structure: `backend/src/**/*.test.ts`, `frontend/src/**/*.test.tsx`

### QA-02: Backend API Tests — GET /api/images

- **File:** `backend/src/routes/images.test.ts` (GET tests)
- **Locked against:** API_CONTRACT.md §1.1
- **Acceptance criteria:**
  - Returns 200 with array of `ImageListItem` objects
  - Array ordered by `created_at DESC` (newest first)
  - Response does NOT include `description` field
  - Returns empty array `[]` when no images exist
  - Returns 500 on database connection failure
  - Each item has correct shape: `{ id, prompt, image_url, created_at, likes, is_seed }`
  - `is_seed` is boolean, `created_at` is ISO 8601 string

### QA-03: Backend API Tests — POST /api/images

- **File:** `backend/src/routes/images.test.ts` (POST tests)
- **Locked against:** API_CONTRACT.md §1.2, §3.1 (validation)
- **Acceptance criteria:**
  - Returns 201 with created `ImageListItem` on valid prompt
  - Returns 400 with specific error message for: missing prompt, non-string prompt, empty prompt, >500 chars
  - Returns 502 when both Pollinations and HuggingFace fail
  - Returns 500 on unexpected server error
  - Prompt is trimmed before validation and storage
  - Response does NOT include `description` field
  - `is_seed` is `false` for user-generated images

### QA-04: Backend API Tests — GET /api/images/:id

- **File:** `backend/src/routes/images.test.ts` (GET single tests)
- **Locked against:** API_CONTRACT.md §1.3
- **Acceptance criteria:**
  - Returns 200 with `ImageDetail` for valid existing ID
  - Response includes `description` field (may be empty string)
  - Response includes `signature_hash` field (string or null)
  - Returns 404 for non-existent ID
  - Returns 404 for non-integer ID (e.g., "abc", "1.5")
  - Returns 500 on database error

### QA-05: Backend API Tests — PATCH /api/images/:id/like

- **File:** `backend/src/routes/images.test.ts` (PATCH tests)
- **Locked against:** API_CONTRACT.md §1.4
- **Acceptance criteria:**
  - Returns 200 with `{ likes: <incremented_count> }`
  - Like count increments by exactly 1 per call
  - Multiple calls increment multiple times (no duplicate prevention)
  - Returns 404 for non-existent ID
  - Returns 404 for non-integer ID
  - Returns 500 on database error
  - No auth required (anonymous access)

### QA-06: Backend Integration Tests — Image Generation Flow

- **File:** `backend/src/lib/pollinations.test.ts`, `backend/src/lib/huggingface.test.ts`, `backend/src/lib/description.test.ts`
- **Locked against:** API_CONTRACT.md §5 (flow), ADR-004, ADR-005, ADR-008
- **Acceptance criteria:**
  - Pollinations: correct URL construction, 30s timeout, retry on failure
  - HuggingFace: correct POST request, binary response handling, Supabase Storage upload
  - Description: correct URL construction, 15s timeout, non-blocking behavior
  - Fallback chain: Pollinations fails → HuggingFace attempted → 502 if both fail
  - Supabase Storage upload: correct bucket, filename generation, public URL retrieval

### QA-07: Frontend Component Tests — Render Tests

- **File:** `frontend/src/components/*.test.tsx` (render tests for all components)
- **Locked against:** COMPONENT_CONTRACT.md (all component specs)
- **Acceptance criteria:**
  - `ModeToggle`: renders two tabs, correct labels, aria-selected state
  - `StudioView`: renders GeneratePanel, renders PreviewCard when previewUrl set
  - `GeneratePanel`: renders input with placeholder, renders submit button, disabled state during loading
  - `PreviewCard`: renders image, renders save/discard buttons, entry animation
  - `GalleryView`: renders ArtworkDisplay, NavigationArrows, Counter, ArtworkDescription, MiniGrid
  - `ArtworkDisplay`: renders image with correct alt text
  - `Counter`: displays "Obra X de Y" format
  - `ArtworkDescription`: renders prompt, description (if present), date, like button, seed badge (if seed)
  - `MiniGrid`: renders thumbnail strip, current item highlighted
  - `EmptyState`: renders message, renders CTA button
  - `Skeleton`: renders correct variant shapes

### QA-08: Frontend Component Tests — Interaction Tests

- **File:** `frontend/src/components/*.test.tsx` (interaction tests)
- **Locked against:** COMPONENT_CONTRACT.md (event handlers, state management)
- **Acceptance criteria:**
  - `ModeToggle`: click switches mode, calls `onToggle` callback
  - `GeneratePanel`: Enter key submits form, Escape clears input, disabled during loading
  - `PreviewCard`: save button calls `onSave`, discard button calls `onDiscard`
  - `NavigationArrows`: prev/next buttons call respective handlers
  - `MiniGrid`: click on thumbnail calls `onSelect` with correct index
  - `ArtworkDescription`: like button calls `onLike` with correct ID
  - `EmptyState`: CTA button calls `onGoToStudio`
  - Keyboard navigation: ArrowLeft/Right/Home/End in GalleryView

### QA-09: Integration Tests — Frontend ↔ Backend Contracts

- **File:** `tests/integration/api-contracts.test.ts`
- **Locked against:** API_CONTRACT.md (all endpoints), COMPONENT_CONTRACT.md §3 (data flow)
- **Acceptance criteria:**
  - Full flow: POST image → GET list includes new image → GET single returns detail
  - Frontend API client correctly parses backend responses
  - Type shapes match between frontend types and backend responses
  - Error responses correctly parsed by frontend (error message extraction)
  - Like flow: PATCH → GET single reflects updated like count
  - Seed data: GET list returns seed artworks with `is_seed: true`

### QA-10: Accessibility Audit — WCAG AA

- **File:** `tests/a11y/wcag-audit.md`
- **Locked against:** DESIGN.md §13 (WCAG AA checklist), COMPONENT_CONTRACT.md §6 (accessibility requirements)
- **Acceptance criteria:**
  - Color contrast ratio ≥ 4.5:1 for all normal text (verified against DESIGN.md §1.2)
  - Color contrast ratio ≥ 3:1 for all large text/headings
  - Focus indicators visible on ALL interactive elements (3px purple ring)
  - Touch targets ≥ 44×44px on mobile
  - Keyboard navigation works for all interactive elements
  - Screen reader announcements present for: mode change, artwork navigation, like action, generation states, errors
  - `prefers-reduced-motion` disables all animations
  - Semantic HTML: proper heading hierarchy, landmarks, ARIA attributes
  - Alt text on all images (prompt text for generated art)
  - Skip link present and functional
  - ARIA attributes match COMPONENT_CONTRACT.md §6.4 table

### QA-11: Responsive Tests

- **File:** `tests/responsive/responsive-audit.md`
- **Locked against:** DESIGN.md §7 (responsive breakpoints), COMPONENT_CONTRACT.md §7 (responsive behavior)
- **Acceptance criteria:**
  - Desktop (≥1024px): ModeToggle centered, ArtworkDisplay flex row, description sticky right panel (320px), navigation arrows hover-visible, MiniGrid 60×60px, full blur(12px)
  - Mobile (<1024px): ModeToggle top-right, ArtworkDisplay flex column, description below, navigation arrows always visible (opacity 0.7), MiniGrid 52×52px, reduced blur(8px), touch swipe navigation
  - Wide (≥1400px): container max-width 1600px, description panel 380px
  - Tablet (769-1023px): intermediate layout adjustments
  - All breakpoints tested: 320px, 768px, 1024px, 1400px, 1920px

---

## Dependencies

```
Phase 1: Foundation (can start in parallel)
├── BE-01 (Project Setup) ──────────────────────────────────────────┐
├── FE-01 (Project Setup) ──────────────────────────────────────────┤
├── FE-02 (Entry + Global Styles) ──────────────────────────────────┤
├── FE-03 (TypeScript Types) ───────────────────────────────────────┤
├── QA-01 (Test Framework Setup) ───────────────────────────────────┘

Phase 2: Core Infrastructure (depends on Phase 1)
├── BE-02 (Database Connection) ───────────────────── depends on BE-01
├── BE-03 (Seed Data Loading) ─────────────────────── depends on BE-02
├── BE-08 (Error Middleware) ──────────────────────── depends on BE-01
├── BE-09 (CORS Configuration) ────────────────────── depends on BE-01
├── FE-04 (API Client) ────────────────────────────── depends on FE-03
├── FE-05 (AutoplayContext) ───────────────────────── depends on FE-03
├── FE-20 (Relative Date Utility) ─────────────────── depends on FE-03

Phase 3: Endpoints + Components (depends on Phase 2)
├── BE-04 (GET /api/images) ───────────────────────── depends on BE-02
├── BE-05 (POST /api/images) ──────────────────────── depends on BE-02, BE-03
├── BE-06 (GET /api/images/:id) ───────────────────── depends on BE-02
├── BE-07 (PATCH /api/images/:id/like) ────────────── depends on BE-02
├── FE-06 (App.tsx) ───────────────────────────────── depends on FE-04, FE-05
├── FE-07 (ModeToggle) ────────────────────────────── depends on FE-02
├── FE-18 (Skeleton) ──────────────────────────────── depends on FE-02
├── FE-19 (CSS Modules) ───────────────────────────── depends on FE-02

Phase 4: Views + Interactions (depends on Phase 3)
├── FE-08 (StudioView) ────────────────────────────── depends on FE-06, FE-09, FE-10
├── FE-09 (GeneratePanel) ─────────────────────────── depends on FE-04
├── FE-10 (PreviewCard) ───────────────────────────── depends on FE-02
├── FE-11 (GalleryView) ───────────────────────────── depends on FE-06, FE-12, FE-13, FE-14, FE-15, FE-16
├── FE-12 (ArtworkDisplay) ────────────────────────── depends on FE-02
├── FE-13 (NavigationArrows) ──────────────────────── depends on FE-02
├── FE-14 (Counter) ───────────────────────────────── depends on FE-02
├── FE-15 (ArtworkDescription) ────────────────────── depends on FE-04, FE-20
├── FE-16 (MiniGrid) ──────────────────────────────── depends on FE-02
├── FE-17 (EmptyState) ────────────────────────────── depends on FE-02
├── FE-21 (SkipLink) ──────────────────────────────── depends on FE-02
├── FE-22 (AutoplayProgressBar) ───────────────────── depends on FE-05
├── FE-23 (TransitionOverlay) ─────────────────────── depends on FE-06
├── FE-24 (MicroInteractions) ─────────────────────── depends on FE-10, FE-15

Phase 5: Testing (depends on Phase 3-4)
├── QA-02 (GET list tests) ────────────────────────── depends on BE-04
├── QA-03 (POST tests) ────────────────────────────── depends on BE-05
├── QA-04 (GET single tests) ──────────────────────── depends on BE-06
├── QA-05 (PATCH like tests) ──────────────────────── depends on BE-07
├── QA-06 (Image generation flow tests) ───────────── depends on BE-05
├── QA-07 (Frontend render tests) ─────────────────── depends on FE-07 through FE-17
├── QA-08 (Frontend interaction tests) ────────────── depends on FE-07 through FE-17
├── QA-09 (Integration tests) ─────────────────────── depends on all BE + FE endpoints
├── QA-10 (Accessibility audit) ───────────────────── depends on all FE components
├── QA-11 (Responsive tests) ──────────────────────── depends on all FE components
```

---

## Parallel Execution Plan

### Wave 1 — Foundation (Day 1, all parallel)
| Agent | Tasks | Duration |
|-------|-------|----------|
| **BACKEND** | BE-01, BE-08, BE-09 | 1h |
| **FRONTEND** | FE-01, FE-02, FE-03, FE-20 | 1.5h |
| **QA** | QA-01 | 0.5h |

### Wave 2 — Infrastructure (Day 1-2, parallel BE ↔ FE)
| Agent | Tasks | Duration | Dependencies |
|-------|-------|----------|-------------|
| **BACKEND** | BE-02, BE-03 | 2h | BE-01 |
| **FRONTEND** | FE-04, FE-05, FE-18, FE-19 (partial) | 2h | FE-01, FE-02, FE-03 |
| **QA** | QA-02 (write tests, run when BE-04 ready) | 1h | QA-01 |

### Wave 3 — Endpoints + Core Components (Day 2-3, parallel BE ↔ FE)
| Agent | Tasks | Duration | Dependencies |
|-------|-------|----------|-------------|
| **BACKEND** | BE-04, BE-05, BE-06, BE-07 | 4h | BE-02, BE-03 |
| **FRONTEND** | FE-06, FE-07, FE-09, FE-10, FE-12, FE-13, FE-14, FE-15, FE-16, FE-17, FE-19 (complete), FE-21, FE-23 | 6h | FE-04, FE-05, FE-02 |
| **QA** | QA-03, QA-04, QA-05, QA-06 | 3h | BE-04 through BE-07 |

### Wave 4 — Views + Integration (Day 3-4, parallel FE + QA)
| Agent | Tasks | Duration | Dependencies |
|-------|-------|----------|-------------|
| **FRONTEND** | FE-08 (StudioView), FE-11 (GalleryView), FE-22 (AutoplayProgressBar), FE-24 (MicroInteractions) | 3.5h | FE-09, FE-10, FE-12-FE-16, FE-05 |
| **QA** | QA-07, QA-08, QA-09 | 4h | All FE components, all BE endpoints |

### Wave 5 — Audit + Polish (Day 4-5, parallel)
| Agent | Tasks | Duration | Dependencies |
|-------|-------|----------|-------------|
| **QA** | QA-10 (WCAG audit), QA-11 (responsive audit) | 3h | All FE components complete |
| **BACKEND** | Bug fixes from QA feedback | As needed | QA test results |
| **FRONTEND** | Bug fixes from QA feedback | As needed | QA test results |

---

## Acceptance Criteria — Sprint Definition of Done

- [ ] All 4 REST endpoints implemented and passing tests (QA-02 through QA-06)
- [ ] All 18 frontend components implemented and passing render + interaction tests (QA-07, QA-08)
- [ ] Frontend ↔ Backend contracts verified (QA-09)
- [ ] WCAG AA accessibility audit passed (QA-10) — includes skip link (FE-21)
- [ ] Responsive design verified at all breakpoints (QA-11)
- [ ] Seed data loads correctly on first startup (BE-03)
- [ ] Image generation flow works: Pollinations primary → HuggingFace fallback (BE-05)
- [ ] Non-blocking description generation works (BE-05, ADR-005)
- [ ] Autoplay works: 5s inactivity → 4s interval → pauses on Studio switch (FE-05, ADR-010)
- [ ] Autoplay progress bar visible and functional (FE-22)
- [ ] Theatrical mode toggle works with color wash transition (FE-06, FE-07, FE-23)
- [ ] Micro-interactions active: heart scale, green flash, seed badge particles (FE-24)
- [ ] CORS configured for production only (BE-09, ADR-007)
- [ ] Error handling returns consistent `{ error: string }` format (BE-08)
- [ ] `npm run dev` starts both frontend (port 5173) and backend (port 3001) with hot reload
- [ ] `npm run build` produces production-ready frontend build
- [ ] `npm run seed` loads 5 seed artworks
- [ ] `npm test` runs all tests with passing results

---

## Task Summary

| Agent | Tasks | Count | Estimated Hours |
|-------|-------|-------|----------------|
| **BACKEND** | BE-01 through BE-09 | 9 | ~10h |
| **FRONTEND** | FE-01 through FE-24 | 24 | ~19h |
| **QA** | QA-01 through QA-11 | 11 | ~12h |
| **TOTAL** | | **44** | **~41h** |

---

## Spec Lock References

Every task is locked against a specific spec document. Agents must NOT deviate from these contracts without explicit approval:

| Contract | Locked Sections |
|----------|----------------|
| **API_CONTRACT.md** | §1.1-1.4 (endpoints), §2 (data shapes), §3 (validation), §4 (errors), §5 (image flow), §6 (schema), §7 (CORS), §8 (server config), §9 (env vars) |
| **COMPONENT_CONTRACT.md** | §1 (types), §2.1-2.12 (all components), §3 (data flow), §4 (state), §5 (events), §6 (a11y), §7 (responsive), §8 (loading), §9 (errors), §10 (API client), §11 (file structure) |
| **DESIGN.md** | §1 (colors), §2 (typography), §3 (spacing), §4 (glassmorphism), §5.1-5.12 (component visuals), §6 (theatrical transition), §7 (responsive), §8 (hover), §9 (focus), §10 (loading), §11 (autoplay), §12 (micro-interactions), §13 (a11y), §14 (seed badge), §15 (CSS reset), §16 (fonts) |
| **ADR-001** | Stack: React 19 + Vite 6 + TS / Express 4 + TS + tsx |
| **ADR-002** | Database: Supabase PostgreSQL via `postgres` |
| **ADR-003** | API: REST with 4 endpoints |
| **ADR-004** | Image API: Pollinations primary + HuggingFace fallback |
| **ADR-005** | Text API: Pollinations text, non-blocking, 15s timeout |
| **ADR-006** | Auth: No authentication |
| **ADR-007** | Dev setup: Vite proxy, port 5173/3001, CORS prod only |
| **ADR-008** | Storage: URL-only for Pollinations, Supabase Storage for fallback |
| **ADR-009** | Seed: JSON file, 5 artworks, is_seed + signature_hash |
| **ADR-010** | Autoplay: Context + useReducer, 5s inactivity, 4s interval |
