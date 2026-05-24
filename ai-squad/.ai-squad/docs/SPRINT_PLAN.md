# SPRINT PLAN — Imaginarium MVP

**Project:** experimento-b7-imaginarium
**Date:** 2026-05-22
**Total Tasks:** 44 (9 BE + 24 FE + 11 QA)
**Total Estimated Hours:** ~41h
**Sprints:** 4 (2-3 days each)

---

## SPRINT 1: Foundation

**Objective:** Establish project scaffolding, type system, global styles, database schema, and test framework so all subsequent work has a stable base.

**Duration:** 2 days

### Tickets

| ID | Title | Agent | Hours | Dependencies | Acceptance Criteria | Locked Spec |
|----|-------|-------|-------|-------------|---------------------|-------------|
| **S1-BE-01** | Backend Project Setup — Express + TS + tsx | BE-Agent | 1h | None | `package.json` with all deps, `tsconfig.json` (ES2020, ESNext, bundler), `.env.example` with 7 vars, `src/index.ts` listens on PORT\|3001, `npm run dev` starts with hot reload | ADR-001, ADR-007 |
| **S1-FE-01** | Frontend Project Setup — Vite + React 19 + TS | FE-Agent-A | 1h | None | `package.json` with React 19/Vite 6 deps, `tsconfig.json` (ES2020, react-jsx), `vite.config.ts` with `/api` proxy to 3001, `index.html` with `#root` + Google Fonts import, `npm run dev` on 5173 | ADR-001, ADR-007 |
| **S1-FE-02** | Entry Point + Global Styles | FE-Agent-B | 1.5h | None | `main.tsx` with `createRoot` + StrictMode, `index.css` with all CSS custom properties (DESIGN.md §1.7), CSS reset (§15), Google Fonts (§16), `.sr-only`, `:focus-visible`, `prefers-reduced-motion`, heading styles (§2.6), glassmorphism base classes (§4.1), skeleton shimmer (§5.12), `@supports` fallbacks | DESIGN.md §1.7, §2.6, §4.1, §15, §16 |
| **S1-FE-03** | TypeScript Types | FE-Agent-C | 0.5h | None | `types/index.ts` exports: `ImageListItem`, `ImageDetail extends ImageListItem`, `ImageCreate`, `LikeResponse`, `ErrorResponse`, `Mode`, `AutoplayState`, `AutoplayAction` union, `FetchState` — all 9 types | COMPONENT_CONTRACT.md §1, API_CONTRACT.md §2 |
| **S1-FE-20** | Relative Date Utility | FE-Agent-C | 0.5h | S1-FE-03 | `relativeDate(isoString)` returns "justo ahora"/"hace X minuto(s)"/"hace X hora(s)"/"hace X día(s)" with correct pluralization | COMPONENT_CONTRACT.md §2.10 |
| **S1-BE-02** | Database Connection Module | BE-Agent | 1.5h | S1-BE-01 | `db.ts` exports `postgres` client from `DATABASE_URL`, `initSchema()` creates `images` table with all 8 columns + `idx_images_created_at` index, idempotent `ALTER TABLE IF NOT EXISTS` for `is_seed`/`signature_hash`, connection test on startup | ADR-002, API_CONTRACT.md §6 |
| **S1-BE-03** | Seed Data Loading | BE-Agent | 1h | S1-BE-02 | `seed/artworks.json` with 5 curated artworks (real Pollinations URLs, poetic Spanish descriptions), `seed/load.ts` reads JSON, generates 8-char hex `signature_hash`, checks `COUNT(*)`, inserts if empty (idempotent), runnable via `npm run seed` | ADR-009 |
| **S1-QA-01** | Test Framework Setup | QA-Agent | 0.5h | None | Vitest installed, `vitest.config.ts` for FE+BE discovery, `@testing-library/react` + `@testing-library/jest-dom` + `jsdom` for FE, scripts: `test`, `test:watch`, `test:coverage`, directory structure `backend/src/**/*.test.ts`, `frontend/src/**/*.test.tsx` | ADR-001 |

### Parallel Opportunities — Sprint 1

**Wave 1A (Day 1, all start simultaneously — 5 agents):**
| Agent | Ticket | Duration |
|-------|--------|----------|
| BE-Agent | S1-BE-01 | 1h |
| FE-Agent-A | S1-FE-01 | 1h |
| FE-Agent-B | S1-FE-02 | 1.5h |
| FE-Agent-C | S1-FE-03 | 0.5h |
| QA-Agent | S1-QA-01 | 0.5h |

**Wave 1B (Day 1, after Wave 1A completes):**
| Agent | Ticket | Depends On | Duration |
|-------|--------|-----------|----------|
| FE-Agent-C | S1-FE-20 | S1-FE-03 | 0.5h |
| BE-Agent | S1-BE-02 | S1-BE-01 | 1.5h |

**Wave 1C (Day 2, after Wave 1B completes):**
| Agent | Ticket | Depends On | Duration |
|-------|--------|-----------|----------|
| BE-Agent | S1-BE-03 | S1-BE-02 | 1h |

**Max parallel agents in Sprint 1:** 5 (Wave 1A)
**Critical path:** S1-BE-01 → S1-BE-02 → S1-BE-03 (3.5h)

---

