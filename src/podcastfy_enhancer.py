# src/podcastfy_enhancer.py
"""
Enhancer to make Podcastfy output more NotebookLM-like
"""

def create_notebooklm_config(articles, market_data):
    """Create enhanced config for NotebookLM-style output"""
    
    # Build rich context
    context = f"""
    You are creating a NotebookLM-style podcast about oil industry news.
    Today: {datetime.now().strftime('%B %d, %Y')}
    
    Market: WTI ${market_data['wti_crude']} ({market_data['change_wti']})
            Brent ${market_data['brent_crude']} ({market_data['change_brent']})
    """
    
    return {
        "word_count": 3500,  # Longer for richer content
        "conversation_style": ["engaging", "analytical", "humorous", "insightful"],
        "podcast_name": "Oil Field Insights Daily",
        
        # Enhanced host personalities
        "roles_person1": """Alex: Senior petroleum engineer, 20 years experience. 
                           Makes dry observations, uses industry jargon naturally, 
                           occasionally laughs at the absurdity of oil markets""",
        
        "roles_person2": """Sam: Energy journalist, asks clarifying questions,
                           explains complex topics with analogies, gets excited 
                           about big numbers, sometimes interrupts with 'Wait, what?'""",
        
        # NotebookLM-specific instructions
        "custom_instructions": f"""
        {context}
        
        CRITICAL: Make this sound EXACTLY like NotebookLM:
        
        1. NATURAL REACTIONS:
        - "Oh wow, {market_data['wti_crude']}? That's actually..."
        - "[laughs] Okay, so let me get this straight..."
        - "Wait wait wait, hold on—"
        - "That's... that's actually fascinating"
        
        2. INTERRUPTIONS & OVERLAPS:
        - Sam cuts off Alex mid-sentence with questions
        - Alex trails off when making connections "So if we look at... oh, OH!"
        - Both occasionally talk at once briefly
        
        3. INDUSTRY-SPECIFIC BANTER:
        - Joke about "another day, another OPEC announcement"
        - Reference famous oil discoveries casually
        - Use drilling terminology naturally
        - Make comparisons to "that time in 2014 when oil crashed"
        
        4. TECHNICAL BUT ACCESSIBLE:
        - Explain horizontal drilling like "imagine drinking a milkshake..."
        - Compare fracking to "basically creating tiny earthquakes"
        - Use barrel counts but translate to "that's like X cars for a year"
        
        5. GENUINE CHEMISTRY:
        - Callback to earlier points
        - Friendly disagreement on predictions
        - Shared excitement over big discoveries
        - Natural tangents that loop back
        """,
        
        # Edge TTS optimization
        "text_to_speech": {
            "model": "edge",
            "edge": {
                "default_voices": {
                    "question": "en-US-AriaNeural",
                    "answer": "en-US-GuyNeural"
                },
                # SSML enhancements
                "ssml_features": {
                    "use_emphasis": True,
                    "use_breaks": True,
                    "use_prosody": True
                }
            }
        },
        
        # Podcast structure
        "dialogue_structure": "two_person_dialogue",
        "max_num_chunks": 12,  # More chunks for natural flow
        "min_chunk_size": 400,
        "output_language": "English",
        
        # Topics to cover
        "engagement_techniques": [
            f"React to WTI at ${market_data['wti_crude']}",
            "Discuss drilling in Permian Basin",
            "Analyze OPEC's latest moves",
            "Explain new extraction technology",
            "Predict next quarter prices",
            "Connect to geopolitical events"
        ]
    }