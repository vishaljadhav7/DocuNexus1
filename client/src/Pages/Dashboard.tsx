import { useAppSelector } from "@/app-store/hooks"


export const Dashboard = () => {
  const data = useAppSelector(store => store.user)
  return (
    <div>
      {JSON.stringify(data)}
    </div>
  )
}
 