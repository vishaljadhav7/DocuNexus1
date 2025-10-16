"use client"

import type React from "react"
import { useCallback, useMemo, useState } from "react"
import { UploadCloud, FileUp,  Info, AlertCircle, CheckCircle2, Loader2, X } from "lucide-react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { useUploadDocumentMutation } from "@/features/documents/api"
import { useNavigate } from "react-router-dom"

type SelectedMeta = {
  name: string
  type: string
  sizeBytes: number
  sizeLabel: string
  lastModified?: string
}

const MAX_FILE_SIZE_MB = 2
const MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
const ACCEPTED_TYPES = ["application/pdf"]

export function FileUploadCard() {
  const [dragOver, setDragOver] = useState(false)
  const [file, setFile] = useState<File | null>(null)
  const [meta, setMeta] = useState<SelectedMeta | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [progress, setProgress] = useState(0)
  const [uploadDocument] = useUploadDocumentMutation();
  const router = useNavigate()

  const acceptAttr = useMemo(() => ACCEPTED_TYPES.join(","), [])

  const reset = useCallback(() => {
    setFile(null)
    setMeta(null)
    setError(null)
    setLoading(false)
    setProgress(0)
  }, [])

  const humanSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(2)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`
  }


  const validateAndSet = async (f: File) => {
    setError(null)

    // Basic type match against ACCEPTED_TYPES patterns
    const typeAllowed = ACCEPTED_TYPES.some((pattern) => {
      if (pattern.endsWith("/*")) {
        const prefix = pattern.replace("/*", "")
        return f.type.startsWith(prefix)
      }
      return f.type === pattern
    })

    if (!typeAllowed) {
      setError("Unsupported file type. Please upload images, videos, or PDF.")
      return
    }

    if (f.size > MAX_FILE_SIZE_BYTES) {
      setError(`File is too large. Max size is ${MAX_FILE_SIZE_MB}MB.`)
      return
    }


    const m: SelectedMeta = {
      name: f.name,
      type: f.type || "unknown",
      sizeBytes: f.size,
      sizeLabel: humanSize(f.size),
      lastModified: f.lastModified ? new Date(f.lastModified).toLocaleString() : undefined
    }

    setFile(f)
    setMeta(m)
  }

  const onInputChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0]
    if (f) {
      await validateAndSet(f)
    }
  }

  const onDrop = async (e: React.DragEvent<HTMLLabelElement>) => {
    e.preventDefault()
    e.stopPropagation()
    setDragOver(false)
    const f = e.dataTransfer.files?.[0]
    if (f) {
      await validateAndSet(f)
    }
  }

  const startUpload = async () => {
    if (!file) {
      setError("Please select a file before uploading.")
      return
    }

    setError(null)
    setLoading(true)
    setProgress(0)

    const formData = new FormData();
    formData.append('doc_file', file);

    const interval = setInterval(() => {
      setProgress((p) => {
        const next = Math.min(p + Math.random() * 20, 95)
        return next
      })
    }, 300)

    try {

      const file_res = await uploadDocument(formData).unwrap();
      setProgress(100)
      console.log("file_res =>>>>>> ", file_res)
      
      // router(`/document/${file_res.document_id}`)
      
    } catch (e: any) {
      setError(e?.message || "Upload failed. Please try again.")
    } finally {
      clearInterval(interval)
      setLoading(false)
    }
  }

  return (
    <Card className="w-full max-w-xl bg-card text-foreground border-border p-6">
      <div className="flex flex-col gap-6 md:flex-row">

        <div className="w-full flex flex-col gap-4">
          <div className="space-y-2 mx-auto">
            <h2 className="text-lg font-medium text-pretty text-center">Upload a file</h2>
            <p className="text-sm text-muted-foreground">
              Drag and drop or click to select a file.
            </p>
          </div>

          <label
            onDragOver={(e) => {
              e.preventDefault()
              setDragOver(true)
            }}
            onDragLeave={() => setDragOver(false)}
            onDrop={onDrop}
            className={[
              "flex cursor-pointer flex-col items-center justify-center gap-2 rounded-md border border-dashed p-6 text-center outline-none transition",
              dragOver ? "bg-muted/40 border-primary/50" : "bg-muted/20 hover:bg-muted/30",
            ].join(" ")}
          >
            <UploadCloud className="h-6 w-6 text-muted-foreground" aria-hidden="true" />
            <div className="space-y-1">
              <p className="text-sm">
                <span className="font-medium">Click to choose</span> or drag and drop
              </p>
              <p className="text-xs text-muted-foreground">Accepted: images, video, PDF • Max {MAX_FILE_SIZE_MB}MB</p>
            </div>
            <input type="file" className="sr-only" accept={acceptAttr} onChange={onInputChange} disabled={loading} />
          </label>

          {/* Details */}
          <div className="rounded-md border border-border p-4 bg-background">
            {file && meta ? (
              <div className="flex items-start gap-3">
                <FileUp className="h-5 w-5 text-muted-foreground mt-0.5" aria-hidden="true" />
                <div className="flex-1 space-y-1">
                  <div className="flex items-center justify-between gap-2">
                    <p className="text-sm font-medium text-pretty">{meta.name}</p>
                    <Button
                      variant="ghost"
                      size="icon"
                      className="h-7 w-7"
                      onClick={reset}
                      aria-label="Remove selected file"
                    >
                      <X className="h-4 w-4" />
                    </Button>
                  </div>
                  <p className="text-xs text-muted-foreground">
                    {meta.type} • {meta.sizeLabel}
                    {meta.lastModified ? ` • Modified ${meta.lastModified}` : ""}
                  </p>
                </div>
              </div>
            ) : (
              <div className="flex items-start gap-3">
                <Info className="h-5 w-5 text-muted-foreground mt-0.5" aria-hidden="true" />
                <p className="text-sm text-muted-foreground">
                  No file selected yet. Choose a file to see details before upload.
                </p>
              </div>
            )}
          </div>

          {/* Validation & helper notes */}
          <ul className="space-y-1 rounded-md border border-border p-3 bg-background text-xs text-muted-foreground">
            <li className="flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-emerald-500" aria-hidden="true" />
              Max size: {MAX_FILE_SIZE_MB}MB
            </li>
            <li className="flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-emerald-500" aria-hidden="true" />
              Types: PDF Only
            </li>

            {error && (
              <li className="flex items-center gap-2 text-destructive">
                <AlertCircle className="h-4 w-4" aria-hidden="true" />
                <span className="text-foreground">{error}</span>
              </li>
            )}
          </ul>

          {/* Actions */}
          <div className="flex items-center gap-2">
            <Button onClick={startUpload} disabled={!file || loading}>
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" aria-hidden="true" />
                  Uploading...
                </>
              ) : (
                "Start Upload"
              )}
            </Button>
            <Button variant="secondary" onClick={reset} disabled={loading}>
              Reset
            </Button>
          </div>

          {/* Loader / Progress */}
          {loading && (
            <div className="space-y-2" aria-live="polite" aria-busy="true">
              <Progress value={progress} />
              <p className="text-xs text-muted-foreground">Uploading... Please wait</p>
            </div>
          )}
        </div>
      </div>
    </Card>
  )
}
