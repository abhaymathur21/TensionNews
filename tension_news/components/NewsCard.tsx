import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import Image from "next/image";
import Link from "next/link";
import { type Article } from "@/lib/types";

const NewsCard = ({ article }: { article: Article }) => {
  return (
    <Card>
      <CardHeader className="grid grid-cols-[auto_1fr] grid-rows-2 gap-x-4">
        <Image
          src={article.thumbnail}
          alt={article.title}
          width={100}
          height={100}
          className="row-span-2 place-self-center rounded-md object-contain"
        />
        <CardTitle className="line-clamp-2 text-sm">{article.title}</CardTitle>
        <CardDescription className="line-clamp-1 text-xs">
          {article.snippet}
        </CardDescription>
      </CardHeader>

      <CardFooter className="flex w-full items-center justify-between gap-4 rounded-b-md bg-gray-100 px-4 py-2 text-sm text-gray-500">
        <a
          href={article.link}
          target="_blank"
          rel="noopener noreferrer"
          className="text-primary"
        >
          {article.source}
        </a>
        <span className="text-gray-500">{article.date}</span>
      </CardFooter>
    </Card>
  );
};

export default NewsCard;
