import type React from "react"

import { useState } from "react"
import { SendHorizonal } from "lucide-react"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

interface ChatInputProps {
  onSend: (message: string) => void
  isLoading?: boolean
  placeholder?: string
}

export function ChatInput({ onSend, isLoading = false, placeholder = "Ask a question..." }: ChatInputProps) {
  const [input, setInput] = useState("")


  const handleSubmit = () => {
    if (input.trim() && !isLoading) {
      onSend(input.trim())
      setInput("")
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }


  return (
    <div className="w-full max-w-3xl mx-auto px-4">
      <div className="relative flex items-end gap-2 bg-muted/50 border border-border rounded-2xl p-2 shadow-sm transition-shadow focus-within:shadow-md focus-within:border-foreground/20">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          disabled={isLoading}
          rows={1}
          className={cn(
            "flex-1 resize-none bg-transparent px-3 py-2 text-sm outline-none placeholder:text-muted-foreground",
            "min-h-[40px] max-h-[150px]",
          )}
        />
        <Button
          size="icon"
          onClick={handleSubmit}
          disabled={!input.trim() || isLoading}
          className={cn(
            "h-9 w-9 rounded-xl transition-all",
            input.trim() ? "bg-foreground text-background hover:bg-foreground/90" : "bg-muted text-muted-foreground",
          )}
        >
          <SendHorizonal className="h-4 w-4" />
          <span className="sr-only">Send message</span>
        </Button>
      </div>
      <p className="text-[10px] text-muted-foreground text-center mt-2">
        Press Enter to send, Shift + Enter for new line
      </p>
    </div>
  )
}
