import { configureStore } from '@reduxjs/toolkit'
import userReducer from '../features/user/userSlice'
import { api } from '@/features/documents/api'

export const store = configureStore({
  reducer: {
    user : userReducer,
    [api.reducerPath] : api.reducer
  },
  middleware: (getDefault) => getDefault().concat(api.middleware),
})

// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>


// Inferred type: {posts: PostsState, comments: CommentsState, users: UsersState}
export type AppDispatch = typeof store.dispatch