# AI Cloud Log Analyzer

Cloud-based log collection, anomaly detection, incident management, and AI-assisted incident explanation.

## Architecture

Next.js frontend → FastAPI backend → Supabase/PostgreSQL → ML anomaly detection → Incident service → AI explanation → Dashboard/alerts.

## Project status

MVP implementation is connected across the frontend, FastAPI API, Supabase schema, ML anomaly detection, incident workflow, and AI explanation service.

## Planned stack

- Frontend: Next.js, TypeScript, Tailwind CSS, Recharts
- Backend: Python, FastAPI, Pydantic
- Data/ML: Pandas, NumPy, Scikit-learn
- Database/Auth/Storage: Supabase/PostgreSQL
- AI: OpenAI-compatible LLM API through a backend service
- Deployment: Vercel frontend, Render FastAPI backend, Supabase services

## Security

Secrets must be supplied through environment/deployment secret configuration. Never commit API keys, service-role keys, passwords, or `.env` files.
