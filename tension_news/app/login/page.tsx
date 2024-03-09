import Link from "next/link";
import { headers } from "next/headers";
import { createClient } from "@/utils/supabase/server";
import { redirect } from "next/navigation";
import { SubmitButton } from "./submit-button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

export default function Login({
  searchParams,
}: {
  searchParams: { message: string };
}) {
  const signIn = async (formData: FormData) => {
    "use server";

    const email = formData.get("email") as string;
    const password = formData.get("password") as string;
    const supabase = createClient();

    const { error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });

    if (error) {
      return redirect("/login?message=Could not authenticate user");
    }

    return redirect("/dashboard");
  };

  const signUp = async (formData: FormData) => {
    "use server";

    const origin = headers().get("origin");
    const email = formData.get("email") as string;
    const password = formData.get("password") as string;
    const firstName = formData.get("first-name") as string;
    const lastName = formData.get("last-name") as string;
    const supabase = createClient();

    const { error } = await supabase.auth.signUp({
      email,
      password,

      options: {
        emailRedirectTo: `${origin}/auth/callback`,
        data: {
          firstName,
          lastName,
        },
      },
    });

    if (error) {
      return redirect("/login?message=Could not authenticate user");
    }

    return redirect("/dashboard");
  };

  return (
    <main className="relative grid h-full grid-rows-[auto_1fr_auto] place-items-center gap-2 p-8 pb-12">
      <Link
        href="/"
        className="bg-btn-background hover:bg-btn-background-hover group absolute left-8 top-8 flex items-center rounded-md px-4 py-2 text-sm text-foreground no-underline"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="mr-2 h-4 w-4 transition-transform group-hover:-translate-x-1"
        >
          <polyline points="15 18 9 12 15 6" />
        </svg>{" "}
        Back
      </Link>

      <h1 className="text-center text-foreground animate-in">
        <span className="text-4xl font-bold">Welcome to</span>{" "}
        <span className="text-4xl font-bold text-primary">TensionNews</span>
      </h1>
      <Tabs defaultValue="login" className="grid w-96 gap-4">
        <TabsList className="grid grid-cols-2">
          <TabsTrigger value="login">Account</TabsTrigger>
          <TabsTrigger value="signup">Password</TabsTrigger>
        </TabsList>
        <TabsContent value="login">
          <form className="grid grid-cols-2 gap-4 text-foreground animate-in">
            <Label className="text-md col-span-2" htmlFor="email">
              Email
              <Input
                className="rounded-md border bg-inherit px-4 py-2"
                name="email"
                placeholder="you@example.com"
                required
              />
            </Label>
            <Label className="text-md col-span-2" htmlFor="password">
              Password
              <Input
                className="rounded-md border bg-inherit px-4 py-2"
                type="password"
                name="password"
                placeholder="••••••••"
                required
              />
            </Label>
            <SubmitButton
              formAction={signIn}
              pendingText="Signing In..."
              className="col-span-2 mt-4 grid gap-2"
            >
              Sign In
            </SubmitButton>
          </form>
        </TabsContent>
        <TabsContent value="signup">
          <form className="grid w-96 grid-cols-2 gap-4 text-foreground animate-in">
            <Label className="text-md" htmlFor="first-name">
              First Name
              <Input
                className="rounded-md border bg-inherit px-4 py-2"
                name="first-name"
                placeholder="John"
                required
              />
            </Label>
            <Label className="text-md" htmlFor="last-name">
              Last Name
              <Input
                className="rounded-md border bg-inherit px-4 py-2"
                name="last-name"
                placeholder="Doe"
                required
              />
            </Label>
            <Label className="text-md col-span-2" htmlFor="email">
              Email
              <Input
                className="rounded-md border bg-inherit px-4 py-2"
                name="email"
                placeholder="you@example.com"
                required
              />
            </Label>
            <Label className="text-md col-span-2" htmlFor="password">
              Password
              <Input
                className="rounded-md border bg-inherit px-4 py-2"
                type="password"
                name="password"
                placeholder="••••••••"
                required
              />
            </Label>

            <SubmitButton
              formAction={signUp}
              pendingText="Signing Up..."
              className="col-span-2 mt-4 grid gap-2"
            >
              Sign Up
            </SubmitButton>
          </form>
        </TabsContent>
      </Tabs>
      {searchParams?.message && (
        <p className="w-full max-w-md rounded-md bg-primary/30 p-4 text-center text-foreground">
          {searchParams.message}
        </p>
      )}
    </main>
  );
}
