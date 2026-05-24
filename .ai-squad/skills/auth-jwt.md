# Auth JWT

**Type:** Security | **Use:** Implementing JWT authentication in Express/Node.js API

## Description

How to implement JWT authentication in an Express/Node.js API.

## Concepts

- **JWT (JSON Web Token)**: Stateless token that stores user information
- **Access Token**: Short-lived (15-60 min), used for API requests
- **Refresh Token**: Long-lived (7-30 days), used to get new access tokens

## Implementation Steps

### 1. Install dependencies

```bash
npm install jsonwebtoken bcrypt
npm install -D @types/jsonwebtoken
```

### 2. Create auth middleware

```ts
// src/middleware/auth.ts
import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';

export const authMiddleware = (req: Request, res: Response, next: NextFunction) => {
  const token = req.headers.authorization?.split(' ')[1];
  
  if (!token) {
    return res.status(401).json({ error: 'No token provided' });
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET!);
    req.user = decoded;
    next();
  } catch (error) {
    return res.status(403).json({ error: 'Invalid token' });
  }
};
```

### 3. Create auth service

```ts
// src/services/auth.service.ts
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';

export class AuthService {
  async login(email: string, password: string) {
    const user = await this.findUserByEmail(email);
    if (!user) throw new Error('Invalid credentials');

    const validPassword = await bcrypt.compare(password, user.password);
    if (!validPassword) throw new Error('Invalid credentials');

    const token = jwt.sign(
      { id: user.id, email: user.email },
      process.env.JWT_SECRET!,
      { expiresIn: '1h' }
    );

    return { token, user: { id: user.id, email: user.email } };
  }

  async register(email: string, password: string) {
    const hashedPassword = await bcrypt.hash(password, 10);
    const user = await this.createUser(email, hashedPassword);
    
    const token = jwt.sign(
      { id: user.id, email: user.email },
      process.env.JWT_SECRET!,
      { expiresIn: '1h' }
    );

    return { token, user: { id: user.id, email: user.email } };
  }
}
```

### 4. Create auth routes

```ts
// src/routes/auth.ts
import { Router } from 'express';
import { AuthService } from '../services/auth.service';

const router = Router();
const authService = new AuthService();

router.post('/api/auth/login', async (req, res) => {
  try {
    const { email, password } = req.body;
    const result = await authService.login(email, password);
    res.json(result);
  } catch (error) {
    res.status(401).json({ error: 'Invalid credentials' });
  }
});

router.post('/api/auth/register', async (req, res) => {
  try {
    const { email, password } = req.body;
    const result = await authService.register(email, password);
    res.json(result);
  } catch (error) {
    res.status(400).json({ error: 'Registration failed' });
  }
});

export default router;
```

## Security Rules

- ✅ Always use HTTPS in production
- ✅ Store JWT_SECRET in environment variables
- ✅ Set reasonable expiration times
- ✅ Validate all inputs before auth
- ✅ Use bcrypt for password hashing

## ❌ Common mistakes

### Not verifying token in production

```ts
// ❌ Bad - skip auth in development
if (process.env.NODE_ENV === 'development') {
  next();
  return;
}
```

### Storing secrets in code

```ts
// ❌ Bad
const SECRET = 'my-secret-key-123';

// ✅ Good
const SECRET = process.env.JWT_SECRET!;
```
