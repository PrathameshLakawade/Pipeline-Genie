from fastapi import Request
import ollama, json


# Generate business needs
def generate_business_needs(request: Request, rows: int, columns: list):
    try:
        logger = request.app.state.logger
        df = request.app.state.dataframe
        
        sampled_df = df.sample(fraction=0.01, seed=42).limit(5)
        
        summary = f"Dataset has {rows} rows and {len(columns)} columns. \n\n"
        summary += "Sampled Data:\n"
        
        for row in sampled_df.collect():
            summary += ", ".join([f"{col}: {row[col]}" for col in columns]) + "\n"
        
            prompt = f"""
            Based on the following dataset sample, analyze the data and provide business needs that can be derived from it.
            Also, mention the transformations required for efficiently extracting each business need.

            Use the following transformation functions:
            - `one_hot_encode`: Apply to categorical columns like "Type", "Gender", etc.
            - `sanitize_text`: Apply to text columns like "Description" to remove special characters.
            - `explode_column`: Apply to list or object columns.

            The response **must** be a valid JSON object with this exact structure:

            {{
            "business_needs": [
                {{
                "need": "Describe the business need",
                "transformations": {{
                    "one_hot_encode": ["column1", "column2"],
                    "sanitize_text": ["column3"],
                    "explode_column": ["column4"]
                }}
                }},
                {{
                "need": "Another business need",
                "transformations": {{
                    "one_hot_encode": ["column1"],
                    "sanitize_text": ["column2"]
                }}
                }}
            ]
            }}

            ### CRITICAL:
            - **Your response must be a single, valid JSON object.**
            - **Do not include explanations, comments, or extra text before or after the JSON.**
            - **Ensure transformation functions are mapped correctly to the columns.**

            Dataset sample:
            {summary}
            """

            response = ollama.chat(model="llama2", messages=[
                {"role": "user", "content": prompt}
            ], format="json")

            if response:
                try:
                    json_obj = json.loads(response["message"]["content"])
                    logger.info("Successfully generated business needs!")
                    
                    return json_obj
                except json.JSONDecodeError:
                    logger.error("LLaMA returned invalid JSON.")
                    return False

    except Exception as e:
        logger.error(f"Failed to generate business needs: {str(e)}")
        raise Exception(f"Failed to generate business needs: {str(e)}")