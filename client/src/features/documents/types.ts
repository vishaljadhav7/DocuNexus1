// export  const ProcessingStatus = {
//     UPLOADED: 'uploaded',
//     PROCESSING: 'processing',
//     COMPLETED: 'completed',
//     FAILED: 'failed'
// } as const;


export interface DocumentListItem{
    id : string;
    user_id : string;
    filename : string;
    file_size: number;
    cloudinary_url : string;
    cloudinary_public_id : string;
    error_message? : string;
    processing_status : string;
    created_at : Date;
    updated_at? : Date;
}

export interface DocumentListResponse{
    documents : DocumentListItem[];
    total : number;
}

export interface DocumentStatusResponse{
    document_id: string;
    processing_status : string;
    error_message? : string;
}

export interface DocumentUploadResponse{
    document_id: string;
    filename : string;
    cloudinary_url : string;
    processing_status: string
    created_at : Date;
    message : string;
}

export interface DocumentDeleteResponse{
    document_id: string;
    message : string;
}