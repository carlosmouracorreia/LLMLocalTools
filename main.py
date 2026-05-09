from news import fetch_news
from llm import summarize_news


def main() -> None:
    articles = fetch_news()

    print("\nToday's News Briefing\n")
    if not articles:
        print("No recent headlines were found. Check your network or feed URLs.")
        return

    print("Top headlines:")
    for index, article in enumerate(articles, start=1):
        print(f"{index}. {article['title']}")
        print(f"   {article['link']}")
    print()

    briefing = summarize_news(articles)
    print(briefing)


if __name__ == "__main__":
    main()
