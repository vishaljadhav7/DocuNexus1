import { SidebarProvider , SidebarTrigger} from "@/components/ui/sidebar";
import { AppSidebar } from "@/app-components/index";

export const Dashboard = () => {  
//  const data = useAppSelector(store => store.user.userInfo)

  return (
    <SidebarWrapper>
    <div className="h-full bg-gray-50 flex items-center justify-center p-4">
    {/* {JSON.stringify(data)} */}
   </div>
    </SidebarWrapper>
  );
}


export const SidebarWrapper = ({ children }: { children: React.ReactNode }) => {

  return (
    <SidebarProvider>
      <AppSidebar/>
      <main className="w-full m-2">
        <div className="border-sidebar-border bg-sidebar border shadow rounded-md overflow-y-scroll h-full p-4">
        <SidebarTrigger />
          {children}
        </div>
      </main>
    </SidebarProvider>
  );
}
 
 
