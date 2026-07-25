# Agent-Eval Dashboard

Next.js web dashboard for visualizing AI agent evaluation results.

## Overview

The dashboard provides:

- 📊 **Results Visualization** - Charts and tables of test results
- 📈 **Performance Metrics** - Success rates, timing, cost analysis
- 🔍 **Detailed Traces** - View individual test cases and responses
- 📁 **Project Management** - Organize evaluations by project
- 🌙 **Dark Mode** - Comfortable viewing experience
- ⚡ **Real-time Updates** - Live result streaming via tRPC

## Tech Stack

- **Framework**: Next.js 14 (React 18)
- **Language**: TypeScript
- **Styling**: Tailwind CSS v4
- **Database**: SQLite (Prisma ORM)
- **API**: tRPC (type-safe API)
- **UI Components**: Headless UI, Radix UI

## Quick Start

### Prerequisites

- Node.js 18+
- pnpm (recommended) or npm

### Installation

```bash
cd dashboard

# Install dependencies
pnpm install

# Setup database
npx prisma migrate dev

# Optional: Seed database with example data
npx prisma db seed

# Start development server
pnpm dev
```

Open http://localhost:3000 in your browser.

## Development

### Project Structure

```
src/
├── app/
│   ├── layout.tsx              # Root layout
│   ├── page.tsx                # Home/Dashboard
│   ├── projects/
│   │   ├── page.tsx            # Projects list
│   │   └── [id]/               # Project details
│   ├── results/
│   │   ├── page.tsx            # Results viewer
│   │   └── [id]/               # Result details
│   ├── api/
│   │   └── trpc/               # tRPC API routes
│   └── error.tsx               # Error page
├── components/
│   ├── Header.tsx              # Navigation header
│   ├── ResultsTable.tsx        # Results display
│   ├── Charts.tsx              # Data visualization
│   ├── ProjectCard.tsx         # Project card component
│   └── ...
├── lib/
│   ├── trpc.ts                 # tRPC client setup
│   ├── utils.ts                # Utility functions
│   └── db.ts                   # Database client
├── styles/
│   └── globals.css             # Global styles
└── server/
    └── api/                    # Server-side API routes
```

### File Organization

- **app/**: Next.js app router pages and routes
- **components/**: Reusable React components
- **lib/**: Shared utilities and configuration
- **styles/**: CSS and styling
- **prisma/**: Database schema and migrations

### Running Tests

```bash
# Run tests
pnpm test

# Run tests in watch mode
pnpm test:watch

# Generate coverage report
pnpm test:coverage
```

### Formatting and Linting

```bash
# Format code with Prettier
pnpm format

# Check with ESLint
pnpm lint

# Fix linting issues
pnpm lint:fix
```

## API Routes

The dashboard uses tRPC for type-safe API calls.

### Available Endpoints

```typescript
// Projects
trpc.project.list.query()              // Get all projects
trpc.project.create.mutate(data)       // Create project
trpc.project.getById.query(id)         // Get project details
trpc.project.delete.mutate(id)         // Delete project

// Results
trpc.result.list.query(projectId)      // Get results for project
trpc.result.create.mutate(data)        // Create result
trpc.result.getById.query(id)          // Get result details
trpc.result.getStats.query(projectId)  // Get result statistics
```

## Database

Using Prisma ORM with SQLite.

### Schema

```prisma
model Project {
  id        String     @id @default(cuid())
  name      String     @unique
  description String?
  results   Result[]
  createdAt DateTime   @default(now())
  updatedAt DateTime   @updatedAt
}

model Result {
  id         String     @id @default(cuid())
  projectId  String
  project    Project    @relation(fields: [projectId], references: [id], onDelete: Cascade)
  testName   String
  input      String?
  expected   String?
  actual     String
  status     String     # passed, failed, error
  score      Float      # 0-1
  grader     String     # grader type used
  error      String?
  details    Json
  createdAt  DateTime   @default(now())
  
  @@index([projectId])
}
```

### Migrations

```bash
# Create new migration
npx prisma migrate dev --name migration_name

# Reset database (development only)
npx prisma migrate reset

# View database
npx prisma studio
```

## Environment Variables

Create a `.env.local` file:

```bash
# Database
DATABASE_URL="file:./prisma/dev.db"

# Optional
NEXT_PUBLIC_API_URL=http://localhost:3000
```

## Styling

Using Tailwind CSS v4:

```tsx
// Use Tailwind classes
<div className="flex items-center justify-between p-4 bg-white rounded-lg shadow">
  <h1 className="text-2xl font-bold">Results</h1>
</div>
```

### Dark Mode

Dark mode is automatically detected from system preferences.

```tsx
// Component will automatically adapt
<div className="bg-white dark:bg-slate-950">
  Content adapts to dark mode
</div>
```

## Performance Optimization

- **Image Optimization**: Next.js Image component
- **Code Splitting**: Automatic route-based splitting
- **Data Caching**: React Query with tRPC
- **Database Indexing**: Prisma indexes on foreign keys

## Deployment

### Vercel (Recommended)

1. Push code to GitHub
2. Connect repo to Vercel
3. Set environment variables
4. Deploy

### Docker

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install
COPY . .
RUN pnpm build
EXPOSE 3000
CMD ["pnpm", "start"]
```

```bash
docker build -t agent-eval-dashboard .
docker run -p 3000:3000 agent-eval-dashboard
```

### Self-Hosted

```bash
# Build
pnpm build

# Start production server
pnpm start
```

## Troubleshooting

### Database Issues

```bash
# Reset database
npx prisma migrate reset

# Verify database
npx prisma db execute --stdin < query.sql
```

### Port Already in Use

```bash
# Use different port
pnpm dev -- -p 3001
```

### Dependencies Issues

```bash
# Clear cache and reinstall
rm -rf node_modules pnpm-lock.yaml
pnpm install
```

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [Prisma Documentation](https://www.prisma.io/docs)
- [tRPC Documentation](https://trpc.io)
- [Tailwind CSS](https://tailwindcss.com)

## Support

For issues and questions:
- Open an [issue](https://github.com/nurettinsoker/-agent-eval/issues)
- Check [discussions](https://github.com/nurettinsoker/-agent-eval/discussions)