## SPRINT 2: Core Infrastructure

**Objective:** Wire up the backend API endpoints, build the frontend API client and state management layer, and configure cross-cutting concerns (CORS, error handling).

**Duration:** 2-3 days

### Tickets

| ID | Title | Agent | Hours | Dependencies | Acceptance Criteria | Locked Spec |
|----|-------|-------|-------|-------------|---------------------|-------------|
| **S2-BE-08** | Error Handling Middleware | BE-Agent-A | 0.5h | S1-BE-01 | `(err, _req, res, _next)` returns 500 with `{ error: "Error interno..." }`, logs with `console.error`, sets `Content-Type: application/json`, mounted after routes in `index.ts` | API_CONTRACT.md §4, §8.1 |
| **S2-BE-09** | CORS Configuration | BE-Agent-A | 0.5h | S1-BE-01 | Dev: NO CORS middleware (Vite proxy), Prod: `cors({ origin: FRONTEND_URL })`, `cors` package imported, `FRONTEND_URL` required in prod | API_CONTRACT.md §7, ADR-007 |
| **S2-BE-04** | GET /api/images Endpoint | BE-Agent-B | 1.5h | S1-BE-02 | Returns `ImageListItem[]` ordered `created_at DESC`, NO `description` field, empty array if none, ISO 8601 dates, boolean `is_seed`, 500 on DB error with Spanish message, `try/catch` + `next(err)` pattern | API_CONTRACT.md §1.1, ADR-003 |
| **S2-BE-06** | GET /api/images/:id Endpoint | BE-Agent-C | 1h | S1-BE-02 | Parses `:id` as integer, non-integer → 404, `SELECT * FROM images WHERE id = $1`, no row → 404, returns `ImageDetail` with `description` + `signature_hash`, 500 on DB error | API_CONTRACT.md §1.3 |
| **S2-BE-07** | PATCH /api/images/:id/like Endpoint | BE-Agent-C | 1h | S1-BE-02 | Parses `:id` as integer, non-integer → 404, `UPDATE images SET likes = likes + 1 WHERE id = $1 RETURNING likes`, no row → 404, returns `{ likes: <new> }`, no auth, no duplicate prevention, 500 on DB error | API_CONTRACT.md §1.4, ADR-006 |
| **S2-BE-05** | POST /api/images Endpoint + Image Generation | BE-Agent-D | 3h | S1-BE-02, S1-BE-03 | Validation (4 rules: missing, type, empty, >500 chars → 400), Pollinations primary (30s timeout, 1 retry), HuggingFace fallback (30s, Supabase Storage upload), save to DB, return 201 `ImageListItem`, async description (fire-and-forget, 15s timeout), 502 if both fail | API_CONTRACT.md §1.2, §5, ADR-004, ADR-005, ADR-008 |
| **S2-FE-04** | API Client Module | FE-Agent-A | 1h | S1-FE-03 | `fetchImages()`, `fetchImageDetail(id)`, `createImage(prompt)`, `likeImage(id)` — all use native `fetch`, `BASE_URL = '/api'`, throw on `!res.ok`, extract error message from `{ error }` response | COMPONENT_CONTRACT.md §10, API_CONTRACT.md |
| **S2-FE-05** | AutoplayContext | FE-Agent-B | 2h | S1-FE-03 | `AutoplayContext` + `AutoplayProvider`, `useReducer` with state `{ isActive, isPaused, currentIndex, inactivityTimer }`, handles TICK/RESET_INACTIVITY/PAUSE/RESUME/NEXT/SET_INDEX, `setInterval` (4s), `setTimeout` (5s inactivity), `visibilitychange` listener, `useAutoplay()` hook, cleanup on unmount | ADR-010, COMPONENT_CONTRACT.md §4.4 |
| **S2-FE-18** | Skeleton Loading Component | FE-Agent-C | 0.5h | S1-FE-02 | `Skeleton` with variants: `image`, `title`, `text`, `text-sm`, `thumb` — correct dimensions, shimmer animation (1.5s purple/cyan gradient), `prefers-reduced-motion` disables animation | DESIGN.md §5.12, §10.2 |
| **S2-FE-21** | Skip Link Component | FE-Agent-C | 0.5h | S1-FE-02 | "Ir al contenido principal", visible on focus, `position: fixed`, `z-index: 9999`, purple background, `.sr-only` when not focused, scrolls to main content | DESIGN.md §13.3 |

### Parallel Opportunities — Sprint 2

**Wave 2A (Day 1, all start simultaneously — 5 agents):**
| Agent | Ticket | Depends On | Duration |
|-------|--------|-----------|----------|
| BE-Agent-A | S2-BE-08 | S1-BE-01 | 0.5h |
| BE-Agent-A | S2-BE-09 | S1-BE-01 | 0.5h |
| BE-Agent-B | S2-BE-04 | S1-BE-02 | 1.5h |
| BE-Agent-C | S2-BE-06 | S1-BE-02 | 1h |
| BE-Agent-C | S2-BE-07 | S1-BE-02 | 1h |

**Wave 2B (Day 1-2, parallel with Wave 2A — 3 agents):**
| Agent | Ticket | Depends On | Duration |
|-------|--------|-----------|----------|
| BE-Agent-D | S2-BE-05 | S1-BE-02, S1-BE-03 | 3h |
| FE-Agent-A | S2-FE-04 | S1-FE-03 | 1h |
| FE-Agent-B | S2-FE-05 | S1-FE-03 | 2h |

