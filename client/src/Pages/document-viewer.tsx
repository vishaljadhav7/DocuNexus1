import { useState, useEffect, useMemo } from "react";
import { Loader2, FileText, CheckCircle2, Clock, Download, MessageSquare, Copy, Check } from "lucide-react";
import { motion } from "framer-motion";
import { useFetchDocumentQuery } from "@/features/documents/api";
import { useAppSelector } from "@/app-store/hooks";
import { useParams } from "react-router-dom";
import axios from "axios";
import type { DocumentStatusResponse } from "@/features/documents/types";
import { Link } from "react-router-dom";

export function DocumentViewer() {
  const user = useAppSelector(store => store.user.userInfo)
  const { document_id }  = useParams();

  const [documentStatus, setDocumentStatus] = useState<DocumentStatusResponse>({
    processing_status : '',
    document_id : '',
    error_message: ''
  });
  const [isStatusLoading, setIsStatusLoading] = useState(false);
  const [copiedId, setCopiedId] = useState(false);

  const {
    data: document,
    isLoading: isDocLoading,
    refetch: refetchDoc,
  } = useFetchDocumentQuery(document_id, { skip: !document_id })

  const baseStatus = document?.processing_status

  const getDocumentStatus = async () => {
    setIsStatusLoading(true);
    try {
      const res = await axios.get(
      `${import.meta.env.VITE_API_URL}/documents/${document_id}/status`,  
       {
        headers : {
          'Authorization' : `Bearer ${user?.access_token}`
        }
       }
      )
      if(res.status >= 200){
        setDocumentStatus(res.data)
      }
    } catch (error) {
      console.error(error)
    }
    finally {
      setIsStatusLoading(false);
    }
  }

  const effectiveStatus = useMemo(
    () =>
      documentStatus?.processing_status 
        ? documentStatus.processing_status
        : baseStatus,
    [documentStatus?.processing_status, baseStatus]
  );

  useEffect(() => {
    if (effectiveStatus === "completed") {
      refetchDoc()
      return;
    }
  }, [effectiveStatus, refetchDoc]);

  const copyToClipboard = async () => {
    if (document?.id) {
      await navigator.clipboard.writeText(document.id);
      setCopiedId(true);
      setTimeout(() => setCopiedId(false), 2000);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case "completed":
        return "bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-950/50 dark:text-emerald-400 dark:border-emerald-800";
      case "processing":
        return "bg-blue-50 text-blue-700 border-blue-200 dark:bg-blue-950/50 dark:text-blue-400 dark:border-blue-800";
      case "failed":
        return "bg-red-50 text-red-700 border-red-200 dark:bg-red-950/50 dark:text-red-400 dark:border-red-800";
      default:
        return "bg-slate-50 text-slate-700 border-slate-200 dark:bg-slate-800 dark:text-slate-300 dark:border-slate-700";
    }
  };

  const getStatusIcon = (status : string | undefined) => {
    switch (status) {
      case "completed":
        return <CheckCircle2 className="w-4 h-4" />;
      case "processing":
        return <Loader2 className="w-4 h-4 animate-spin" />;
      default:
        return <Clock className="w-4 h-4" />;
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + " " + sizes[i];
  };

  const formatDate = (dateString : Date) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  if (isDocLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-50 dark:from-slate-950 dark:via-blue-950/20 dark:to-slate-950 p-6 flex items-center justify-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
          className="w-full max-w-xl"
        >
          <div className="bg-card rounded-2xl border border-border shadow-xl overflow-hidden">
            {/* Header Skeleton */}
            <div className="p-8 border-b border-border">
              <div className="flex items-start gap-4 mb-6">
                <div className="w-14 h-14 rounded-xl shimmer" />
                <div className="flex-1 space-y-3">
                  <div className="h-6 shimmer rounded-lg w-3/4" />
                  <div className="h-4 shimmer rounded w-24" />
                </div>
              </div>
              <div className="h-8 shimmer rounded-full w-32" />
            </div>

            {/* Content Skeleton */}
            <div className="p-8">
              <div className="grid grid-cols-2 gap-4 mb-6">
                <div className="p-4 bg-muted rounded-xl border border-border">
                  <div className="h-3 shimmer rounded w-8 mb-3" />
                  <div className="h-4 shimmer rounded w-full" />
                </div>
                <div className="p-4 bg-muted rounded-xl border border-border">
                  <div className="h-3 shimmer rounded w-16 mb-3" />
                  <div className="h-4 shimmer rounded w-full" />
                </div>
              </div>

              <div className="h-11 shimmer rounded-xl mb-6" />
              <div className="space-y-4">
                <div className="h-5 shimmer rounded w-48 mx-auto" />
                <div className="h-11 shimmer rounded-xl" />
              </div>

              <div className="mt-8 pt-6 border-t border-border">
                <div className="h-3 shimmer rounded w-40 mx-auto" />
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-50 dark:from-slate-950 dark:via-blue-950/20 dark:to-slate-950 p-6 flex items-center justify-center">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        className="w-full max-w-xl"
      >
        <div className="bg-card rounded-2xl border border-border shadow-xl overflow-hidden backdrop-blur-sm">
          {/* Header Section */}
          <div className="p-8 border-b border-border bg-gradient-to-br from-transparent to-primary/5">
            <div className="flex items-start gap-4 mb-6">
              <motion.div 
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ delay: 0.1 }}
                className="p-3.5 bg-gradient-to-br from-primary/10 to-primary/20 rounded-xl ring-1 ring-primary/20"
              >
                <FileText className="w-7 h-7 text-primary" />
              </motion.div>
              <div className="flex-1 min-w-0">
                <motion.h1 
                  initial={{ x: -20, opacity: 0 }}
                  animate={{ x: 0, opacity: 1 }}
                  transition={{ delay: 0.15 }}
                  className="text-xl font-semibold text-foreground break-words leading-tight"
                >
                  {document?.filename}
                </motion.h1>
                <motion.p 
                  initial={{ x: -20, opacity: 0 }}
                  animate={{ x: 0, opacity: 1 }}
                  transition={{ delay: 0.2 }}
                  className="text-sm text-muted-foreground mt-1.5 font-medium"
                >
                  {formatFileSize(document?.file_size)}
                </motion.p>
              </div>
            </div>

            {/* Status Badge */}
            <motion.div 
              initial={{ y: 10, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.25 }}
              className="flex items-center gap-2"
            >
              <div
                className={`inline-flex items-center gap-2.5 px-4 py-2 rounded-full border text-sm font-semibold shadow-sm ${getStatusColor(
                  effectiveStatus
                )}`}
              >
                {getStatusIcon(effectiveStatus)}
                <span className="capitalize tracking-wide">{effectiveStatus}</span>
              </div>
            </motion.div>
          </div>

          {/* Content Section */}
          <div className="p-8">
            {/* Info Grid */}
            <motion.div 
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.3 }}
              className="grid grid-cols-2 gap-4 mb-6"
            >
              <div className="group relative p-4 bg-muted/50 rounded-xl border border-border hover:border-primary/30 transition-all duration-200">
                <p className="text-xs text-muted-foreground font-bold uppercase tracking-wider mb-2.5">
                  Document ID
                </p>
                <div className="flex items-center gap-2">
                  <p className="text-sm font-mono text-foreground font-medium truncate flex-1" title={document?.id}>
                    {document?.id}
                  </p>
                  <button
                    onClick={copyToClipboard}
                    className="copy-button p-1.5 rounded-lg hover:bg-primary/10 text-muted-foreground hover:text-primary transition-colors"
                    title="Copy ID"
                  >
                    {copiedId ? (
                      <Check className="w-4 h-4 text-success" />
                    ) : (
                      <Copy className="w-4 h-4" />
                    )}
                  </button>
                </div>
              </div>
              <div className="p-4 bg-muted/50 rounded-xl border border-border hover:border-primary/30 transition-all duration-200">
                <p className="text-xs text-muted-foreground font-bold uppercase tracking-wider mb-2.5">
                  Uploaded
                </p>
                <p className="text-sm text-foreground font-medium">
                  {document?.created_at ? formatDate(document.created_at) : "—"}
                </p>
              </div>
            </motion.div>

            {/* View Document Button */}
            <motion.div
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.35 }}
            >
              <a href={document?.cloudinary_url} target="_blank" rel="noopener noreferrer">
                <button className="w-full mb-6 px-5 py-3 text-foreground font-semibold bg-secondary hover:bg-secondary/80 border border-border rounded-xl transition-all duration-200 flex items-center justify-center gap-2.5 shadow-sm hover:shadow group">
                  <Download className="w-4 h-4 group-hover:scale-110 transition-transform" />
                  View Original Document
                </button>
              </a>
            </motion.div>

            {/* Action Section */}
            {effectiveStatus !== "completed" ? (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
                className="space-y-4"
              >
                <div className="flex items-center justify-center gap-2 text-sm text-muted-foreground font-medium">
                  {/* <Loader2 className="w-4 h-4 animate-spin text-primary" /> */}
                  <p>Processing your document...</p>
                </div>
                <button
                  onClick={getDocumentStatus}
                  disabled={isStatusLoading}
                  className="w-full px-5 py-3 bg-primary hover:bg-primary/90 disabled:bg-muted disabled:text-muted-foreground disabled:cursor-not-allowed text-primary-foreground font-semibold rounded-xl transition-all duration-200 flex items-center justify-center gap-2.5 shadow-lg hover:shadow-xl disabled:shadow-none"
                >
                  {isStatusLoading ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      Checking Status...
                    </>
                  ) : (
                    <>
                      <Clock className="w-4 h-4" />
                      Check Status
                    </>
                  )}
                </button>
              </motion.div>
            ) : (
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.3, delay: 0.4 }}
                className="space-y-4"
              >
                <div className="flex items-center justify-center gap-2 text-sm text-success font-semibold mb-2">
                  <CheckCircle2 className="w-5 h-5" />
                  <p>Your document is ready!</p>
                </div>

                <Link to={`/document/${document_id}/chat`}>                
                <button className="w-full px-5 py-3 bg-primary hover:bg-primary/90 text-primary-foreground font-semibold rounded-xl transition-all duration-200 flex items-center justify-center gap-2.5 shadow-lg hover:shadow-xl group">
                  <MessageSquare className="w-4 h-4 group-hover:scale-110 transition-transform" />
                  Ask AI Questions
                </button>
                </Link>

              </motion.div>
            )}

            {/* Footer */}
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5 }}
              className="mt-8 pt-6 border-t border-border"
            >
              <p className="text-xs text-muted-foreground text-center font-medium">
                {document?.updated_at ? `Last updated: ${formatDate(document.updated_at)}` : ""}
              </p>
            </motion.div>
          </div>
        </div>
      </motion.div>
    </div>
  );
}

export default DocumentViewer;
