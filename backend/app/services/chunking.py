from typing import List, Dict, Any

class TextChunkingService:
    def __init__(self, chunk_size: int = 400, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(self, text: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Splits a given text into smaller, overlapping chunks.
        This is a simplified example; a real implementation would use a robust text splitter.
        """
        if not text:
            return []

        # Simple whitespace tokenizer for demonstration
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk_words = words[i : i + self.chunk_size]
            chunk_text = " ".join(chunk_words)
            
            chunk_metadata = metadata.copy()
            chunk_metadata["text"] = chunk_text # Store chunk text in metadata
            chunk_metadata["id"] = f"{metadata.get('url', 'no_url')}_{i}" # Generate a unique ID

            chunks.append(chunk_metadata)
            
        return chunks
