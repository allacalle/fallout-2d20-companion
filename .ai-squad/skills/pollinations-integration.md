# Pollinations Integration

**Type:** External API | **Use:** Integrating Pollinations.ai for image generation and text descriptions

## Description

How to integrate Pollinations.ai APIs — image generation (binary) and text/description generation — with proper error handling, timeouts, and retry logic.

## Endpoints

### Image Generation
```
GET https://image.pollinations.ai/prompt/{prompt_encoded}
```
- No API key required
- Returns image binary directly (JPEG/PNG)
- Prompt must be URL-encoded
- Response time: 5-30 seconds depending on complexity
- No rate limit documented, but be respectful

### Text/Description Generation
```
GET https://text.pollinations.ai/{prompt_encoded}
```
- No API key required
- Returns text/plain response
- Used for generating poetic descriptions for artworks
- Response time: 2-10 seconds

## Workflow for Image Generation (Backend)

1. Receive prompt from frontend (POST /api/images)
2. URL-encode the prompt
3. Fetch from `https://image.pollinations.ai/prompt/{encoded}`
4. Handle the binary response
5. Store the URL (not the binary) in SQLite: `https://image.pollinations.ai/prompt/{encoded}`
6. Generate description via text API (optional)
7. Return Image object with id, prompt, image_url, description, created_at, likes

## Workflow for Description Generation (Backend)

1. After saving image, call text API with an artistic prompt:
   ```
   "Write a short poetic museum plaque description (2-3 sentences) for an artwork generated from this prompt: '{user_prompt}'. Write in Spanish. Be evocative, mysterious, like a real museum description."
   ```
2. Store the response in the `description` field
3. If description generation fails, store empty string (non-blocking)

## Error Handling

### Image API fails
- Timeout after 30 seconds
- Retry once after 5 seconds
- If still fails, return 502 with error message
- Log the raw response for debugging

### Text API fails
- Timeout after 15 seconds
- Do NOT retry (non-critical)
- Store empty description
- Log the error

## Code Pattern (Backend - Express)

```ts
import fetch from 'node-fetch';

async function generateImageUrl(prompt: string): Promise<string> {
  const encoded = encodeURIComponent(prompt);
  const url = `https://image.pollinations.ai/prompt/${encoded}`;
  
  // We store the URL, not download the binary
  // The frontend will load this URL directly
  return url;
}

async function generateDescription(prompt: string): Promise<string> {
  const artisticPrompt = encodeURIComponent(
    `Write a short poetic museum plaque description (2-3 sentences) for an artwork generated from this prompt: "${prompt}". Write in Spanish. Be evocative, mysterious, like a real museum description.`
  );
  const url = `https://text.pollinations.ai/${artisticPrompt}`;
  
  try {
    const response = await fetch(url, { signal: AbortSignal.timeout(15000) });
    if (!response.ok) return '';
    return (await response.text()).trim();
  } catch {
    return '';
  }
}
```

## Important Notes

- **Do NOT download and store images** — Pollinations URLs are stable, store only the URL
- **URL encoding is critical** — spaces, special chars must be properly encoded
- **The image URL IS the API endpoint** — frontend loads images directly from Pollinations
- **No caching needed** — Pollinations caches on their side
- **Description is optional** — image works without it

## Debug Protocol

If images don't load:
1. Log the raw URL being stored
2. Open the URL directly in browser
3. Check if prompt encoding is correct
4. Check if Pollinations is up (status unknown, no status page)
