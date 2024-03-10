"use client";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { cva } from "class-variance-authority";
import Image from "next/image";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { MessageSquareX } from "lucide-react";

const Chat = () => {
  const [messages, setMessages] = useState<
    {
      user: "agent" | "user";
      message: string;
    }[]
  >([{ user: "agent", message: "Hi there! How can I help you today?" }]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const chatVariant = cva("max-w-[90%] rounded-md p-2 text-pretty", {
    variants: {
      variant: {
        user: "bg-primary text-white rounded-br-none ml-auto",
        agent: "bg-secondary text-secondary-foreground rounded-bl-none mr-auto",
      },
    },
  });

  const addMessage = (message: string, user: "agent" | "user") => {
    setMessages((prev) => [...prev, { user, message }]);
  };

  const router = useRouter();
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    addMessage(input, "user");
    setInput("");
    setLoading(true);
    try {
      const response = await fetch("http://localhost:5000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt_input: input, context: messages }),
      });
      const res = await response.json();
      console.log(res);

      addMessage(res["context"], "agent");
    } catch (error) {
      console.error("Error:", error);
      setMessages((prev) => prev.slice(0, -1));
    }
    setLoading(false);
  };

  return (
    <Card className="grid h-full grid-rows-[auto_1fr_auto] overflow-hidden rounded-none border-2">
      <CardHeader className="p-4">
        <CardTitle className="flex items-center gap-4 text-foreground">
          <Image src="/chat.svg" alt="Chat" width={32} height={32} />
          TensionChat
          <Button
            variant="outline"
            className="ml-auto"
            onClick={() => {
              setMessages(() => [
                {
                  user: "agent",
                  message: "Hi there! How can I help you today?",
                },
              ]);
            }}
          >
            <MessageSquareX size={24} color="hsl(263.4 70% 50.4%)" />
          </Button>
        </CardTitle>
      </CardHeader>
      <CardContent className="flex h-full flex-col justify-end gap-2 overflow-y-auto border-y-2 p-2">
        {messages.map((message, index) => (
          <CardDescription
            key={index}
            className={chatVariant({ variant: message.user })}
          >
            {message.message}
          </CardDescription>
        ))}
      </CardContent>
      <CardFooter className="p-4">
        <form className="relative grid w-full" onSubmit={handleSubmit}>
          <Input
            id="chat"
            placeholder="Send a Message..."
            name="chat"
            onChange={(e) => setInput(e.target.value)}
            value={input}
          />
          <Button
            variant="ghost"
            className="absolute right-0 aspect-square p-2"
            type="submit"
          >
            <Image src="/send.svg" alt="Send" width={24} height={24} />
          </Button>
        </form>
      </CardFooter>
    </Card>
  );
};
export default Chat;
