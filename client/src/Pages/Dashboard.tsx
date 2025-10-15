import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppSidebar } from "@/app-components/index";
import { FileUploadCard } from "@/app-components/file-uploader-card";

export const Dashboard = () => {
  return (
    <SidebarWrapper>
      <div className="h-full bg-gray-50 flex items-center justify-center p-4">
        <FileUploadCard />
      </div>
    </SidebarWrapper>
  );
};

export const SidebarWrapper = ({ children }: { children: React.ReactNode }) => {
  return (
    <SidebarProvider>
      <AppSidebar />
      <main className="w-full m-2">
        <div className="border-sidebar-border bg-sidebar border shadow rounded-md overflow-y-scroll h-full p-4">
          <SidebarTrigger />
          {children}
        </div>
      </main>
    </SidebarProvider>
  );
};
