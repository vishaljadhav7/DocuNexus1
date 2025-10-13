import { createBrowserRouter } from "react-router-dom";
import { HeroSection,  ProtectedRoute, RedirectRoute} from "@/app-components/index";
import { Layout, SignIn, SignUp,  Dashboard } from "@/Pages/index";
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
                    element : <ProtectedRoute> <Dashboard/> </ProtectedRoute>  
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