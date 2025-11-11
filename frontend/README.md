# Multi-Agent Advisory System - Frontend

React + TypeScript + Vite frontend for the Corporate Formation Advisory System.

## Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

#### Required Environment Variables

| Variable | Description | Example Value |
|----------|-------------|---------------|
| `VITE_API_URL` | Backend API base URL | `http://localhost:8000` (development) |

**Example `.env` file:**
```
VITE_API_URL=http://localhost:8000
```

### 3. Run Development Server

```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## Building for Production

### Build the Application

```bash
npm run build
```

The production build will be in the `dist/` directory. This creates an optimized, minified bundle ready for deployment.

### Preview Production Build Locally

```bash
npm run preview
```

This serves the production build locally at `http://localhost:4173` for testing.

### Production Environment Variables

For production deployments, create a `.env.production` file or set environment variables in your deployment platform:

```bash
VITE_API_URL=https://your-backend-api-url.com
```

**Important**: The `VITE_` prefix is required for Vite to expose the variable to the client-side code.

## Deployment

The frontend is a static site that can be deployed to any static hosting service.

### Vercel (Recommended)

1. Connect your GitHub repository to Vercel
2. Set the environment variable:
   - `VITE_API_URL`: Your production backend URL
3. Vercel will automatically detect Vite and deploy on every push

### Netlify

1. Drag and drop the `dist/` folder to Netlify, or connect your GitHub repo
2. Build settings:
   - Build command: `npm run build`
   - Publish directory: `dist`
3. Set environment variable:
   - `VITE_API_URL`: Your production backend URL

### AWS S3 + CloudFront

```bash
# Build the application
npm run build

# Upload to S3 bucket
aws s3 sync dist/ s3://your-bucket-name --delete

# Invalidate CloudFront cache
aws cloudfront create-invalidation --distribution-id YOUR_DIST_ID --paths "/*"
```

### GitHub Pages

Add a GitHub Actions workflow to deploy automatically:

```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      - run: npm ci
      - run: npm run build
        env:
          VITE_API_URL: ${{ secrets.VITE_API_URL }}
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist
```

### Other Platforms

The `dist/` folder can be deployed to:
- **Railway**: Connect GitHub and deploy automatically
- **Render**: Static site deployment from GitHub
- **DigitalOcean App Platform**: Static site hosting
- **Firebase Hosting**: `firebase deploy`

## Project Structure

```
src/
├── api/
│   └── client.ts          # API client for backend communication
├── components/
│   ├── QueryInput.tsx     # User query input component
│   ├── RecommendationDisplay.tsx  # Display recommendations
│   └── ClarificationDialog.tsx    # Clarification modal
├── types/
│   └── index.ts           # TypeScript interfaces
├── App.tsx                # Main application component
└── main.tsx               # Application entry point
```

## React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...

      // Remove tseslint.configs.recommended and replace with this
      tseslint.configs.recommendedTypeChecked,
      // Alternatively, use this for stricter rules
      tseslint.configs.strictTypeChecked,
      // Optionally, add this for stylistic rules
      tseslint.configs.stylisticTypeChecked,

      // Other configs...
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```
