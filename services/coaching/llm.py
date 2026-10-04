from services.config.workout_config import PROMPT


class LLMCoach:

    def __init__(self, groq_client):
        """
        Initialize LLM Coach with Groq client.
        
        The groq_client is passed from main.py where it's already
        instantiated with the GROQ_API_KEY from environment.
        """
        
        self.client = groq_client
        self.history = []
        self.system_prompt = PROMPT
        
        # Model: Use confirmed available Groq model (August 2026)
        # Available models:
        # - "llama-3.1-8b-instant" (fastest, cheapest) ⭐ RECOMMENDED
        # - "gpt-oss-20b"
        # - "gpt-oss-120b"
        # - "llama-3.3-70b-versatile" (best quality, slower)
        # - "qwen-3.6-27b"
        self.model = "openai/gpt-oss-20b"

    def give_feedback(self, event, issue=None):
        """
        Generate AI coaching feedback based on event and form issue.
        
        Args:
            event: "workout_started", "set_completed", "form_issue", etc.
            issue: Optional form problem description
            
        Returns:
            str - Short AI coaching feedback (max 40 tokens) or None if error
        """
        
        try:
            # Build prompt
            prompt = f"Event: {event}"
            if issue:
                prompt += f"\nForm Issue: {issue}"
            
            # Build messages with system prompt and history
            messages = [
                {
                    "role": "system",
                    "content": self.system_prompt
                },
                *self.history[-10:],  # Keep last 10 exchanges
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            # Call Groq API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.4,
                max_tokens=40
            )
            
            # Extract response text
            text = response.choices[0].message.content.strip()
            
            # Store in history for context
            self.history.append({
                "role": "user",
                "content": prompt
            })
            
            self.history.append({
                "role": "assistant",
                "content": text
            })
            
            return text
        
        except Exception as e:
            print(f"LLM Error: {e}")
            return None