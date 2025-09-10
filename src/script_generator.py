# src/script_generator.py
from dotenv import load_dotenv
import os
import json
import google.generativeai as genai
from datetime import datetime
import re

# Load .env file
load_dotenv()

class DialogueScriptGenerator:
    def __init__(self):
        # Configure Gemini (API key from environment)
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.use_ai = True
        else:
            print("Warning: No GEMINI_API_KEY found, using basic script generation")
            self.use_ai = False
        
        self.host1_name = "Alex"
        self.host2_name = "Sam"
    
    def generate_dialogue_script(self, articles, market_data=None):
        """Create natural two-host conversation using Gemini AI"""
        
        if self.use_ai and len(articles) > 0:
            try:
                return self._generate_ai_script(articles, market_data)
            except Exception as e:
                print(f"AI generation failed: {e}, falling back to template")
                return self._generate_template_script(articles, market_data)
        else:
            return self._generate_template_script(articles, market_data)
    
    def _generate_ai_script(self, articles, market_data):
        """Generate NotebookLM-style script using Gemini"""
        
        # Prepare articles summary
        articles_text = ""
        for i, article in enumerate(articles[:5], 1):
            articles_text += f"""
            Article {i}:
            Title: {article['title']}
            Summary: {article['summary'][:300]}
            Source: {article['source']}
            ---"""
        
        # Create the prompt
        prompt = f"""
        You are creating a podcast script for "Oil Field Insights Daily" - an engaging, NotebookLM-style podcast about the oil and gas industry.
        
        Create a natural dialogue between two hosts:
        - Alex: Analytical, asks insightful questions, connects dots between stories
        - Sam: Enthusiastic, provides context, explains technical concepts simply
        
        Today's date: {datetime.now().strftime('%B %d, %Y')}
        
        Market Data:
        - WTI Crude: ${market_data.get('wti_crude', 75.50) if market_data else 75.50} ({market_data.get('change_wti', '+0.5%') if market_data else '+0.5%'})
        - Brent Crude: ${market_data.get('brent_crude', 79.30) if market_data else 79.30} ({market_data.get('change_brent', '+0.8%') if market_data else '+0.8%'})
        
        News Articles:
        {articles_text}
        
        Create a 4-5 minute podcast script with:
        1. Engaging opening hook (reference the date and market mood)
        2. Natural back-and-forth discussion of the top 3 stories
        3. Use phrases like "That's fascinating!", "Right!", "Here's what's interesting..."
        4. Connect stories to bigger industry trends
        5. Each speaker should have 8-12 turns
        6. End with a forward-looking insight
        
        IMPORTANT: Return ONLY a JSON array with this exact format, no markdown or extra text:
        [
            {{"speaker": "host1", "text": "Opening line here...", "emotion": "neutral"}},
            {{"speaker": "host2", "text": "Response here...", "emotion": "excited"}},
            ...
        ]
        
        Emotions can be: neutral, excited, thoughtful, concerned, optimistic
        """
        
        # Generate with Gemini
        response = self.model.generate_content(
            prompt,
            generation_config={
                'temperature': 0.9,
                'top_p': 0.95,
                'max_output_tokens': 4000,
            }
        )
        
        # Parse response
        try:
            # Clean up response text
            response_text = response.text.strip()
            # Remove markdown code blocks if present
            response_text = re.sub(r'^```json\s*', '', response_text)
            response_text = re.sub(r'\s*```$', '', response_text)
            
            script_data = json.loads(response_text)
            
            # Ensure proper format
            formatted_script = []
            for item in script_data:
                formatted_script.append({
                    'speaker': item.get('speaker', 'host1'),
                    'text': item.get('text', ''),
                    'emotion': item.get('emotion', 'neutral')
                })
            
            # Add closing if not present
            if len(formatted_script) < 10:
                formatted_script.extend(self._add_closing())
            
            return formatted_script
            
        except json.JSONDecodeError as e:
            print(f"Failed to parse AI response: {e}")
            # Extract any dialogue we can find
            return self._extract_dialogue_fallback(response.text, articles)
    
    def _extract_dialogue_fallback(self, text, articles):
        """Fallback to extract dialogue from malformed response"""
        script = []
        
        # Try to extract dialogue patterns
        lines = text.split('\n')
        current_speaker = 'host1'
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('{') and not line.startswith('['):
                if 'Alex:' in line or 'host1:' in line:
                    current_speaker = 'host1'
                    text = line.split(':', 1)[-1].strip()
                elif 'Sam:' in line or 'host2:' in line:
                    current_speaker = 'host2'
                    text = line.split(':', 1)[-1].strip()
                else:
                    text = line
                
                if text and len(text) > 10:
                    script.append({
                        'speaker': current_speaker,
                        'text': text,
                        'emotion': 'neutral'
                    })
                    # Alternate speakers
                    current_speaker = 'host2' if current_speaker == 'host1' else 'host1'
        
        # If we got something, use it; otherwise fall back to template
        return script if len(script) > 5 else self._generate_template_script(articles, None)
    
    def _generate_template_script(self, articles, market_data):
        """Fallback template-based script generation (original method)"""
        script = []
        date_str = datetime.now().strftime('%B %d, %Y')
        
        # Opening
        script.append({
            'speaker': 'host1',
            'text': f"Good morning everyone, and welcome to Oil Field Insights! "
                   f"I'm {self.host1_name}, here with my co-host {self.host2_name}. "
                   f"Today is {date_str}, and we've got some fascinating developments "
                   f"in the oil and gas sector to discuss.",
            'emotion': 'neutral'
        })
        
        script.append({
            'speaker': 'host2',
            'text': f"That's right, {self.host1_name}! The industry never sleeps, "
                   f"and today we've got {len(articles)} major stories that caught our attention. "
                   f"From drilling innovations to market movements, let's dive right in!",
            'emotion': 'excited'
        })
        
        # Market update if available
        if market_data:
            script.append({
                'speaker': 'host1',
                'text': f"But first, let's check the markets. WTI Crude is trading at "
                       f"${market_data.get('wti_crude', 75.50)}, {market_data.get('change_wti', 'up slightly')} for the day.",
                'emotion': 'neutral'
            })
            
            script.append({
                'speaker': 'host2',
                'text': f"And Brent Crude is at ${market_data.get('brent_crude', 79.30)}, "
                       f"{market_data.get('change_brent', 'showing some movement')}. "
                       f"Interesting dynamics in the market today.",
                'emotion': 'thoughtful'
            })
        
        # Discuss articles
        for i, article in enumerate(articles[:3]):
            if i == 0:
                script.append({
                    'speaker': 'host1',
                    'text': f"Let's start with our top story: {article['title']}.",
                    'emotion': 'neutral'
                })
            else:
                script.append({
                    'speaker': 'host1',
                    'text': f"Now, here's another important development: {article['title']}.",
                    'emotion': 'neutral'
                })
            
            summary = article['summary'][:200] if len(article['summary']) > 200 else article['summary']
            script.append({
                'speaker': 'host2',
                'text': f"{summary}... This comes from {article['source']}.",
                'emotion': 'neutral'
            })
            
            # Add reaction
            if 'drilling' in article['title'].lower():
                reaction = "This could really reshape drilling operations going forward."
            elif 'price' in article['title'].lower():
                reaction = "The market implications here are significant."
            else:
                reaction = "This is definitely something the industry is watching closely."
            
            script.append({
                'speaker': 'host1',
                'text': f"That's really interesting! {reaction}",
                'emotion': 'thoughtful'
            })
        
        # Closing
        script.extend(self._add_closing())
        
        return script
    
    def _add_closing(self):
        """Add standard closing to script"""
        return [
            {
                'speaker': 'host1',
                'text': "And that wraps up today's Oil Field Insights. Thanks for joining us!",
                'emotion': 'neutral'
            },
            {
                'speaker': 'host2',
                'text': f"Remember to subscribe for daily updates on the oil and gas industry. "
                       f"I'm {self.host2_name}...",
                'emotion': 'neutral'
            },
            {
                'speaker': 'host1',
                'text': f"And I'm {self.host1_name}. Have a great day, and we'll see you tomorrow!",
                'emotion': 'optimistic'
            }
        ]