**Wave 2C (Day 2, after Wave 2B — 1 agent):**
| Agent | Ticket | Depends On | Duration |
|-------|--------|-----------|----------|
| FE-Agent-C | S2-FE-18 | S1-FE-02 | 0.5h |
| FE-Agent-C | S2-FE-21 | S1-FE-02 | 0.5h |

**Max parallel agents in Sprint 2:** 5 (Wave 2A + Wave 2B simultaneously)
**Critical path:** S1-BE-02 → S2-BE-05 (3h) — longest single ticket

---

## SPRINT 3: Views + Interactions

**Objective:** Implement all 18 frontend UI components, the root App orchestration, mode toggle with theatrical transitions, autoplay integration, and micro-interactions.

**Duration:** 3 days

### Tickets

| ID | Title | Agent | Hours | Dependencies | Acceptance Criteria | Locked Spec |
|----|-------|-------|-------|-------------|---------------------|-------------|
| **S3-FE-07** | ModeToggle Component | FE-Agent-A | 1h | S1-FE-02 | Two buttons "Estudio"/"Galería", `role="tablist"`/`role="tab"`, `aria-selected`, active state (purple bg, accent text), fixed position (centered desktop, top-right mobile), glassmorphism bg, focus-visible, keyboard Tab/Enter/Space | COMPONENT_CONTRACT.md §2.2, DESIGN.md §5.1, §13.2 |
| **S3-FE-10** | PreviewCard Component | FE-Agent-A | 1h | S1-FE-02 | Image 1:1 aspect ratio, max-width 512px, "Guardar en galería" (green) + "Descartar" (red) buttons, `fadeInScale` entry animation (300ms), glass card, `role="region"`, buttons disabled while `isSaving` | COMPONENT_CONTRACT.md §2.5, DESIGN.md §5.4 |
| **S3-FE-12** | ArtworkDisplay Component | FE-Agent-A | 1h | S1-FE-02 | Image centered, `max-height: 80vh` desktop / `55vh` mobile, `object-fit: contain`, hover purple glow, `alt={image.prompt}`, flex row desktop (description 320px sticky right), flex column mobile, wide ≥1400px (1600px container, 380px description) | COMPONENT_CONTRACT.md §2.7, DESIGN.md §5.6, §7 |
| **S3-FE-13** | NavigationArrows Component | FE-Agent-A | 0.5h | S1-FE-02 | Left/right arrow buttons, desktop: `opacity: 0` default visible on hover, mobile: always visible `opacity: 0.7`, focus-visible always visible, 48×48px desktop / 44×44px mobile, glass bg, hover purple, `aria-label="Navegación de obras"` | COMPONENT_CONTRACT.md §2.8, DESIGN.md §5.7 |
| **S3-FE-14** | Counter Component | FE-Agent-A | 0.5h | S1-FE-02 | "Obra X de Y" format, current number highlighted (accent color, weight 600), centered, 0.875rem, muted color, `aria-live="polite"`, `aria-atomic="true"` | COMPONENT_CONTRACT.md §2.9, DESIGN.md §5.8 |
| **S3-FE-16** | MiniGrid Component | FE-Agent-A | 1h | S1-FE-02 | Horizontal scrollable strip, 60×60px desktop / 52×52px mobile, current item purple border + glow, click → `onSelect(index)` + `scrollIntoView`, thin purple scrollbar, `role="listbox"`/`role="option"`, `aria-selected`, `aria-current`, lazy loading images | COMPONENT_CONTRACT.md §2.11, DESIGN.md §5.10 |
| **S3-FE-17** | EmptyState Component | FE-Agent-A | 0.5h | S1-FE-02 | Centered, `min-height: 60vh`, decorative icon (4rem, 0.3 opacity), title "Un lienzo en blanco" (serif, 1.75rem), text, CTA button "Crear tu primera obra" (purple, hover glow), `role="status"` | COMPONENT_CONTRACT.md §2.12, DESIGN.md §5.11 |
| **S3-FE-09** | GeneratePanel Component | FE-Agent-B | 1.5h | S2-FE-04 | Text input with placeholder, submit button inside input (absolute right), form submission trims + validates, loading state (disabled input/button, spinner, rotating messages every 2s), input styling (glass, rounded full, focus purple), `role="search"`, Enter submits, Escape clears | COMPONENT_CONTRACT.md §2.4, DESIGN.md §5.3 |
| **S3-FE-15** | ArtworkDescription Component | FE-Agent-B | 2h | S2-FE-04, S1-FE-20 | Displays: prompt (italic, purple left border), poetic description (if non-empty), relative date, like button (pessimistic update), seed badge (if `is_seed`), sticky right panel desktop (320px), below mobile (max-width 480px), glass card, `role="region"`, like button `aria-pressed` | COMPONENT_CONTRACT.md §2.10, DESIGN.md §5.9, §14 |
| **S3-FE-22** | Autoplay Progress Bar | FE-Agent-B | 0.5h | S2-FE-05 | Visible when `isActive && !isPaused`, gradient purple→cyan, `position: fixed` bottom, 3px height, animates 0%→100% over 4s, freezes when paused, `prefers-reduced-motion` disables animation | DESIGN.md §11.1, §11.2 |
| **S3-FE-23** | Transition Overlay | FE-Agent-B | 0.5h | S1-FE-06 | Full-screen overlay, radial gradient purple wash, `position: fixed` inset 0, z-index 200, animation phases: exit 150ms → switch → enter 300ms (scale 0.97→1.0), `prefers-reduced-motion` instant switch | DESIGN.md §6.2 |
| **S3-FE-24** | Micro-interactions | FE-Agent-B | 0.5h | S3-FE-10, S3-FE-15 | Heart scale animation on like (0.8s, scale 1→1.3→1), green flash on save (0.5s), seed badge particle effect on hover (CSS `::before`/`::after`), all respect `prefers-reduced-motion` | DESIGN.md §12.2 |
| **S3-FE-06** | App.tsx — Root Component | FE-Agent-C | 2h | S2-FE-04, S2-FE-05 | State: mode, images, fetchState, fetchError, isTransitioning, transitionPhase. On mount: fetchImages(). Refetch callback. Force studio if no images + gallery mode. Theatrical toggle handler (exit 150ms → switch → enter 300ms). Renders ModeToggle + StudioView/EmptyState/GalleryView conditionally. `AutoplayProvider` wraps all. Screen reader announcements. Skip link. | COMPONENT_CONTRACT.md §2.1, API_CONTRACT.md §1.1 |
| **S3-FE-08** | StudioView Component | FE-Agent-C | 1.5h | S3-FE-06, S3-FE-09, S3-FE-10 | State: previewUrl, isGenerating, generationError. Renders GeneratePanel + PreviewCard (when previewUrl set). handleSubmit calls `createImage()`, handles 201/400/500/502 errors. handleSave calls `onImageSaved()` + clears preview. handleDiscard clears preview. Layout: max-width 640px, centered. `role="tabpanel"`, error `role="alert"`, SR announcements | COMPONENT_CONTRACT.md §2.3, DESIGN.md §5.2 |
| **S3-FE-11** | GalleryView Component | FE-Agent-C | 2.5h | S3-FE-06, S3-FE-12, S3-FE-13, S3-FE-14, S3-FE-15, S3-FE-16 | State: currentIndex, detailImage, detailLoading, detailError. Fetches detail on mount/currentIndex change. Autoplay integration (consumes AutoplayContext, dispatches RESET_INACTIVITY). Circular navigation. Keyboard (ArrowRight/Left/Home/End). Touch swipe (>50px). Renders ArtworkDisplay + NavigationArrows + Counter + ArtworkDescription + MiniGrid. Autoplay progress bar. `role="tabpanel"` | COMPONENT_CONTRACT.md §2.6, DESIGN.md §5.5, ADR-010 |

