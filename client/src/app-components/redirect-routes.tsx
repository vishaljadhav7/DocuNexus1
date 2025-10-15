import { useAppSelector } from "@/app-store/hooks";
import { HeroSection } from "./index";
import { Dashboard } from "@/Pages";
import type React from "react";


export const ProtectedRoute = ({children} : { children : React.ReactNode}) => {
    const user = useAppSelector(store => store.user);
  return (
     <>
      {user.isAuthenticated ? children : <HeroSection/> }
     </>
  )
}

 
export const RedirectRoute = ({children} : { children : React.ReactNode}) => {
    const user = useAppSelector(store => store.user);
  return (
     <>
      {user.isAuthenticated ? <Dashboard/> : children }
     </>
  )
}