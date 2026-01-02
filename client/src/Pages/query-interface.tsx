import { useState } from "react";
import { useParams } from "react-router-dom";
import { useFetchQueriesQuery, useQueryDocumentMutation } from "@/features/documents/api";
import { ChatMessage, ChatInput, ChatSkeleton, ResponseSkeleton } from "@/app-components";
import { MessageSquare } from "lucide-react";

export const QueryInterface = () => {
  const { document_id }  = useParams();
  const [errorMsg, setErrorMsg] = useState(false)
 const [isSending, setIsSending] = useState(false)
  const {  
    data: queries,
    isLoading: isDocLoading
  } = useFetchQueriesQuery(document_id, { skip: !document_id })


  const [queryDocument] = useQueryDocumentMutation()

  const handleSend = async (message: string) => {
    setIsSending(true)
    if(message.trim() == "" || document_id == undefined) return
    try {
      await queryDocument({query_text : message, document_id}).unwrap()
    } catch (error : any) {
      setErrorMsg(error)
    } finally {
      setIsSending(false)
    }
  }

  return (
      <div className="flex flex-col h-[520px] bg-background">
      {/* Header */}
      <header className="flex-shrink-0   border-b border-border  backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="flex items-center gap-3 px-6 py-4 max-w-4xl mx-auto">
          <div className="h-9 w-9 rounded-lg bg-foreground text-background flex items-center justify-center">
            <MessageSquare className="h-5 w-5" />
          </div>
          <div>
            <h1 className="font-semibold text-foreground">Document Assistant</h1>
            <p className="text-xs text-muted-foreground">Ask questions about your document</p>
          </div>
        </div>
      </header>

      {/* Messages area */}
      <main className="flex-1 overflow-y-auto">
        <div className="max-w-4xl mx-auto py-6">
          {isDocLoading ? (
            <ChatSkeleton />
          ) : queries && queries.length > 0 ? (
            <div className="flex flex-col gap-6 px-4">
              {queries.map((query) => (
                <div key={query.id} className="flex flex-col gap-4">
                  <ChatMessage type="user" content={query.query_text} timestamp={query.created_at} />
                  <ChatMessage type="assistant" content={query.response_text} timestamp={query.created_at} />
                </div>
              ))}
              {isSending && (
                <div className="px-4">
                  <ResponseSkeleton />
                </div>
              )}
            
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center h-full text-center px-4 py-20">
              <div className="h-16 w-16 rounded-2xl bg-muted flex items-center justify-center mb-4">
                <MessageSquare className="h-8 w-8 text-muted-foreground" />
              </div>
              <h2 className="text-lg font-medium text-foreground mb-1">No conversations yet</h2>
              <p className="text-sm text-muted-foreground max-w-sm">
                Start by asking a question about your document below.
              </p>
            </div>
          )}
        </div>
      </main>

      {/* Input area */}
      <footer className="flex-shrink-0 border-t border-border bg-background py-4">
        <ChatInput onSend={handleSend} isLoading={isSending} placeholder="Ask about your document..." />
      </footer>
    </div>
  )
}

 