### Parallel Opportunities — Sprint 3

**Wave 3A (Day 1, all start simultaneously — 3 agents):**
| Agent | Ticket | Depends On | Duration |
|-------|--------|-----------|----------|
| FE-Agent-A | S3-FE-07 | S1-FE-02 | 1h |
| FE-Agent-A | S3-FE-10 | S1-FE-02 | 1h |
| FE-Agent-A | S3-FE-12 | S1-FE-02 | 1h |
| FE-Agent-A | S3-FE-13 | S1-FE-02 | 0.5h |
| FE-Agent-A | S3-FE-14 | S1-FE-02 | 0.5h |
| FE-Agent-A | S3-FE-16 | S1-FE-02 | 1h |
| FE-Agent-A | S3-FE-17 | S1-FE-02 | 0.5h |
| FE-Agent-B | S3-FE-09 | S2-FE-04 | 1.5h |
| FE-Agent-B | S3-FE-15 | S2-FE-04, S1-FE-20 | 2h |
| FE-Agent-B | S3-FE-22 | S2-FE-05 | 0.5h |
| FE-Agent-C | S3-FE-06 | S2-FE-04, S2-FE-05 | 2h |

**Wave 3B (Day 2, after Wave 3A — 2 agents):**
| Agent | Ticket | Depends On | Duration |
|-------|--------|-----------|----------|
| FE-Agent-B | S3-FE-23 | S1-FE-02 | 0.5h |
| FE-Agent-B | S3-FE-24 | S3-FE-10, S3-FE-15 | 0.5h |
| FE-Agent-C | S3-FE-08 | S3-FE-06, S3-FE-09, S3-FE-10 | 1.5h |
| FE-Agent-C | S3-FE-11 | S3-FE-06, S3-FE-12, S3-FE-13, S3-FE-14, S3-FE-15, S3-FE-16 | 2.5h |

**Max parallel agents in Sprint 3:** 3 (FE-Agent-A, FE-Agent-B, FE-Agent-C)
**Critical path:** S2-FE-04 → S3-FE-09 → S3-FE-08 (5h) OR S2-FE-04 + S1-FE-20 → S3-FE-15 → S3-FE-11 (6.5h) — **longest chain**

---

## SPRINT 4: Polish + QA

**Objective:** Write comprehensive tests for all endpoints and components, perform accessibility and responsive audits, run integration tests, and fix all bugs discovered.

**Duration:** 2-3 days

