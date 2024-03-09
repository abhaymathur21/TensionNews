import AuthButton from "@/components/AuthButton";

export default async function Index() {
  return (
    <main className="relative grid h-full grid-rows-[auto_1fr] place-items-center gap-2 px-8">
      <h1 className="mt-8 text-center text-foreground animate-in">
        <span className="text-4xl font-bold">Welcome to</span>{" "}
        <span className="text-4xl font-bold text-primary">TensionNews</span>
      </h1>
      <div className="grid">
        <AuthButton />
      </div>
    </main>
  );
}
