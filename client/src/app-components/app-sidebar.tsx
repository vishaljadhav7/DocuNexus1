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
// useFetchProjectsQuery
import { useFetchAllDocumentsQuery } from "@/features/documents/api";
import axios from "axios";
// import { DocumentListResponse } from "@/features/documents/types";

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
  const location = useLocation(); //
  const pathName = location.pathname;
  const dispatch = useAppDispatch();
  const router = useNavigate();
  const userInfo = useAppSelector((store) => store.user.userInfo);
  const { open } = useSidebar();
  // const {data : projects, isLoading} = useFetchAllProjectsQuery();
  const projects  = [
        {
            "id": "ab993c3c-4131-4b7e-84ec-5aee131312be",
            "filename": "Profile",
            "user_id": "59fafedc-6ea7-4c8f-ac03-4082918b8fd6",
            "file_size": 46581,
            "cloudinary_url": "https://res.cloudinary.com/dhg1hqsnn/raw/upload/v1760437085/rag_documents/59fafedc-6ea7-4c8f-ac03-4082918b8fd6/Profile.pdf",
            "cloudinary_public_id": "rag_documents/59fafedc-6ea7-4c8f-ac03-4082918b8fd6/Profile.pdf",
            "processing_status": "uploaded",
            "created_at": "2025-10-14T10:18:02.730966Z",
            "updated_at": "2025-10-14T10:18:02.730966Z"
        },
        {
            "id": "ae0d14b9-c016-4908-af01-3e302b71641d",
            "filename": "vishal resume web_dev",
            "user_id": "59fafedc-6ea7-4c8f-ac03-4082918b8fd6",
            "file_size": 650070,
            "cloudinary_url": "https://res.cloudinary.com/dhg1hqsnn/raw/upload/v1760437049/rag_documents/59fafedc-6ea7-4c8f-ac03-4082918b8fd6/vishal%20resume%20web_dev.pdf",
            "cloudinary_public_id": "rag_documents/59fafedc-6ea7-4c8f-ac03-4082918b8fd6/vishal resume web_dev.pdf",
            "processing_status": "uploaded",
            "created_at": "2025-10-14T10:17:24.252876Z",
            "updated_at": "2025-10-14T10:17:24.252876Z"
        },
        {
            "id": "fa667700-38b5-4dbc-8b5e-31d85986999e",
            "filename": "vishal rez new",
            "user_id": "59fafedc-6ea7-4c8f-ac03-4082918b8fd6",
            "file_size": 650070,
            "cloudinary_url": "https://res.cloudinary.com/dhg1hqsnn/raw/upload/v1760347390/rag_documents/59fafedc-6ea7-4c8f-ac03-4082918b8fd6/vishal%20rez%20new.pdf",
            "cloudinary_public_id": "rag_documents/59fafedc-6ea7-4c8f-ac03-4082918b8fd6/vishal rez new.pdf",
            "processing_status": "uploaded",
            "created_at": "2025-10-14T10:16:31.880710Z",
            "updated_at": "2025-10-14T10:16:31.880710Z"
        },
        {
            "id": "a42de22e-a757-484e-bd75-004827076781",
            "filename": "vishal rez new",
            "user_id": "59fafedc-6ea7-4c8f-ac03-4082918b8fd6",
            "file_size": 650070,
            "cloudinary_url": "https://res.cloudinary.com/dhg1hqsnn/raw/upload/v1760347390/rag_documents/59fafedc-6ea7-4c8f-ac03-4082918b8fd6/vishal%20rez%20new.pdf",
            "cloudinary_public_id": "rag_documents/59fafedc-6ea7-4c8f-ac03-4082918b8fd6/vishal rez new.pdf",
            "processing_status": "completed",
            "created_at": "2025-10-13T09:51:22.322251Z",
            "updated_at": "2025-10-13T09:52:51.530963Z"
        }
    ];
  

  const {data , isLoading} =  useFetchAllDocumentsQuery()

   console.log("data from sidebar =>>>>>", data)

  const handleLogout = async () => {
    try {
      await axios.post(
        `${import.meta.env.BASE_URL}/sign-out`,
        {},
        {
          withCredentials: true,
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
                  {projects?.map((project) => {
                    return (
                      <SidebarMenuItem key={project.id} className="list-none">
                        <SidebarMenuButton>
                          <Link to={`/project/${project.id}`} key={project.id}>
                            <div className="flex items-center  gap-2">
                              <div
                                className={cn(
                                  "rounded-sm border size-6 flex items-center justify-center text-sm bg-white text-primary",
                                  {
                                    "bg-primary text-white":
                                      `/project/${project.id}` === pathName,
                                  }
                                )}
                              >
                                {project.filename.charAt(0).toUpperCase()}
                              </div>
                              <span>{project.filename}</span>
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
