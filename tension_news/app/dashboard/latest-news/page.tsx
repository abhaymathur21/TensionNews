import NewsCard from "@/components/NewsCard";
import { type Article } from "@/lib/types";

const sites = [
  "economictimes.indiatimes.com",
  "livemint.com",
  "hindustantimes.com",
  "bloombergquint.com",
  "moneycontrol.com",
  "ndtv.com",
  "businesstoday.in",
  "financialexpress.com",
  "thehindubusinessline.com",
  "firstpost.com",
  "moneylife.in",
  "dsij.in",
  "zeebiz.com",
  "businessworld.in",
  "goodreturns.in",
  "investing.com",
  "indiainfoline.com",
];

const fetchArticles = async (query: string) => {
  // https://serpapi.com/search.json?engine=google&q=business+finance+news&api_key=c3ca09050618bf14418bb5cfb3837bd0229c5fafb7257183470bac607100831c&tbm=nws&num=100
  const url = new URL("https://serpapi.com/search.json");
  url.searchParams.append("engine", "google");
  url.searchParams.append("q", query);
  url.searchParams.append("tbm", "nws");
  url.searchParams.append("num", "5");
  url.searchParams.append(
    "api_key",
    process.env.NEXT_PUBLIC_SERP_API_KEY as string,
  );
  const response = await fetch(url.toString());
  const res = await response.json();
  return res["news_results"];
};

const LatestNews = async ({
  searchParams: { q },
}: {
  searchParams: { q: string };
}) => {
  const articles = await Promise.all(
    sites.map(async (site) => {
      const query = `${q || "business+finance+news"} site:${site}`;
      const articles = await fetchArticles(query);
      return articles satisfies Article[];
    }),
  )
    .then((res) => res.flat() satisfies Article[])
    .then((res: Article[]) =>
      res.map((article) => {
        const [_, n, d] = article.date.match(/(\d+) (\w+) ago/) || [];
        const convertDict: { [key: string]: number } = {
          seconds: 1,
          minutes: 60,
          hours: 3600,
          days: 86400,
          weeks: 604800,
          months: 2628000,
          years: 31536000,
        };

        if (!d)
          return {
            ...article,
            date: new Date(article.date).toLocaleString("en-IN", {
              dateStyle: "long",
            }),
          };

        const delta = convertDict[d] * parseInt(n) * 1000 || 0;
        const date = new Date(Date.now() - delta).toLocaleString("en-IN", {
          dateStyle: "long",
        });
        return {
          ...article,
          date,
        };
      }),
    )
    .then((res) =>
      res.sort(
        (a, b) => new Date(b.date).getTime() - new Date(a.date).getTime(),
      ),
    );

  // console.log(articles);

  return (
    <>
      <h1 className="mb-4 px-4 text-2xl font-bold text-primary">Latest News</h1>
      <div className="flex max-h-[80vh] flex-col gap-4 overflow-y-auto px-4">
        {articles.map((article: any) => (
          <NewsCard
            article={article}
            key={`${article.source} ${article.position}`}
          />
        ))}
      </div>
    </>
  );
};

export default LatestNews;
