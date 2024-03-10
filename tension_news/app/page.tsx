import AuthButton from "@/components/AuthButton";
import { Button } from "@/components/ui/button";
import { createClient } from "@/utils/supabase/server";
import Link from "next/link";

export default async function Index() {
  const client = createClient();
  const user = await client.auth.getUser();
  return (
    <main className="relative grid h-full grid-rows-[auto_1fr] place-items-center gap-2 px-8">
      <h1 className="mt-8 text-center text-foreground animate-in">
        <span className="text-4xl font-bold">Welcome to</span>{" "}
        <span className="text-4xl font-bold text-primary">TensionNews</span>
      </h1>
      <div className="grid place-items-center gap-4">
        <AuthButton />
        {user && (
          <Button>
            <Link href="/dashboard/latest-news">Dashboard</Link>
          </Button>
        )}
      </div>
    </main>
  );
}
