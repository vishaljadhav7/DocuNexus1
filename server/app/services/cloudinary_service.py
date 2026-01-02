import asyncio
import cloudinary
import cloudinary.uploader
from pathlib import Path
from app.config import Settings
from app.core.exceptions import CloudinaryError
import aiofiles.tempfile
import os
import logging

logger = logging.getLogger(__name__)


class CloudinaryService:
    def __init__(self):
        settings = Settings()
        cloudinary.config(
            cloud_name=settings.cloudinary_cloud_name,
            api_key=settings.cloudinary_api_key,
            api_secret=settings.cloudinary_api_secret
        )
    
    async def upload_pdf(
        self,
        file_content: bytes,
        filename: str,
        user_id: str
    ) -> dict:
        """Upload PDF to Cloudinary - raises CloudinaryError on failure"""
        folder = f"rag_documents/{user_id}"
        temp_path = None
        
        try:
            # Create temp file
            tmp_file = await aiofiles.tempfile.NamedTemporaryFile('wb+', delete=False)
            await tmp_file.write(file_content)
            await tmp_file.flush()
            temp_path = tmp_file.name
            await tmp_file.close()
            
            # Upload to Cloudinary
            result = await asyncio.to_thread(
                cloudinary.uploader.upload,
                temp_path,
                resource_type="raw",
                folder=folder,
                public_id=Path(filename).stem,
                overwrite=True,
                format="pdf",
            )
            
            return {
                "url": result["secure_url"],
                "public_id": result["public_id"],
                "size": result["bytes"],
                "created_at": result["created_at"],
            }
        
        except Exception as e:
            logger.error(f"Cloudinary upload failed: {str(e)}")
            raise CloudinaryError("upload", str(e))
        
        finally:
            # Cleanup temp file
            if temp_path:
                try:
                    os.unlink(temp_path)
                except Exception as e:
                    logger.warning(f"Failed to cleanup temp file: {e}")
    
    async def delete_file(self, public_id: str) -> bool:
        """Delete file from Cloudinary"""
        try:
            result = await asyncio.to_thread(
                cloudinary.uploader.destroy,
                public_id,
                resource_type="raw"
            )
            return result.get("result") == "ok"
        except Exception as e:
            logger.error(f"Cloudinary delete failed: {str(e)}")
            raise CloudinaryError("delete", str(e))