import gradio as gr
from google import genai
from pymongo import MongoClient
from qdrant.reranking import get_reranked_results


CUSTOM_CSS = """
body {
    background: radial-gradient(circle at top, #0f172a, #020617);
    color: #e5e7eb;
    font-family: 'Inter', system-ui, sans-serif;
}

.gradio-container {
    max-width: 1100px !important;
    margin: auto;
}

/* Header */
#title {
    text-align: center;
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(90deg, #22d3ee, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
}

#subtitle {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 30px;
}

/* Cards */
.card {
    background: rgba(15, 23, 42, 0.9);
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.6);
    border: 1px solid rgba(148,163,184,0.1);
}

/* Inputs */
textarea, input {
    background: #020617 !important;
    color: #e5e7eb !important;
    border-radius: 12px !important;
    border: 1px solid #1e293b !important;
}

/* Buttons */
button.primary {
    background: linear-gradient(135deg, #6366f1, #22d3ee) !important;
    border-radius: 14px !important;
    font-weight: 600 !important;
    border: none !important;
}

button.primary:hover {
    transform: scale(1.03);
    filter: brightness(1.15);
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 6px;
}
::-webkit-scrollbar-thumb {
    background: #334155;
    border-radius: 6px;
}
"""


gemini_client = genai.Client(api_key="<YOUR_KEY>")

mongo_client = MongoClient(
    "mongodb://admin:admin123@10.81.53.217:27017/?authSource=admin"
)

db = mongo_client["lawgpt_db"]
articles_collection = db["articles"]

def retrieve_articles_from_mongodb(article_ids: list) -> dict:
    articles = {}
    for article_id in article_ids:
        doc = articles_collection.find_one({"article_id": str(article_id)})
        if doc:
            articles[article_id] = doc.get("article_desc", "")
    return articles


def generate_summary(query: str, articles: dict) -> str:
    context = "\n\n".join(
        [f"Article {aid}:\n{content}" for aid, content in articles.items()]
    )

    prompt = f"""
You are a legal information retrieval agent trained on the full text of the
Constitution of India, including all Parts, Articles, and Schedules.

Your role is to help users understand constitutional provisions by
retrieving relevant articles and explaining them in clear, simple language.

STRICT RULES:
1. You MUST NOT provide legal advice, legal opinions, or recommendations.
2. You MUST ground every response strictly in retrieved constitutional text.
3. You MUST explicitly cite Article numbers, Parts, and titles.
4. You MUST NOT hallucinate laws, interpretations, amendments, or case law.
5. If the query falls outside the Constitution, state this clearly.
6. Always include an informational disclaimer.


RESPONSE STRUCTURE (MANDATORY):
1. Relevant Constitutional Provision(s)
   - Article number, Part, and official title
2. Constitutional Text
   - Exact or briefly excerpted text if long
3. Plain-language Explanation
   - Neutral explanation limited to what the text states
4. Source
   - Constitution of India
5. Disclaimer
   - “This information is for educational purposes only and does not constitute legal advice.”

SCOPE LIMITATIONS:
- Constitution of India only
- No judicial interpretations unless explicitly present in retrieved data
- No predictive, advisory, or prescriptive statements

GOAL:
Improve equitable access to constitutional knowledge by enabling
accurate, traceable, and evidence-grounded retrieval of constitutional provisions.

Articles:
{context}

User Query: {query}

Provide a clear, concise answer.
"""

    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text




def lawgpt_interface(query: str):
    try:
        if not query.strip():
            return " Please enter a valid query.", ""

        print(f"Processing query: {query}")

        ranked_article_ids = get_reranked_results(query, top_k=5)

        if not ranked_article_ids:
            return "No relevant articles found.", ""

        articles = retrieve_articles_from_mongodb(ranked_article_ids)

        if not articles:
            return "Failed to retrieve articles from database.", ""

        answer = generate_summary(query, articles)

        # Format sources
        sources = "##  Retrieved Articles\n\n"
        for article_id, content in articles.items():
            preview = content[:300] + "..." if len(content) > 300 else content
            sources += f"**Article {article_id}**\n\n{preview}\n\n---\n\n"

        return answer, sources

    except Exception as e:
        print("Error:", e)
        return f"Error: {str(e)}", ""


def create_interface():
    with gr.Blocks(title="⚖️ LawGPT - Indian Constitution Assistant") as demo:

        gr.Markdown("<div id='title'>⚖️ LawGPT</div>")
        gr.Markdown(
            "<div id='subtitle'>AI-powered Indian Constitution Assistant</div>"
        )

        with gr.Row():
            with gr.Column():
                with gr.Group(elem_classes="card"):
                    query_input = gr.Textbox(
                        label="Ask your question",
                        placeholder="e.g. What are the fundamental rights?",
                        lines=4
                    )

                    submit_btn = gr.Button(
                        "Search & Summarize",
                        variant="primary"
                    )

        with gr.Row():
            with gr.Column():
                with gr.Group(elem_classes="card"):
                    answer_output = gr.Textbox(
                        label="Answer",
                        interactive=False,
                        lines=8
                    )

        with gr.Row():
            with gr.Column():
                with gr.Group(elem_classes="card"):
                    sources_output = gr.Markdown(
                        label="Sources"
                    )

        submit_btn.click(
            fn=lawgpt_interface,
            inputs=query_input,
            outputs=[answer_output, sources_output]
        )

        gr.Markdown("### Example Questions")

        gr.Examples(
            examples=[
                ["What are the fundamental rights under the Indian Constitution?"],
                ["Explain the powers of the President"],
                ["How can the Constitution be amended?"],
                ["Describe the structure of Parliament"]
            ],
            inputs=query_input
        )

    return demo


if __name__ == "__main__":
    demo = create_interface()
    demo.launch(
        share=True,
        css=CUSTOM_CSS,
        theme=gr.themes.Soft(primary_hue="indigo")
    )