### Tickets

| ID | Title | Agent | Hours | Dependencies | Acceptance Criteria | Locked Spec |
|----|-------|-------|-------|-------------|---------------------|-------------|
| **S4-QA-02** | Backend Tests — GET /api/images | QA-Agent-A | 1h | S2-BE-04 | Returns 200 with `ImageListItem[]`, ordered `created_at DESC`, NO `description` field, empty array when none, 500 on DB failure, correct shape (id, prompt, image_url, created_at, likes, is_seed), boolean is_seed, ISO 8601 created_at | API_CONTRACT.md §1.1 |
| **S4-QA-03** | Backend Tests — POST /api/images | QA-Agent-A | 1.5h | S2-BE-05 | Returns 201 on valid prompt, 400 for: missing/non-string/empty/>500 chars prompt, 502 when both providers fail, 500 on unexpected error, prompt trimmed before validation, NO `description` in response, `is_seed: false` | API_CONTRACT.md §1.2, §3.1 |
| **S4-QA-04** | Backend Tests — GET /api/images/:id | QA-Agent-A | 1h | S2-BE-06 | Returns 200 with `ImageDetail` for valid ID, includes `description` (may be empty), includes `signature_hash` (string or null), 404 for non-existent ID, 404 for non-integer ID ("abc", "1.5"), 500 on DB error | API_CONTRACT.md §1.3 |
| **S4-QA-05** | Backend Tests — PATCH /api/images/:id/like | QA-Agent-A | 1h | S2-BE-07 | Returns 200 with `{ likes: <incremented> }`, increments by exactly 1, multiple calls increment multiple times, 404 for non-existent/non-integer ID, 500 on DB error, no auth required | API_CONTRACT.md §1.4 |
| **S4-QA-06** | Backend Integration Tests — Image Generation Flow | QA-Agent-B | 2h | S2-BE-05 | Pollinations: correct URL, 30s timeout, retry on failure. HuggingFace: correct POST, binary response, Supabase Storage upload. Description: correct URL, 15s timeout, non-blocking. Fallback chain: Pollinations fails → HuggingFace → 502 if both. Supabase Storage: correct bucket, filename, public URL | API_CONTRACT.md §5, ADR-004, ADR-005, ADR-008 |
| **S4-QA-07** | Frontend Render Tests — All Components | QA-Agent-C | 2h | S3-FE-07 through S3-FE-17 | Tests render for: ModeToggle (two tabs, labels, aria-selected), StudioView (GeneratePanel, PreviewCard), GeneratePanel (input, button, disabled state), PreviewCard (image, save/discard buttons, animation), GalleryView (all sub-components), ArtworkDisplay (image, alt text), Counter ("Obra X de Y"), ArtworkDescription (prompt, desc, date, like, seed badge), MiniGrid (thumbnails, current highlighted), EmptyState (message, CTA), Skeleton (variants) | COMPONENT_CONTRACT.md (all) |
| **S4-QA-08** | Frontend Interaction Tests | QA-Agent-C | 2h | S3-FE-07 through S3-FE-17 | ModeToggle: click switches mode, calls onToggle. GeneratePanel: Enter submits, Escape clears, disabled during loading. PreviewCard: save calls onSave, discard calls onDiscard. NavigationArrows: prev/next call handlers. MiniGrid: click calls onSelect with correct index. ArtworkDescription: like calls onLike with ID. EmptyState: CTA calls onGoToStudio. Keyboard: ArrowLeft/Right/Home/End in GalleryView | COMPONENT_CONTRACT.md (events, state) |
| **S4-QA-09** | Integration Tests — FE ↔ BE Contracts | QA-Agent-D | 2h | S2-BE-04 through S2-BE-07, S2-FE-04 | Full flow: POST → GET list includes new → GET single returns detail. API client correctly parses BE responses. Type shapes match between FE types and BE responses. Error responses correctly parsed. Like flow: PATCH → GET single reflects updated count. Seed data: GET list returns `is_seed: true` | API_CONTRACT.md, COMPONENT_CONTRACT.md §3 |
| **S4-QA-10** | Accessibility Audit — WCAG AA | QA-Agent-E | 2h | All S3 FE components complete | Contrast ≥ 4.5:1 normal text, ≥ 3:1 large text. Focus indicators on ALL interactive elements (3px purple). Touch targets ≥ 44×44px mobile. Keyboard nav works for all. SR announcements: mode change, artwork nav, like, generation states, errors. `prefers-reduced-motion` disables all animations. Semantic HTML: headings, landmarks, ARIA. Alt text on all images. Skip link present + functional. ARIA attributes match COMPONENT_CONTRACT.md §6.4 | DESIGN.md §13, COMPONENT_CONTRACT.md §6 |
| **S4-QA-11** | Responsive Audit | QA-Agent-E | 1.5h | All S3 FE components complete | Desktop ≥1024px: ModeToggle centered, ArtworkDisplay flex row, description sticky 320px, nav arrows hover-visible, MiniGrid 60×60px, blur(12px). Mobile <1024px: ModeToggle top-right, flex column, description below, nav arrows visible 0.7, MiniGrid 52×52px, blur(8px), touch swipe. Wide ≥1400px: container 1600px, description 380px. All breakpoints tested: 320px, 768px, 1024px, 1400px, 1920px | DESIGN.md §7, COMPONENT_CONTRACT.md §7 |

