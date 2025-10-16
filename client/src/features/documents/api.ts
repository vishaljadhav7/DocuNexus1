import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import type {
  DocumentUploadResponse,
  DocumentListResponse,
  DocumentListItem,
  DocumentDeleteResponse,
  DocumentStatusResponse
} from './types';
import type { RootState } from '@/app-store/store';

export const api = createApi({
  reducerPath: "api",
  baseQuery: fetchBaseQuery({
    baseUrl: import.meta.env.VITE_API_URL,
    prepareHeaders: (headers, { getState }) => {
      const token = (getState() as RootState).user.userInfo?.access_token;
      console.log("prepareHeaders token => ", token?.slice(0,50))
      if (token) {
        headers.set('Authorization', `bearer ${token}`);
      }
      return headers;
    },
  }),
  tagTypes: ["Documents"],
  endpoints: (build) => ({
    fetchAllDocuments: build.query<DocumentListResponse, void>({
      query: () => '/documents',
      providesTags: ["Documents"],
    }),

    getDocumentStatus: build.query<DocumentStatusResponse, string | undefined>({
      query: (document_id) => `/documents/${document_id}/status`
    }),

    fetchDocument : build.query<DocumentListItem,  string | undefined>({
      query: (document_id) => `/documents/${document_id}`,
    }),

    uploadDocument: build.mutation<DocumentUploadResponse, FormData>({
      query: (formData) => ({
        url: '/documents',
        method: 'POST',
        body: formData,
      }),
      invalidatesTags: ["Documents"],
    }),

    deleteDocument: build.mutation<DocumentDeleteResponse, string>({
      query: (document_id) => ({
        url: `/documents/${document_id}`,
        method: 'DELETE'
      }),
      invalidatesTags: ["Documents"],
    })
  })
});

export const {
  useFetchAllDocumentsQuery,
  useGetDocumentStatusQuery,
  useUploadDocumentMutation,
  useDeleteDocumentMutation,
  useFetchDocumentQuery
} = api;