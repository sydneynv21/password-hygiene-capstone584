import gradio as gr

from pass_analysis import password_strength
from pass_analysis import check_password_in_dictionary
from pass_analysis import get_safe_metrics
from prompt_builder import build_prompt
from ollama_client import OllamaClient

#summarizes password analysis metrics for UI
def format_metrics_for_display(metrics):
    scores = metrics["scores"]

    dictionary_flag = str(metrics.get("in_dictionary", "no")).lower() == "yes"
    breach_flag = str(metrics.get("breach_detected", "no")).lower() == "yes"

    def yes_no(value):
        return "Yes" if value else "No"

    return f"""Overall Password Assessment
Overall Score: {metrics["total_100"]}/100
Risk Level: {metrics["severity"]}

What We Detected
- Length: {metrics["length"]} characters
- Includes letters: {yes_no(metrics["has_letter"])}
- Includes numbers: {yes_no(metrics["has_digit"])}
- Includes special characters: {yes_no(metrics["has_special"])}
- Includes common or dictionary words: {yes_no(dictionary_flag)}
- Found in known data breaches: {"Yes (high risk)" if breach_flag else "No"}

Security Category Scores
- Length Strength: {scores["Length"]}/10
- Predictability: {scores["Predictability"]}/5
- Pattern Resistance: {scores["Patterns"]}/10
- Character Variety: {scores["Variety"]}/10

What These Scores Mean
- Length Strength measures whether the password is long enough to resist guessing.
- Predictability measures how easy the structure may be to anticipate.
- Pattern Resistance checks for common sequences or simple constructions.
- Character Variety reflects how mixed the character types are.
- If a password is found in data breaches, it means attackers may already know it.
"""

#core data flow
def password_pipeline(password, experience_level):
    if not password:
        return "Please enter a password.", "", ""

    experience_level = int(experience_level)

    score = password_strength(password)
    dict_result = check_password_in_dictionary(password)
    metrics = get_safe_metrics(password)

    prompt = build_prompt(metrics, experience_level)
    metrics_text = format_metrics_for_display(metrics)

    client = OllamaClient(model="llama3.1:8b")
    if not client.ping():
        return (
            "Ollama is not reachable at http://localhost:11434. Make sure Ollama is running.",
            metrics_text
        )

    coaching = client.generate(
        prompt,
        system="You are a helpful cybersecurity coach. Keep advice safe and privacy-preserving."
    )

    return coaching, metrics_text, ""

#Gradio css setup
custom_css = """
.gradio-container {
    max-width: 1000px !important;
    margin: 0 auto !important;
}

.hero {
    text-align: center;
    padding: 16px 0 8px 0;
}

.hero h1 {
    margin-bottom: 6px;
}

.hero p {
    font-size: 16px;
    opacity: 0.9;
    margin-bottom: 0;
}

.section-card {
    border-radius: 16px;
    padding: 16px;
    border: 1px solid #2f2f2f22;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    margin-top: 10px;
}

.input-panel .gr-column {
    gap: 10px !important;
}

.input-panel .gr-block,
.input-panel .gr-box,
.input-panel .gr-group {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

.input-panel .gr-column:first-child {
    padding-right: 10px !important;
}

.input-panel .gr-column:last-child {
    padding-left: 10px !important;
}

/* make spacing around the helper box consistent */
.input-panel .experience-help {
    margin-top: 18px !important;
    margin-bottom: 18px !important;
    padding: 14px 18px;
    border-radius: 12px;
    background: rgba(255,255,255,0.04);
    font-size: 14px;
    line-height: 1.7;
    width: 100%;
    box-sizing: border-box;
}

.experience-help-title {
    font-weight: 600;
    margin-bottom: 8px;
}

.output-card {
    border-radius: 16px;
    padding: 10px;
    border: 1px solid #2f2f2f22;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    margin-top: 14px;
}

.footer-note {
    text-align: center;
    font-size: 13px;
    opacity: 0.75;
    margin-top: 12px;
}
"""

#Gradio UX/UI setup
def main():
    theme = gr.themes.Soft(
        radius_size="lg",
        text_size="md",
    )

    with gr.Blocks(title="AI Password Coach") as demo:
        gr.HTML("""
        <div class="hero">
            <h1>🔐 AI Password Hygiene Coach</h1>
            <p>
            This AI-powered coaching tool analyzes password strength and provides personalized suggestions to help you build safer login habits. All analysis is performed locally, so you can explore security improvements with confidence.
            </p>

            <p style="margin-top:20px;">
            Enter a password below to receive constructive security coaching and learn how small changes can significantly improve your digital safety.
            </p>
        </div>
        """)

        with gr.Group(elem_classes="section-card input-panel"):
            with gr.Row(equal_height=True):
                with gr.Column(scale=2, min_width=0):
                    password_input = gr.Textbox(
                        label="Enter Password",
                        type="password",
                        placeholder="Type password here..."
                    )

                with gr.Column(scale=1, min_width=0):
                    experience_input = gr.Radio(
                        choices=["1", "2", "3"],
                        label="Experience Level",
                        value="1"
                    )

            gr.HTML("""
            <div class="experience-help">
                <div class="experience-help-title">Not sure what experience level to choose?</div>
                <div><b>Beginner (1)</b> — You want simple, practical password advice</div>
                <div><b>Intermediate (2)</b> — You understand some basic security concepts</div>
                <div><b>Advanced (3)</b> — You prefer more technical explanations and deeper insight</div>
            </div>
            """)

            analyze_btn = gr.Button("Analyze Password", variant="primary")
                    

        with gr.Group(elem_classes="output-card"):
            coaching_output = gr.Textbox(
                label="AI Coaching Response",
                lines=12,
                interactive=False
            )

        with gr.Accordion("Password Analysis Metrics", open=False):
            metrics_output = gr.Textbox(
                label="Metrics Sent to AI Model",
                lines=12,
                interactive=False
            )

        gr.Markdown(
            "<div class='footer-note'>Local-only UI • No public sharing • Designed for privacy-focused password coaching</div>"
        )

        analyze_btn.click(
            fn=password_pipeline,
            inputs=[password_input, experience_input],
            outputs=[coaching_output, metrics_output, password_input]
        )

    demo.launch(
        share=False,
        theme=theme,
        css=custom_css
    )


if __name__ == "__main__":
    main()