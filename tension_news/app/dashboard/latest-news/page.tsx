const LatestNews = ({
  searchParams: { q },
}: {
  searchParams: { q: string };
}) => {
  return (
    <div>
      LatestNews
      {q && <div>Search: {q}</div>}
    </div>
  );
};
export default LatestNews;