### Parallel Opportunities — Sprint 4

**Wave 4A (Day 1, all start simultaneously — 5 agents):**
| Agent | Ticket | Depends On | Duration |
|-------|--------|-----------|----------|
| QA-Agent-A | S4-QA-02 | S2-BE-04 | 1h |
| QA-Agent-A | S4-QA-03 | S2-BE-05 | 1.5h |
| QA-Agent-A | S4-QA-04 | S2-BE-06 | 1h |
| QA-Agent-A | S4-QA-05 | S2-BE-07 | 1h |
| QA-Agent-B | S4-QA-06 | S2-BE-05 | 2h |

**Wave 4B (Day 2, after Sprint 3 complete — 3 agents):**
| Agent | Ticket | Depends On | Duration |
|-------|--------|-----------|----------|
| QA-Agent-C | S4-QA-07 | All S3 FE components | 2h |
| QA-Agent-C | S4-QA-08 | All S3 FE components | 2h |
| QA-Agent-D | S4-QA-09 | All BE endpoints + S2-FE-04 | 2h |

**Wave 4C (Day 2-3, after Sprint 3 complete — 1 agent type, 2 agents):**
| Agent | Ticket | Depends On | Duration |
|-------|--------|-----------|----------|
| QA-Agent-E | S4-QA-10 | All S3 FE components | 2h |
| QA-Agent-E | S4-QA-11 | All S3 FE components | 1.5h |

**Max parallel agents in Sprint 4:** 5 (Wave 4A)
**Critical path:** S3-FE-15 → S4-QA-07 (or S4-QA-08) — depends on all FE components being complete

---

## DEPENDENCY GRAPH

### Complete Dependency Tree

```
LEVEL 0 (No dependencies — can start immediately)
├── S1-BE-01 (Backend Setup)
├── S1-FE-01 (Frontend Setup)
├── S1-FE-02 (Global Styles)
├── S1-FE-03 (TypeScript Types)
└── S1-QA-01 (Test Framework)

LEVEL 1 (Depends on Level 0)
├── S1-BE-02 ────────────── depends on S1-BE-01
├── S1-FE-20 ────────────── depends on S1-FE-03
├── S2-BE-08 ────────────── depends on S1-BE-01
├── S2-BE-09 ────────────── depends on S1-BE-01
├── S3-FE-07 ────────────── depends on S1-FE-02
├── S3-FE-10 ────────────── depends on S1-FE-02
├── S3-FE-12 ────────────── depends on S1-FE-02
├── S3-FE-13 ────────────── depends on S1-FE-02
├── S3-FE-14 ────────────── depends on S1-FE-02
├── S3-FE-16 ────────────── depends on S1-FE-02
├── S3-FE-17 ────────────── depends on S1-FE-02
├── S3-FE-23 ────────────── depends on S1-FE-02
├── S2-FE-18 ────────────── depends on S1-FE-02
└── S2-FE-21 ────────────── depends on S1-FE-02

LEVEL 2 (Depends on Level 1)
├── S1-BE-03 ────────────── depends on S1-BE-02
├── S2-BE-04 ────────────── depends on S1-BE-02
├── S2-BE-06 ────────────── depends on S1-BE-02
├── S2-BE-07 ────────────── depends on S1-BE-02
├── S2-BE-05 ────────────── depends on S1-BE-02, S1-BE-03
├── S2-FE-04 ────────────── depends on S1-FE-03
├── S2-FE-05 ────────────── depends on S1-FE-03
├── S3-FE-15 ────────────── depends on S2-FE-04, S1-FE-20
└── S3-FE-09 ────────────── depends on S2-FE-04

LEVEL 3 (Depends on Level 2)
├── S3-FE-06 ────────────── depends on S2-FE-04, S2-FE-05
├── S3-FE-22 ────────────── depends on S2-FE-05
└── S4-QA-02 ────────────── depends on S2-BE-04
└── S4-QA-03 ────────────── depends on S2-BE-05
└── S4-QA-04 ────────────── depends on S2-BE-06
└── S4-QA-05 ────────────── depends on S2-BE-07
└── S4-QA-06 ────────────── depends on S2-BE-05

LEVEL 4 (Depends on Level 3)
├── S3-FE-08 ────────────── depends on S3-FE-06, S3-FE-09, S3-FE-10
├── S3-FE-24 ────────────── depends on S3-FE-10, S3-FE-15
└── S4-QA-09 ────────────── depends on S2-BE-04..07, S2-FE-04

LEVEL 5 (Depends on Level 4)
└── S3-FE-11 ────────────── depends on S3-FE-06, S3-FE-12, S3-FE-13, S3-FE-14, S3-FE-15, S3-FE-16

LEVEL 6 (Depends on ALL FE components)
├── S4-QA-07 ────────────── depends on S3-FE-07 through S3-FE-17
├── S4-QA-08 ────────────── depends on S3-FE-07 through S3-FE-17
├── S4-QA-10 ────────────── depends on ALL S3 FE components
└── S4-QA-11 ────────────── depends on ALL S3 FE components
```

### Critical Path (Longest Chain)

