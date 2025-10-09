import { Header } from "@/app-components/index"
import { Outlet } from "react-router-dom"

export const Layout = () => {
  return (
    <>
       <Header/>
       <Outlet/>
    </>
  )
} 