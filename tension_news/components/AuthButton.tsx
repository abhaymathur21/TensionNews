import { createClient } from "@/utils/supabase/server";
import Link from "next/link";
import { redirect } from "next/navigation";
import { Button } from "@/components/ui/button";

export default async function AuthButton() {
  const supabase = createClient();

  const {
    data: { user },
  } = await supabase.auth.getUser();

  const signOut = async () => {
    "use server";

    const supabase = createClient();
    await supabase.auth.signOut();
    return redirect("/login");
  };

  return user ? (
    <div className="flex w-64 items-center justify-end gap-4">
      Hey, {user.user_metadata.firstName} {user.user_metadata.lastName}!
      <form action={signOut}>
        <Button size="sm">Logout</Button>
      </form>
    </div>
  ) : (
    <Button variant="default" size="sm">
      <Link href="/login">Login</Link>
    </Button>
  );
}