```
S1-FE-03 (0.5h) → S2-FE-04 (1h) → S3-FE-15 (2h) → S3-FE-11 (2.5h) → S4-QA-07 (2h)
= 8h total

Alternative critical path (backend):
S1-BE-01 (1h) → S1-BE-02 (1.5h) → S1-BE-03 (1h) → S2-BE-05 (3h) → S4-QA-03 (1.5h)
= 8h total

Both paths are 8h — the project has TWO parallel critical paths.
```

### Independent Tickets (No Dependencies — Can Start Immediately)

| Ticket | Agent | Hours |
|--------|-------|-------|
| S1-BE-01 | BE-Agent | 1h |
| S1-FE-01 | FE-Agent-A | 1h |
| S1-FE-02 | FE-Agent-B | 1.5h |
| S1-FE-03 | FE-Agent-C | 0.5h |
| S1-QA-01 | QA-Agent | 0.5h |

**5 tickets, 4.5h total — all can run simultaneously with 5 agents.**

---

## AGENT ORCHESTRATION PLAN

### Proposed Agent Pool

| Agent Type | Count | Role |
|------------|-------|------|
| BE-Agent-A | 1 | Backend cross-cutting (middleware, CORS) |
| BE-Agent-B | 1 | Backend GET endpoints |
| BE-Agent-C | 1 | Backend single-item + mutation endpoints |
| BE-Agent-D | 1 | Backend POST + image generation (complex) |
| FE-Agent-A | 1 | Frontend independent components (ModeToggle, PreviewCard, ArtworkDisplay, NavArrows, Counter, MiniGrid, EmptyState) |
| FE-Agent-B | 1 | Frontend form + description + effects (GeneratePanel, ArtworkDescription, AutoplayProgressBar, TransitionOverlay, MicroInteractions) |
| FE-Agent-C | 1 | Frontend orchestration (App.tsx, StudioView, GalleryView) |
| QA-Agent-A | 1 | Backend endpoint tests |
| QA-Agent-B | 1 | Backend integration tests (image generation flow) |
| QA-Agent-C | 1 | Frontend component tests (render + interaction) |
| QA-Agent-D | 1 | FE ↔ BE integration tests |
| QA-Agent-E | 1 | Accessibility + responsive audits |

**Total agents: 12**

### Timeline — Agent Assignment by Sprint

#### Sprint 1: Foundation (Days 1-2)

| Time | BE-Agent | FE-Agent-A | FE-Agent-B | FE-Agent-C | QA-Agent |
|------|----------|------------|------------|------------|----------|
| Day 1 09:00 | S1-BE-01 (1h) | S1-FE-01 (1h) | S1-FE-02 (1.5h) | S1-FE-03 (0.5h) | S1-QA-01 (0.5h) |
| Day 1 10:00 | S1-BE-02 (1.5h) | — | — | S1-FE-20 (0.5h) | — |
| Day 1 11:30 | — | — | — | — | — |
| Day 2 09:00 | S1-BE-03 (1h) | — | — | — | — |

**Sprint 1 peak:** 5 agents simultaneously (Day 1 morning)
**Sprint 1 total wall-clock:** ~1.5 days

#### Sprint 2: Core Infrastructure (Days 3-5)

| Time | BE-Agent-A | BE-Agent-B | BE-Agent-C | BE-Agent-D | FE-Agent-A | FE-Agent-B | FE-Agent-C |
|------|------------|------------|------------|------------|------------|------------|------------|
| Day 3 09:00 | S2-BE-08 (0.5h) | S2-BE-04 (1.5h) | S2-BE-06 (1h) | S2-BE-05 (3h) | S2-FE-04 (1h) | S2-FE-05 (2h) | — |
| | S2-BE-09 (0.5h) | | S2-BE-07 (1h) | | | | |
| Day 3 12:00 | — | — | — | — | — | — | — |
| Day 4 09:00 | — | — | — | — | S2-FE-18 (0.5h) | S2-FE-21 (0.5h) | — |

**Sprint 2 peak:** 7 agents simultaneously (Day 3 morning)
**Sprint 2 total wall-clock:** ~2 days

#### Sprint 3: Views + Interactions (Days 6-8)

| Time | FE-Agent-A | FE-Agent-B | FE-Agent-C |
|------|------------|------------|------------|
| Day 6 09:00 | S3-FE-07 (1h) | S3-FE-09 (1.5h) | S3-FE-06 (2h) |
| | S3-FE-10 (1h) | S3-FE-15 (2h) | |
| | S3-FE-12 (1h) | S3-FE-22 (0.5h) | |
| | S3-FE-13 (0.5h) | | |
| | S3-FE-14 (0.5h) | | |
| | S3-FE-16 (1h) | | |
| | S3-FE-17 (0.5h) | | |
| Day 6 17:00 | — | S3-FE-23 (0.5h) | S3-FE-08 (1.5h) |
| Day 7 09:00 | — | S3-FE-24 (0.5h) | S3-FE-11 (2.5h) |

**Sprint 3 peak:** 3 agents simultaneously (all FE agents)
**Sprint 3 total wall-clock:** ~2.5 days

#### Sprint 4: Polish + QA (Days 9-11)

