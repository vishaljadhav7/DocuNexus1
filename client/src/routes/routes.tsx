import { createBrowserRouter } from "react-router-dom";
import { HeroSection,  Wrapper, RedirectRoute} from "@/app-components/index";
import { Layout, SignIn, SignUp,  Dashboard, DocumentViewer, QueryInterface, UserProfile } from "@/Pages/index";
import { RouterProvider } from "react-router-dom";

export const AppRoutes = () => {
    const appRouter = createBrowserRouter([
        {
            path : "/",
            element : <Layout/>,
            children : [
                {
                    path : "/",
                    element : <RedirectRoute><HeroSection/></RedirectRoute>
                },
                {
                    path : "/dashboard",
                    element : <Wrapper> <Dashboard/> </Wrapper>  
                },
                {
                    path : "/document/:document_id",
                    element : <Wrapper> <DocumentViewer/></Wrapper> 
                },
                {
                    path : "/document/:document_id/chat",
                    element : <Wrapper> <QueryInterface/> </Wrapper> 
                },
                {
                    path : "/user",
                    element : <Wrapper><UserProfile/></Wrapper>
                }
            ]
        },
        {
            path : "/sign-up",
            element : <RedirectRoute> <SignUp/> </RedirectRoute>
        },
        {
            path : "/sign-in",
            element : <RedirectRoute><SignIn/></RedirectRoute>
        }
    ])
    
    return <>
    <RouterProvider router={appRouter}/>
    </>
}