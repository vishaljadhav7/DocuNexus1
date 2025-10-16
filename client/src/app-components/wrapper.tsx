import { ProtectedRoute } from "./redirect-routes"
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppSidebar } from "./app-sidebar";


export const Wrapper = ({ children }: { children: React.ReactNode }) => {
  return (
  <ProtectedRoute>
    <SidebarProvider>
      <AppSidebar />
      <main className="w-full m-2">
        <div className="border-sidebar-border bg-sidebar border shadow rounded-md overflow-y-scroll h-full p-4">
          <SidebarTrigger />
          {children}
        </div>
      </main>
    </SidebarProvider>
  </ProtectedRoute>
  );
};
