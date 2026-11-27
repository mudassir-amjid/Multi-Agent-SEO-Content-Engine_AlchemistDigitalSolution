
from app.agents.research_agent import ResearchAgent
from app.agents.outline_agent import OutlineAgent
from app.agents.writer_agent import WriterAgent
from app.agents.critic_agent import CriticAgent

from app.models.input_models import ArticleRequest


class EditorialPipeline:

    def __init__(self):
        self.research_agent = ResearchAgent()
        self.outline_agent = OutlineAgent()
        self.writer_agent = WriterAgent()
        self.critic_agent = CriticAgent()

    def run(self, request: ArticleRequest):

        print("\n[1/4] Running Research Agent...")
        research = self.research_agent.run(request)

        if research is None:
            return {"status": "failed", "error": "Research Agent failed"}

        print("[2/4] Running SEO Outliner...")
        outline = self.outline_agent.run(research)

        if outline is None:
            return {"status": "failed", "error": "Outline Agent failed"}

        print("[3/4] Running Editorial Writer...")
        article = self.writer_agent.run(research, outline)

        if article is None:
            return {"status": "failed", "error": "Writer Agent failed"}

        print("[4/4] Running Quality Critic...")
        feedback = self.critic_agent.run(research, outline, article)

        if feedback is None:
            return {"status": "failed", "error": "Critic Agent failed"}

        # One revision attempt if score is below 80
        if feedback.total_score < 80:

            print("\nQuality score below 80. Starting one revision...")

            article = self.writer_agent.run(
                research,
                outline,
                revision_feedback=feedback.model_dump_json(indent=2)
            )

            if article is None:
                return {"status": "failed", "error": "Article revision failed"}

            print("Reviewing revised article...")

            feedback = self.critic_agent.run(
                research,
                outline,
                article
            )

            if feedback is None:
                return {"status": "failed", "error": "Final review failed"}

        return {
            "status": "completed",
            "research": research.model_dump(),
            "outline": outline.model_dump(),
            "article": article.model_dump(),
            "critic_feedback": feedback.model_dump(),
            "quality_score": feedback.total_score,
            "approved": feedback.total_score >= 80
        }


if __name__ == "__main__":

    pipeline = EditorialPipeline()

    print("\nEditorial Pipeline initialized successfully!")
    print("Agents connected: 4")
    print("Revision attempts: 1")
    print("Approval threshold: 80/100")
