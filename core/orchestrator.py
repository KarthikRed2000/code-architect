import subprocess
import time
from google import genai
from google.genai import types
from utils.linter import validate_code
from utils.replacer import surgical_replace

class RefactorOrchestrator:
    def __init__(self, chroma_collection, gemini_key):
        self.collection = chroma_collection
        self.client = genai.Client(api_key=gemini_key)

    def get_full_context(self, query):
        """Finds target code and its dependencies in the Vector DB."""
        # Query the collection
        results = self.collection.query(query_texts=[query], n_results=1)
        
        # Check if we actually found anything
        # ChromaDB results are lists of lists: results['documents'][0][0]
        if not results['documents'] or not results['documents'][0]:
            print(f"⚠️ No results found for query: {query}")
            return None, None, None
            
        snippet = results['documents'][0][0]
        meta = results['metadatas'][0][0]
        
        # Ensure we are using the correct keys from your upsert.py
        # You used 'path' in upsert.py, so we use 'path' here
        file_path = meta.get('path') or meta.get('file') 
        obj_name = meta.get('name')
        
        context = f"FILE: {file_path}\nNAME: {obj_name}\nCODE:\n{snippet}"
        
        # This returns exactly 3 values: (string, string, string)
        return context, file_path, obj_name
    
    def run_refactor_loop(self, query, pattern="Strategy Pattern", max_attempts=3):
        """The Agentic Loop: Retrieve -> Prompt -> Validate -> Retry/Apply."""
        context_block, file_path, obj_name = self.get_full_context(query)
        
        if not context_block:
            print(f"❌ Could not find any code matching: {query}")
            return

        current_prompt = (
            f"Refactor the following code using the {pattern}. "
            "Ensure you maintain the same function signatures so external calls don't break. "
            "Output ONLY valid Python code.\n\n"
            f"{context_block}"
        )

        for attempt in range(max_attempts):
            try:
                print(f"--- 🤖 Gemini Attempt {attempt + 1} ---")
                
                response = self.client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=current_prompt,
                    config={'temperature': 0.1}
                )
                
                # Clean the output (remove markdown backticks)
                new_code = response.text.replace("```python", "").replace("```", "").strip()

                # 🛡️ Step: Linter Validation
                is_valid, error_msg = validate_code(new_code)

                if is_valid:
                    print(f"✅ Code validated. Applying surgery to {file_path}...")
                    surgical_replace(file_path, obj_name, new_code)
                    print("✨ Refactor complete!")
                    return
                else:
                    print(f"⚠️ Linter Error: {error_msg}")
                    # SELF-HEALING: Feed the error back to the AI for the next loop
                    current_prompt = (
                        f"The previous refactoring had a syntax error:\n{error_msg}\n\n"
                        f"Please fix the error and provide the full corrected code:\n{new_code}"
                    )
            except Exception as e:
                print(f"❌ Exception during refactoring: {e}")
                if "429" in str(e):
                    print("⚠️ Rate limit hit. Sleeping for 60 seconds before retrying...")
                    time.sleep(60) # Wait for the quota window to reset
                    continue
                else:
                    raise e

        print(f"❌ Failed to refactor after {max_attempts} attempts.")

    def apply_refactor(self, query: str, pattern: str):
        """The main Agentic loop: Retrieve -> Refactor -> Validate -> Apply."""
        context = self.get_full_context(query)
        
        # Get target info for replacement later
        primary = self.collection.query(query_texts=[query], n_results=1)
        file_path = primary['metadatas'][0][0]['path']
        obj_name = primary['metadatas'][0][0]['name']

        print(f"🚀 Starting refactor for {obj_name}...")
        
        prompt = f"Refactor the target code using {pattern}. Context:\n{context}"
        
        # Gemini Call
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction="You are a Senior Architect. Output ONLY the code."
            )
        )
        
        clean_code = response.text.strip().strip("```python").strip("```")

        # Validation
        is_valid, error = validate_code(clean_code)
        if is_valid:
            surgical_replace(file_path, obj_name, clean_code)
            print(f"✅ Refactor applied to {file_path}")
        else:
            print(f"❌ Validation failed: {error}")