# AI Cloud Log Analyzer

Cloud-based log collection, anomaly detection, incident management, and AI-assisted incident explanation.

## Architecture

Next.js frontend → FastAPI backend → Supabase/PostgreSQL → ML anomaly detection → Incident service → AI explanation → Dashboard/alerts.

## Project status

Initial project foundation. Implementation will be built layer-by-layer according to the technical project report.

## Planned stack

- Frontend: Next.js, TypeScript, Tailwind CSS, Recharts
- Backend: Python, FastAPI, Pydantic
- Data/ML: Pandas, NumPy, Scikit-learn
- Database/Auth/Storage: Supabase/PostgreSQL
- AI: OpenAI-compatible LLM API through a backend service
- Deployment: Docker; cloud deployment configuration to be added

## Security

Secrets must be supplied through environment/deployment secret configuration. Never commit API keys, service-role keys, passwords, or `.env` files.
