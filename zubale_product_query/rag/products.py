import os
import glob
import chromadb

from typing import List
from pydantic import BaseModel
from zubale_product_query.serializers.models import ProductQuerySerializer


class ProductQueryContextDocument(BaseModel):
    document_content: str


class ProductQueryContext(BaseModel):
    context: List[ProductQueryContextDocument]


def get_top_k():
    if os.getenv("TOP_K"):
        return int(os.getenv("TOP_K"))

    return 5


def initialize_product_query_context():
    """
    Initialize the ChromaDB collection for product query context.

    This function prepares the vector database for product queries by:
    1. Getting or creating the ChromaDB collection named 'product_query_context'
    2. Deleting all existing documents in the collection
    3. Reading all markdown files from the product_docs directory
    4. Adding each file's content to the collection with appropriate IDs and metadata
    """
    # Initialize Chroma client using default embedding function
    client = chromadb.Client()
    collection = client.get_or_create_collection(
        name="product_query_context",
    )

    # Delete all existing documents
    try:
        collection.delete(where={})
    except Exception:
        # If the collection is empty, an exception might be raised
        pass

    # Get all markdown files from product_docs directory
    product_files = glob.glob("product_docs/*.md")

    # Read and index each file
    documents = []
    ids = []
    metadatas = []

    for i, file_path in enumerate(product_files):
        with open(file_path, "r") as f:
            content = f.read()
            documents.append(content)
            # Use the filename as part of the ID
            file_name = os.path.basename(file_path)
            ids.append(f"product_{i+1}")
            metadatas.append({"source": file_name})

    # Add documents to the collection if there are any
    if documents:
        collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadatas
        )


def retrieve_product_query_context(product_query_operation: ProductQuerySerializer) -> ProductQueryContext:
    """
    Retrieves relevant product documents based on a user query.

    This function queries the ChromaDB collection 'product_query_context' with the
    user's query text and returns the most relevant product documents.

    Args:
        product_query_operation: A ProductQuerySerializer object containing the user's query
            and other operation details.

    Returns:
        ProductQueryContext: An object containing a list of relevant product documents
            that match the user's query. The number of documents is determined by
            the get_top_k() function.
    """
    # Extract the user query
    query_text = product_query_operation.query

    # Initialize Chroma client using default embedding function
    client = chromadb.Client()
    collection = client.get_or_create_collection(
        name="product_query_context",
    )

    # Embed the query and retrieve top-k documents
    results = collection.query(
        query_texts=[query_text],
        n_results=get_top_k(),
        include=["documents"]
    )

    # Build and return ProductQueryContext from retrieved documents
    documents = results["documents"][0]
    return ProductQueryContext(
        context=[ProductQueryContextDocument(document_content=doc) for doc in documents]
    )
