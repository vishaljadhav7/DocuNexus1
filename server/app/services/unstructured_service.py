import asyncio
from typing import List, Dict, Any
import aiohttp
import aiofiles
from pathlib import Path
from app.config import Settings

class UnstructuredService:
    
    def __init__(self):
        self.settings = Settings()
        
    async def parse_pdf(self, pdf_url : str) -> List[Dict[str, Any]]:
        
        async with aiohttp.ClientSession() as session:
            async with session.get(pdf_url) as response:
                pdf_content = await response.read() 
                
        async with aiofiles.tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_file:
            await tmp_file.write(pdf_content)
            tmp_path = tmp_file.name
            
        try:
            chunks = await asyncio.to_thread(
                self._parse_pdf_sync,
                tmp_path
            )
        
            return chunks      
        
        finally:
            # Clean up temporary file
            Path(tmp_path).unlink(missing_ok=True)            
                
    def _parse_pdf_sync(self, pdf_path:str):
        from unstructured.partition.pdf import partition_pdf
        from unstructured.chunking.title import chunk_by_title
        
        elements = partition_pdf(
            filename=pdf_path,
            strategy="hi_res",  # High resolution for better extraction
            extract_images_in_pdf=True,
            extract_image_block_types=["Image"],
            chunking_strategy="by_title",
            max_characters=self.settings.chunk_size,    
            overlap=self.settings.chunk_overlap
        )
        chunks = chunk_by_title(elements=elements, max_characters=3000, new_after_n_chars=2400, combine_text_under_n_chars=500)
        return chunks
            

                             
            