import { createBrowserRouter } from "react-router-dom";
import { HeroSection, SignIn, SignUp, ProtectedRoute, RedirectRoute} from "@/app-components/index";
import { Layout, Home } from "@/Pages/index";
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
                    path : "/home",
                    element : <ProtectedRoute> <Home/> </ProtectedRoute>  
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