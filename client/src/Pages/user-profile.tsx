import { useAppSelector } from '@/app-store/hooks'

export const UserProfile = () => {
    const user = useAppSelector((store) => store.user.userInfo)
  return (
    <div>
        {JSON.stringify(user)}
    </div>
  )
}
