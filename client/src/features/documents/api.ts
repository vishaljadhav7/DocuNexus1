import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import type {DocumentUploadResponse, DocumentListResponse, DocumentListItem, DocumentDeleteResponse, DocumentStatusResponse} from './types'
import { useAppSelector } from "@/app-store/hooks";


export const api = createApi({
    reducerPath : "api",
    baseQuery : fetchBaseQuery({baseUrl : import.meta.env.VITE_API_URL}),
    endpoints : (build) => ({
        fetchAllDocuments : build.query<DocumentListResponse, void>({
            query : () => '/documents'
        }),

        getDocumentStatus : build.query<DocumentStatusResponse, {document_id : {document_id : string}}>({
            query : ({document_id}) => `/${document_id}/status`
        }),
        
        deleteDocument : build.mutation<DocumentDeleteResponse, {document_id : {document_id : string}}>({
             query : ({document_id}) => ({
                url : `/${document_id}`,
                method : "DELETE"
             }),
             
        })
    })
})