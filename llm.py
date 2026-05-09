import os
import subprocess
from typing import List


def _get_model() -> str:
    return os.environ.get("OLLAMA_MODEL", "qwen2.5:3b")


def summarize_news(articles: List[dict]) -> str:
    if not articles:
        return "No articles to summarize."

    model = _get_model()
    prompt_lines = [
        "You are a concise news assistant. Summarize the following articles into a short briefing, key themes, and 4–5 bullet points.",
        "Use plain language and keep it local-first.",
        "",
        "Articles:",
    ]

    for index, article in enumerate(articles, start=1):
        prompt_lines.append(f"{index}. {article['title']}")
        prompt_lines.append(f"Link: {article['link']}")
        prompt_lines.append(f"{article['description']}")
        prompt_lines.append("")

    prompt_lines.append("Output:")
    prompt = "\n".join(prompt_lines)

    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt,
            text=True,
            capture_output=True
        )
        return result.stdout.strip() or "No summary returned from the model."
    except subprocess.CalledProcessError as exc:
        return f"Ollama failed: {exc.stderr.strip() or exc}"  # type: ignore
    except FileNotFoundError:
        return "Ollama is not installed or not available in PATH."
    except subprocess.TimeoutExpired:
        return "Ollama request timed out."
