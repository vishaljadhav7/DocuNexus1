import { createBrowserRouter } from "react-router-dom";
import { HeroSection, SignIn, SignUp  } from "@/app-components/index";
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
                    element : <HeroSection/>
                },
                {
                    path : "/home",
                    element : <Home/> // protected
                }
            ]
        },
        {
            path : "/sign-up",
            element : <SignUp/>
        },
        {
            path : "/sign-in",
            element : <SignIn/>
        }
    ])
    
    return <>
    <RouterProvider router={appRouter}/>
    </>
}