import { createClient } from "@/utils/supabase/server";
import { redirect } from "next/navigation";
import AuthButton from "@/components/AuthButton";
import { Navbar } from "@/components/Navbar";
import Chat from "@/components/Chat";

const layout = ({ children }: { children: React.ReactNode }) => {
  const supabase = createClient();
  const user = supabase.auth.getUser();
  if (!user) return redirect("/login");
  return (
    <div className="grid grid-rows-[auto_1fr]">
      <header className="flex w-full justify-between bg-neutral-900 px-4 py-2">
        <Navbar />
        <AuthButton />
      </header>
      <main className="grid grid-cols-[5fr_2fr]">
        <div className="p-4">{children}</div>
        <Chat />
      </main>
    </div>
  );
};
export default layout;
