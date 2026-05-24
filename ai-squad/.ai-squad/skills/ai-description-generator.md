# AI Description Generator

**Type:** AI Integration | **Use:** Generating poetic museum-plaque descriptions for artworks

## Description

How to use Pollinations text API to generate evocative, museum-quality descriptions for saved artworks. The description transforms a simple prompt into a poetic "placa de museo" that elevates the experience.

## The Concept

When a visitor saves an artwork, the system generates a description that reads like a real museum plaque:

**User prompt:** "un perro espacial con gafas de sol"
**Generated description:** "El visitante soñó con un canino navegando el cosmos, y así nació esta pieza donde la soledad del espacio se encuentra con la irreverencia de unas gafas de sol. Una reflexión sobre cómo incluso en la vastedad del universo, el humor nos mantiene humanos."

## API Usage

### Endpoint
```
GET https://text.pollinations.ai/{prompt_encoded}
```

### System Prompt Template
```
Eres un curador de museo de arte moderno. Escribe una descripción poética de 2-3 frases para una obra de arte generada por IA.

El visitante escribió este prompt: "{user_prompt}"

La descripción debe:
- Ser evocadora y misteriosa
- Sonar como una placa real de museo
- Referenciar lo que el visitante quiso crear
- Tener tono poético pero accesible
- Escribir en español
- Máximo 3 frases
```

## Backend Implementation

```ts
async function generateArtDescription(userPrompt: string): Promise<string> {
  const systemPrompt = `Eres un curador de museo de arte moderno. Escribe una descripción poética de 2-3 frases para una obra de arte generada por IA. El visitante escribió: "${userPrompt}". La descripción debe ser evocadora, misteriosa, como una placa real de museo. En español. Máximo 3 frases.`;
  
  const encoded = encodeURIComponent(systemPrompt);
  const url = `https://text.pollinations.ai/${encoded}`;
  
  try {
    const response = await fetch(url, { 
      signal: AbortSignal.timeout(15000) 
    });
    
    if (!response.ok) {
      console.error(`Description API returned ${response.status}`);
      return '';
    }
    
    const text = await response.text();
    return text.trim().slice(0, 500); // Cap at 500 chars
  } catch (error) {
    console.error('Description generation failed:', error);
    return ''; // Non-blocking failure
  }
}
```

## Integration Point

Called in POST /api/images after the image URL is generated:

```ts
app.post('/api/images', (req, res) => {
  const { prompt } = req.body;
  const imageUrl = `https://image.pollinations.ai/prompt/${encodeURIComponent(prompt)}`;
  
  // Generate description (non-blocking, fire-and-forget pattern)
  const description = await generateArtDescription(prompt);
  
  // Insert into DB
  const stmt = db.prepare(
    'INSERT INTO images (prompt, image_url, description) VALUES (?, ?, ?)'
  );
  const result = stmt.run(prompt, imageUrl, description);
  
  res.json({ id: result.lastInsertRowid, prompt, image_url: imageUrl, description, created_at: new Date().toISOString(), likes: 0 });
});
```

## Fallback Behavior

- If description generation fails → store empty string
- If description is too long → truncate to 500 chars
- If description contains inappropriate content → store empty string
- **Never block the save** — description is enhancement, not requirement

## Display in Frontend

```tsx
<div className={styles.description}>
  {artwork.description ? (
    <p>"{artwork.description}"</p>
  ) : (
    <p className={styles.noDescription}>Sin descripción</p>
  )}
</div>
```

## Gotchas

- **Response can be unpredictable** — Pollinations text API is not fine-tuned, results vary
- **Timeout is critical** — don't let it hang forever (15s max)
- **Language** — explicitly request Spanish in the prompt
- **Non-blocking** — image saves even if description fails
- **Cache consideration** — same prompt → same description (acceptable for this project)
- **Debug** — log the raw text response to understand what the API returns
