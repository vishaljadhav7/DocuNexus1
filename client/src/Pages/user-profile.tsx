import { useAppSelector } from "@/app-store/hooks"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"

import { Badge } from "@/components/ui/badge"
import { Mail, Calendar, Hash } from "lucide-react"

export const UserProfile = () => {
  const user = useAppSelector((store) => store.user.userInfo)

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    })
  }

  const getInitials = (name: string) => {
    return name
      .split(" ")
      .map((n) => n[0])
      .join("")
      .toUpperCase()
      .slice(0, 2)
  }

  if (!user) return null

  return (
    <div className="w-full max-w-md mx-auto">
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-primary/5 via-background to-secondary/10 border border-border/50 backdrop-blur-sm">
        {/* Header accent */}
        <div className="absolute top-0 left-0 right-0 h-24 bg-gradient-to-r from-primary/10 to-primary/5" />

        <div className="relative px-6 pt-8 pb-6">
          {/* Avatar section */}
          <div className="flex flex-col items-center mb-6">
            <Avatar className="h-20 w-20 ring-4 ring-background shadow-lg">
              <AvatarFallback className="bg-primary text-primary-foreground text-xl font-semibold">
                {getInitials(user.username)}
              </AvatarFallback>
            </Avatar>
            <h2 className="mt-4 text-xl font-semibold text-foreground">{user.username}</h2>
            <Badge variant="secondary" className="mt-2">
              Member
            </Badge>
          </div>

          {/* Info rows */}
          <div className="space-y-4">
            <div className="flex items-center gap-3 p-3 rounded-xl bg-muted/50 transition-colors hover:bg-muted/80">
              <div className="flex items-center justify-center h-10 w-10 rounded-lg bg-primary/10">
                <Mail className="h-5 w-5 text-primary" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide">Email</p>
                <p className="text-sm font-medium text-foreground truncate">{user.email}</p>
              </div>
            </div>

            <div className="flex items-center gap-3 p-3 rounded-xl bg-muted/50 transition-colors hover:bg-muted/80">
              <div className="flex items-center justify-center h-10 w-10 rounded-lg bg-primary/10">
                <Calendar className="h-5 w-5 text-primary" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide">Joined</p>
                <p className="text-sm font-medium text-foreground">{formatDate(user.created_at)}</p>
              </div>
            </div>

            <div className="flex items-center gap-3 p-3 rounded-xl bg-muted/50 transition-colors hover:bg-muted/80">
              <div className="flex items-center justify-center h-10 w-10 rounded-lg bg-primary/10">
                <Hash className="h-5 w-5 text-primary" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide">User ID</p>
                <p className="text-xs font-mono text-muted-foreground truncate">{user.id}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
