
-- Multi-Agent Editorial & SEO Content Intelligence Engine
-- Supabase / PostgreSQL database schema

CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Articles table
CREATE TABLE IF NOT EXISTS public.articles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    topic TEXT NOT NULL,
    target_keyword TEXT NOT NULL,
    search_intent TEXT,
    meta_title VARCHAR(60),
    meta_description VARCHAR(155),
    outline_json JSONB,
    content_markdown TEXT,
    bilingual_summary TEXT,
    quality_score INTEGER CHECK (
        quality_score >= 0 AND quality_score <= 100
    ),
    status TEXT NOT NULL DEFAULT 'draft'
        CHECK (status IN ('draft', 'approved', 'published')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Agent execution logs
CREATE TABLE IF NOT EXISTS public.agent_runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    article_id UUID REFERENCES public.articles(id) ON DELETE CASCADE,
    agent_name TEXT NOT NULL,
    input_tokens INTEGER DEFAULT 0,
    output_tokens INTEGER DEFAULT 0,
    latency_ms INTEGER DEFAULT 0,
    critic_feedback_json JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for faster article searches
CREATE INDEX IF NOT EXISTS idx_articles_created_at
ON public.articles(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_articles_status
ON public.articles(status);

CREATE INDEX IF NOT EXISTS idx_agent_runs_article_id
ON public.agent_runs(article_id);

-- Verify tables
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
AND table_name IN ('articles', 'agent_runs');
