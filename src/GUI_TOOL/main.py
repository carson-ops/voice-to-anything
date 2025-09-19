from helper import *
from transformers import pipeline


summarization = pipeline("summarization", model="facebook/bart-large-cnn")

def chunk_text(text, max_length=3000): # chunk it
    words = text.split()       # split into individual words ['word1', 'word2', ...]
    chunks = []                # list to store finished chunks
    current_chunk = ""         # string we're currently building

    for word in words: # itterating through each word
        if len(current_chunk) + len(word) + 1 <= max_length: # number length of current chunk + number length of current word + 1 for account space until above max length
            # Add the word to the current chunk (plus a space)
            current_chunk += " " + word
        else:
            # Current chunk is full -> store it
            chunks.append(current_chunk.strip()) # store chunk in list and strip leading spaces.
            # Start a new chunk with this word
            current_chunk = word

    # Add the last chunk if there is one
    if current_chunk: # check remaing text and add it to list of chunks
        chunks.append(current_chunk.strip())

    return chunks

def summarize_long_text(text): # put it in chunk -> summarize each chunk -> stich chunk together -> summarize again after stiched
    chunks = chunk_text(text, max_length=3000) # puts text into chunks max 3k characters
    summaries = [] # holds the chunks in a list

    for i, chunk in enumerate(chunks): # loop to summarize each chunk | enum lets us loop over a list and keep track of the index of each item | basically looping over each chunk and keeping track of which chunk we're on
        print(f"Summarizing chunk {i+1}/{len(chunks)}...")
        summary = summarization(
            chunk, max_length=130, min_length=30, do_sample=False
        )[0]['summary_text'] # summarizing process
        summaries.append(summary) # add summary to list

    # Combine partial summaries into one final pass if there are multiple chunks
    combined_summary = " ".join(summaries)
    if len(chunks) > 1: # if we have more thank 1 chunk, summarize the stiched chunks of summaries
        combined_summary = summarization(
            combined_summary, max_length=150, min_length=50, do_sample=False
        )[0]['summary_text']

    return combined_summary