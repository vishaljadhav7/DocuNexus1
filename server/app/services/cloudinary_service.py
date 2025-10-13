import asyncio
import cloudinary
import cloudinary.uploader
from typing import Dict, Any
from pathlib import Path
from app.config import Settings
import aiofiles.tempfile
import os

class CloudinaryService:
        
    def __init__(self):
        settings = Settings()
        cloudinary.config(
          cloud_name=settings.cloudinary_cloud_name,
          api_key=settings.cloudinary_api_key,
          api_secret=settings.cloudinary_api_secret
        ) 
   
    async def upload_pdf(self, file_content: bytes, filename: str, user_id: str):
        folder = f"rag_documents/{user_id}"

        # Create temp file with delete=False to avoid Windows sharing violation
        tmp_file = await aiofiles.tempfile.NamedTemporaryFile('wb+', delete=False)
        try:
            await tmp_file.write(file_content)
            await tmp_file.flush()
            temp_path = tmp_file.name
    
            await tmp_file.close()  # Close file handle, unlock file
            
            # Run blocking upload in thread, pass file path
            result = await asyncio.to_thread(
                cloudinary.uploader.upload,
                temp_path,
                resource_type="raw",
                folder=folder,
                public_id=Path(filename).stem,
                overwrite=True,
                format="pdf",
            )
            
            print("5 ------------ done ------------- ")
        finally:
            # Cleanup temp file manually
            try:
                os.unlink(temp_path)
            except Exception:
                pass
    
        return {
            "url": result["secure_url"],
            "public_id": result["public_id"],
            "size": result["bytes"],
            "created_at": result["created_at"],
        }

        
    async def delete_file(self, public_id: str) -> bool:
        """Delete file from Cloudinary"""
        try:
            # Offload sync destroy to thread
            result = await asyncio.to_thread(
                cloudinary.uploader.destroy,
                public_id,
                resource_type="raw"
            )
            return result.get("result") == "ok"
        except Exception:
            return False    

    
 
