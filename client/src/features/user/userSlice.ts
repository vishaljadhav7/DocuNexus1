import { createSlice } from "@reduxjs/toolkit";
import type { PayloadAction } from "@reduxjs/toolkit";


export interface IUser {
  id: string;
  email: string;
  userName: string | null;
  profileUrl? : string;
  createdAt: Date;
  credits : number;
//myDocs? : []
}

export interface userStatus{
    userInfo : IUser | null;
    isAuthenticated : boolean
}

const initialState : userStatus = {
    userInfo : null,
    isAuthenticated : false
}
 
 const userSlice = createSlice({
    name : "userSlice",
    initialState,
    reducers : {
       addUser : (state, action: PayloadAction<IUser>) => {
        state.isAuthenticated = true; 
        state.userInfo = action.payload;   
       },
       removeUser : (state)  => {
        state.isAuthenticated = false;
        state.userInfo = null;
       }
    }
 });


 export const {addUser, removeUser} = userSlice.actions

 export default userSlice.reducer