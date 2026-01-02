export function ChatSkeleton() {
  return (
    <div className="flex flex-col gap-6 p-4 animate-pulse">
      {/* User message skeleton */}
      <div className="flex justify-end">
        <div className="max-w-[70%] space-y-2">
          <div className="h-4 w-48 bg-muted rounded-lg shimmer" />
          <div className="h-4 w-32 bg-muted rounded-lg shimmer" />
        </div>
      </div>

      {/* AI response skeleton */}
      <div className="flex justify-start">
        <div className="flex gap-3 max-w-[70%]">
          <div className="h-8 w-8 rounded-full bg-muted shimmer flex-shrink-0" />
          <div className="space-y-2 flex-1">
            <div className="h-4 w-full bg-muted rounded-lg shimmer" />
            <div className="h-4 w-[90%] bg-muted rounded-lg shimmer" />
            <div className="h-4 w-[80%] bg-muted rounded-lg shimmer" />
            <div className="h-4 w-[60%] bg-muted rounded-lg shimmer" />
          </div>
        </div>
      </div>

      {/* User message skeleton */}
      <div className="flex justify-end">
        <div className="max-w-[70%] space-y-2">
          <div className="h-4 w-56 bg-muted rounded-lg shimmer" />
        </div>
      </div>

      {/* AI response skeleton */}
      <div className="flex justify-start">
        <div className="flex gap-3 max-w-[70%]">
          <div className="h-8 w-8 rounded-full bg-muted shimmer flex-shrink-0" />
          <div className="space-y-2 flex-1">
            <div className="h-4 w-full bg-muted rounded-lg shimmer" />
            <div className="h-4 w-[85%] bg-muted rounded-lg shimmer" />
            <div className="h-4 w-[70%] bg-muted rounded-lg shimmer" />
          </div>
        </div>
      </div>
    </div>
  )
}

export function ResponseSkeleton() {
  return (
    <div className="flex justify-start animate-pulse">
      <div className="flex gap-3 max-w-[70%]">
        <div className="h-8 w-8 rounded-full bg-muted shimmer flex-shrink-0" />
        <div className="space-y-2 flex-1 min-w-[300px]">
          <div className="h-4 w-full bg-muted rounded-lg shimmer" />
          <div className="h-4 w-[90%] bg-muted rounded-lg shimmer" />
          <div className="h-4 w-[75%] bg-muted rounded-lg shimmer" />
        </div>
      </div>
    </div>
  )
}