| Time | QA-Agent-A | QA-Agent-B | QA-Agent-C | QA-Agent-D | QA-Agent-E |
|------|------------|------------|------------|------------|------------|
| Day 9 09:00 | S4-QA-02 (1h) | S4-QA-06 (2h) | — | — | — |
| | S4-QA-03 (1.5h) | | | | |
| | S4-QA-04 (1h) | | | | |
| | S4-QA-05 (1h) | | | | |
| Day 10 09:00 | — | — | S4-QA-07 (2h) | S4-QA-09 (2h) | S4-QA-10 (2h) |
| | | | S4-QA-08 (2h) | | S4-QA-11 (1.5h) |

**Sprint 4 peak:** 5 agents simultaneously (Day 9 morning)
**Sprint 4 total wall-clock:** ~2 days

### Handoff Points

| Handoff | From | To | What |
|---------|------|-----|------|
| H1 | BE-Agent (S1-BE-01) | BE-Agent-A/B/C/D (S2-BE-08/09/04/06/07/05) | Backend project scaffold ready |
| H2 | BE-Agent (S1-BE-02) | BE-Agent-B/C/D (S2-BE-04/06/07/05) | DB connection + schema ready |
| H3 | BE-Agent (S1-BE-03) | BE-Agent-D (S2-BE-05) | Seed data loaded for POST testing |
| H4 | FE-Agent-C (S1-FE-03) | FE-Agent-A/B (S2-FE-04/05), FE-Agent-C (S1-FE-20) | Types available for import |
| H5 | FE-Agent-A (S1-FE-02) | FE-Agent-A/B (all S3 components) | Global styles + CSS variables ready |
| H6 | FE-Agent-A (S2-FE-04) | FE-Agent-B (S3-FE-09/15), FE-Agent-C (S3-FE-06) | API client ready for component use |
| H7 | FE-Agent-B (S2-FE-05) | FE-Agent-C (S3-FE-06/22) | AutoplayContext ready for consumption |
| H8 | FE-Agent-A/B (all S3 components) | QA-Agent-C/E (S4-QA-07/08/10/11) | All UI components ready for testing |
| H9 | BE-Agent-B/C/D (all S2 endpoints) | QA-Agent-A (S4-QA-02/03/04/05) | All endpoints ready for testing |
| H10 | All agents (Sprint 1-3) | QA-Agent-D (S4-QA-09) | Full system ready for integration testing |

### Maximum Parallelism Summary

| Sprint | Max Concurrent Agents | Bottleneck |
|--------|----------------------|------------|
| Sprint 1 | 5 agents | None — all Level 0 tickets |
| Sprint 2 | 7 agents | S2-BE-05 (3h) is the longest single ticket |
| Sprint 3 | 3 agents | S3-FE-11 (2.5h) depends on 6 other components |
| Sprint 4 | 5 agents | All QA tickets depend on Sprints 2-3 completion |

### Optimal Agent Assignment (Minimum Wall-Clock)

If we have **12 agents available**, the theoretical minimum wall-clock is:

- Sprint 1: **1.5 days** (critical path: BE-01 → BE-02 → BE-03 = 3.5h)
- Sprint 2: **2 days** (critical path: BE-02 → BE-05 = 3h, but needs Sprint 1 done)
- Sprint 3: **2.5 days** (critical path: FE-04 → FE-15 → FE-11 = 5.5h, but needs Sprint 2 done)
- Sprint 4: **2 days** (critical path: depends on all FE components)

**Total estimated wall-clock: ~8 days (12 agents fully parallelized)**

If we have only **5 agents** (1 BE, 2 FE, 2 QA):
- Sprint 1: 2 days
- Sprint 2: 3 days
- Sprint 3: 3 days
- Sprint 4: 3 days
**Total: ~11 days**

---

## TICKET SUMMARY BY SPRINT

| Sprint | Tickets | BE | FE | QA | Total Hours |
|--------|---------|----|----|----|-------------|
| Sprint 1: Foundation | 8 | 3 | 4 | 1 | 7.5h |
| Sprint 2: Core Infrastructure | 11 | 5 | 4 | 0 | 12h |
| Sprint 3: Views + Interactions | 15 | 0 | 15 | 0 | 14h |
| Sprint 4: Polish + QA | 10 | 0 | 0 | 10 | 15.5h |
| **TOTAL** | **44** | **8** | **23** | **11** | **~49h** |

Note: Hours are slightly higher than original BACKLOG (~41h) because ticket granularity adds small overhead for context switching between sprints.

---

## RISK MITIGATION

| Risk | Impact | Mitigation |
|------|--------|------------|
| S2-BE-05 (POST endpoint) is the most complex ticket (3h) | Blocks all QA endpoint tests | Assign most experienced BE agent, can split into S2-BE-05a (validation + save) + S2-BE-05b (image generation) if needed |
| S3-FE-11 (GalleryView) depends on 6 other components | Blocks all FE QA tests | Start S3-FE-11 as soon as S3-FE-12/13/14/15/16 are done (don't wait for S3-FE-06/08) |
| S4-QA-10/11 (audits) depend on ALL FE components | Last to complete, any bug fix delays sprint | Start audits incrementally — test components as they're completed in Sprint 3, don't wait for all |
| Two parallel critical paths (FE and BE) | Either path can delay the project | Monitor both paths equally, allocate extra resources to whichever is behind |
