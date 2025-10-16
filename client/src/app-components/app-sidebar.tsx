import { useNavigate, useLocation, Link } from "react-router-dom";
import {
  LayoutDashboard,
  UserCog,
  CreditCard,
  ChevronUp,
  User2,
  Loader2,
  Plus,
} from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenuItem,
  SidebarMenuButton,
  SidebarMenu,
  SidebarFooter,
  useSidebar,
} from "@/components/ui/sidebar";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { useAppDispatch, useAppSelector } from "@/app-store/hooks";
import { removeUser } from "@/features/user/userSlice";
import { useFetchAllDocumentsQuery } from "@/features/documents/api";
import axios from "axios";

const sidebarItems = [
  {
    title: "Dashboard",
    path: "/dashboard",
    icon: LayoutDashboard,
  },
  {
    title: "User",
    path: "/user-profile",
    icon: UserCog,
  },
  {
    title: "Billing",
    path: "/billing",
    icon: CreditCard,
  },
];

export const AppSidebar = () => {
  const location = useLocation(); 
  const pathName = location.pathname;
  const dispatch = useAppDispatch();
  const router = useNavigate();
  const userInfo = useAppSelector((store) => store.user.userInfo);
  const { open } = useSidebar();

  const {data , isLoading} =  useFetchAllDocumentsQuery()

  const handleLogout = async () => {
    try {
      await axios.post(
        `${import.meta.env.VITE_API_URL}/sign_out`,
        {},
        {
          withCredentials: true,
          headers : {
            'Authorization': `Bearer ${userInfo?.access_token}`,
          }
        }
      );
      dispatch(removeUser());
      router("/");
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <Sidebar collapsible="icon" variant="floating">
      <SidebarHeader>
        <div className="flex items-center p-2">
          {!open && (
            <span className="text-xl font-bold text-purple-400 ">DN</span>
          )}
          {open && (
            <span className="text-xl font-bold text-slate-900 ">DocuNexus</span>
          )}
        </div>
      </SidebarHeader>

      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Application</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {sidebarItems.map((item) => {
                return (
                  <SidebarMenuItem key={item.path} className="list-none">
                    <SidebarMenuButton asChild>
                      <Link
                        className={
                          pathName == item.path ? `bg-primary text-white` : ""
                        }
                        to={item.path}
                      >
                        <item.icon />
                        <span>{item.title}</span>
                      </Link>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                );
              })}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>

         <SidebarGroup>
          <SidebarGroupLabel>Projects</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {isLoading ? (
                <Loader2 className="animate-spin text-center ml-6" />
              ) : (
                <>
                  {data?.documents?.map((document) => {
                    return (
                      <SidebarMenuItem key={document.id} className="list-none">
                        <SidebarMenuButton>
                          <Link to={`/document/${document.id}`} key={document.id}>
                            <div className="flex items-center gap-2">
                              <div
                                className={cn(
                                  "rounded-sm border size-6 flex items-center justify-center text-sm bg-white text-primary",
                                  {
                                    "bg-primary text-white":
                                      `/document/${document.id}` === pathName,
                                  }
                                )}
                              >
                                {document.filename.charAt(0).toUpperCase()}
                              </div>
                              <span>{document.filename}</span>
                            </div>
                          </Link>
                        </SidebarMenuButton>
                      </SidebarMenuItem>
                    );
                  })}
                </>
              )}
            </SidebarMenu>
            <Button className="mt-3" size={"sm"} variant={"outline"}>
              <Plus />
              {open && "Create Project"}
            </Button>
          </SidebarGroupContent>
        </SidebarGroup> 

        <SidebarFooter className="mb-2 relative">
          <SidebarMenu>
            <SidebarMenuItem>
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <SidebarMenuButton>
                    <User2 /> {userInfo?.username}
                    <ChevronUp className="ml-auto" />
                  </SidebarMenuButton>
                </DropdownMenuTrigger>
                <DropdownMenuContent
                  side="top"
                  className="w-[220px] absolute bottom-2"
                >
                  <Link to={"/billing"}>
                    <DropdownMenuItem>
                      <span>Billing</span>
                    </DropdownMenuItem>
                  </Link>

                  <DropdownMenuItem onClick={handleLogout}>
                    <span>Sign out</span>
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarFooter>
      </SidebarContent>
    </Sidebar>
  );
};
