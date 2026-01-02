import { cn } from "@/lib/utils"
import { Bot, User } from "lucide-react"

interface ChatMessageProps {
  type: "user" | "assistant"
  content: string
  timestamp?: Date
}

export function ChatMessage({ type, content, timestamp }: ChatMessageProps) {
  const isUser = type === "user"

  return (
    <div className={cn("flex w-full", isUser ? "justify-end" : "justify-start")}>
      <div className={cn("flex gap-3 max-w-[75%] md:max-w-[70%]", isUser && "flex-row-reverse")}>
        {/* Avatar */}
        <div
          className={cn(
            "h-8 w-8 rounded-full flex items-center justify-center flex-shrink-0 shadow-sm",
            isUser ? "bg-foreground text-background" : "bg-muted text-muted-foreground",
          )}
        >
          {isUser ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
        </div>

        {/* Message content */}
        <div className="flex flex-col gap-1">
          <div
            className={cn(
              "px-4 py-3 rounded-2xl text-sm leading-relaxed",
              isUser ? "bg-foreground text-background rounded-tr-sm" : "bg-muted text-foreground rounded-tl-sm",
            )}
          >
            <p className="whitespace-pre-wrap">{content}</p>
          </div>
          {timestamp && (
            <span className={cn("text-[10px] text-muted-foreground px-2", isUser ? "text-right" : "text-left")}>
              {new Date(timestamp).toLocaleTimeString([], {
                hour: "2-digit",
                minute: "2-digit",
              })}
            </span>
          )}
        </div>
      </div>
    </div>
  )
}
