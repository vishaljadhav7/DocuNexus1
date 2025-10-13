import asyncio
from typing import List, Dict, Any
from app.core.exceptions import RAGException
from langchain_google_genai import  GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from app.config import Settings
import logging
import time
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiService:
    
    def __init__(self):
        self.settings = Settings()

        self.llm = ChatGoogleGenerativeAI(
           model=self.settings.gemini_model,
           google_api_key=self.settings.gemini_api_key,
           temperature=0.3
        )
            
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model = self.settings.gemini_embedding_model,
            google_api_key=self.settings.gemini_api_key,
            temperature=0.3,
            task_type="retrieval_document"
        )

        self.output_parser = StrOutputParser()

        
        # Simple rate limiting variables
        self.last_request_time = 0
        self.min_delay_between_requests = 0.5  # 500ms delay between requests
        self.batch_size = 3  # Process 3 chunks at a time
        self.batch_delay = 2  # 2 second delay between batches
    
    
    async def wait_for_rate_limit(self):
        """Simple rate limiting - wait if needed."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_delay_between_requests:
            wait_time = self.min_delay_between_requests - time_since_last
            logger.info(f"Rate limiting: waiting {wait_time:.2f}s")
            await asyncio.sleep(wait_time)
        
        self.last_request_time = time.time()  
           
    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text"""
        try:
            embedding = await self.embeddings.aembed_query(text)
            return embedding
        except Exception as e:
            return []
    
    
    def create_simple_prompt(self, content: Dict[str, Any]) -> str:   
        # Fixed prompt construction
        prompt_text = f"""You are creating a searchable description for document content retrieval.
        Content To Analyze:
        Text Content:
        {content['text']}
        """
            
        if content['has_tables']:
            prompt_text += "\nTables:\n"
            for idx, table in enumerate(content['tables']):
                prompt_text += f"Table {idx+1}:\n{table}\n\n"  # Fixed string concatenation
            
            # Fixed prompt continuation
        prompt_text += """
        Your Task:
        Generate a comprehensive suitable description that covers:
        
        1. Key facts, numbers, and data points from text and tables 
        2. Main topics and concepts discussed 
        3. Questions this content could answer
        4. Visual content analysis (charts, diagrams, patterns in images)
        5. Alternate search terms users might use
        
        Make it concise and searchable - prioritize findability over brevity.
        
        SEARCHABLE DESCRIPTION:"""
       
        return prompt_text
    
    def extract_content(self, chunk) -> Dict[str, Any]:
        content = {
            'text': chunk.text,
            'has_tables': False,
            'has_images': False,
            'tables': [],
            'images': []
        }
        
        # Check for tables and images
        if hasattr(chunk, 'metadata') and hasattr(chunk.metadata, 'orig_elements'):
            for element in chunk.metadata.orig_elements:
                element_type = type(element).__name__
                
                if element_type == 'Table':
                    content['has_tables'] = True
                    table_html = getattr(element.metadata, 'text_as_html', element.text)
                    content['tables'].append(table_html)
                
                elif element_type == 'Image':
                    if hasattr(element, 'metadata') and hasattr(element.metadata, 'image_base64'):
                        content['has_images'] = True
                        content['images'].append(element.metadata.image_base64)
        
        return content   
    
    async def generate_summary(self, content: Dict[str, Any], chunk_idx: int) -> str:
        
        await self.wait_for_rate_limit()
        
        if content['has_images']:
            message_content = [{'type': 'text', 'text': self.create_simple_prompt(content)}]
            for img_base64 in content['images'][:2]:
                message_content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}  # Fixed image format
                })
            
            message = [HumanMessage(content=message_content)]
        else:
            # Text only
            message = [HumanMessage(content=self.create_simple_prompt(content))]    
            
        # Retry logic with exponential backoff
        max_retries = 2
        for attempt in range(max_retries + 1):
            try:
                # Make the API call
                response = await self.llm.ainvoke(message)
                summary = self.output_parser.parse(response) 
                # logger.info(f"✓ Generated summary for chunk {chunk_idx + 1}")
                return summary.content
                
            except Exception as e:
                if attempt > max_retries:
                    break
                
                error_msg = str(e).lower()
                                
                # Handle specific errors
                if "rate limit" in error_msg or "quota" in error_msg:
                    wait_time = (2 ** attempt) * 2  # Exponential backoff: 2s, 4s, 8s
                    logger.warning(f"Rate limited - waiting {wait_time}s before retry {attempt + 1}")
                    await asyncio.sleep(wait_time)
                
                elif "timeout" in error_msg:
                    wait_time = 1 * (attempt + 1)  # Linear backoff for timeouts
                    logger.warning(f"Timeout - waiting {wait_time}s before retry {attempt + 1}")
                    await asyncio.sleep(wait_time)
                
                else:
                    logger.warning(f"Attempt {attempt + 1} failed for chunk {chunk_idx + 1}: {e}")
                    if attempt < max_retries:
                        await asyncio.sleep(1)  # Brief wait before retry
        
        # All retries failed - return fallback
        logger.error(f"✗ All retries failed for chunk {chunk_idx + 1}, using fallback")
        return f"Summary unavailable. Content preview: {content['text'][:900]}..."
    
    async def process_batch(self, batch_chunks: List[Any], start_idx: int) -> List[Dict[str, Any]]:
        """Process a batch of chunks sequentially."""
        results = []
        
        for i, chunk in enumerate(batch_chunks):
            chunk_idx = start_idx + i
            
            # Extract content
            content = self.extract_content(chunk)
            
            # Generate summary
            summary = await self.generate_summary(content, chunk_idx)
            
            embedding = await self.generate_embedding(summary)
            
            # Create result
            result = {
                'chunk_id': str(uuid.uuid4()),
                'summary': summary,
                'embed_data' : {
                 'embedding_id': str(uuid.uuid4()),
                 'embedding' : embedding,    
                }, 
                'metadata': {
                    'raw_text': content['text'],
                    'tables_html': content['tables'],
                    'image_base64': content['images'],
                    'has_tables': content['has_tables'],
                    'has_images': content['has_images']
                }
            }
            results.append(result)
        
        return results    
    
 
    async def summarize_chunks(self, chunks: List[Any]) -> List[Dict[str, Any]]:

        total_chunks = len(chunks)
        logger.info(f"Starting to process {total_chunks} chunks in batches of {self.batch_size}")
        
        all_results = []
        
        # Process in batches
        for i in range(0, total_chunks, self.batch_size):
            batch_chunks = chunks[i:i + self.batch_size]
            batch_num = (i // self.batch_size) + 1
            total_batches = (total_chunks + self.batch_size - 1) // self.batch_size
            
            logger.info(f"Processing batch {batch_num}/{total_batches}")
            
            try:
                # Process this batch
                batch_results = await self.process_batch(batch_chunks, i)
                all_results.extend(batch_results)
                
                # Wait between batches (except for the last one)
                if i + self.batch_size < total_chunks:
                    # logger.info(f"Batch complete. Waiting {self.batch_delay}s before next batch...")
                    await asyncio.sleep(self.batch_delay)
                
            except Exception as e:
                logger.error(f"Error processing batch {batch_num}: {e}")
                raise RAGException("Could not process the file") 
        
        logger.info(f"✓ Completed processing all {len(all_results)} chunks")
        return all_results
 
  