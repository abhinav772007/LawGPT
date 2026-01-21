CHUNK_LEN = 200
OVERLAP_WORDS = 50

def getChunks(text: str, chunk_len: int = CHUNK_LEN, overlap: int = OVERLAP_WORDS):
    """
    Split text into chunks with overlapping words.
    
    Args:
        text: The input text to split
        chunk_len: Number of words per chunk (default: CHUNK_LEN)
        overlap: Number of overlapping words between chunks (default: OVERLAP_WORDS)
    
    Returns:
        List of text chunks with overlap
    """
    chunks = []
    words = text.split()
    
    # If text is shorter than chunk_len, return it as a single chunk
    if len(words) <= chunk_len:
        return [text]
    
    # Calculate the step size (how many words to advance for each chunk)
    step = chunk_len - overlap
    
    # Ensure step is at least 1 to avoid infinite loop
    if step < 1:
        raise ValueError(f"overlap ({overlap}) must be less than chunk_len ({chunk_len})")
    
    # Create chunks with overlap
    start = 0
    while start < len(words):
        end = start + chunk_len
        chunk_words = words[start:end]
        chunks.append(' '.join(chunk_words))
        
        # Move to next chunk position
        start += step
        
        # Break if we've processed all words
        if end >= len(words):
            break
    
    return chunks