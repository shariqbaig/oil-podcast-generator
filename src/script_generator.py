# src/script_generator.py
import random
from datetime import datetime

class DialogueScriptGenerator:
    def __init__(self):
        self.host1_name = "Alex"
        self.host2_name = "Sam"
        
    def generate_dialogue_script(self, articles, market_data=None):
        """Create natural two-host conversation"""
        
        script = []
        date_str = datetime.now().strftime('%B %d, %Y')
        
        # Opening
        script.append({
            'speaker': 'host1',
            'text': f"Good morning everyone, and welcome to Oil Field Insights! "
                   f"I'm {self.host1_name}, here with my co-host {self.host2_name}. "
                   f"Today is {date_str}, and we've got some fascinating developments "
                   f"in the oil and gas sector to discuss."
        })
        
        script.append({
            'speaker': 'host2',
            'text': f"That's right, {self.host1_name}! The industry never sleeps, "
                   f"and today we've got {len(articles)} major stories that caught our attention. "
                   f"From drilling innovations to market movements, let's dive right in!"
        })
        
        # Market update if available
        if market_data:
            script.append({
                'speaker': 'host1',
                'text': f"But first, let's check the markets. WTI Crude is trading at "
                       f"${market_data['wti_crude']}, {market_data['change_wti']} for the day."
            })
            
            script.append({
                'speaker': 'host2',
                'text': f"And Brent Crude is at ${market_data['brent_crude']}, "
                       f"{market_data['change_brent']}. "
                       f"{'Looks like a positive start' if '+' in market_data['change_brent'] else 'Some downward pressure'} "
                       f"in the markets today."
            })
        
        # Discuss each article with natural back-and-forth
        for i, article in enumerate(articles[:5]):
            self._add_article_discussion(script, article, i)
        
        # Closing
        script.append({
            'speaker': 'host1',
            'text': "And that wraps up today's Oil Field Insights. Thanks for joining us!"
        })
        
        script.append({
            'speaker': 'host2',
            'text': f"Remember to subscribe for daily updates on the oil and gas industry. "
                   f"I'm {self.host2_name}..."
        })
        
        script.append({
            'speaker': 'host1',
            'text': f"And I'm {self.host1_name}. Have a great day, and we'll see you tomorrow!"
        })
        
        return script
    
    def _add_article_discussion(self, script, article, index):
        """Create natural discussion about an article"""
        
        transitions = [
            "Now, moving on to our next story...",
            "Here's something interesting...",
            "This next development is particularly noteworthy...",
            "Speaking of industry news...",
            "Let's shift gears to discuss..."
        ]
        
        reactions = [
            "That's really significant!",
            "Interesting development there.",
            "This could have major implications.",
            "That's a game-changer.",
            "The industry will be watching this closely."
        ]
        
        # Host 1 introduces
        if index > 0:
            transition = random.choice(transitions)
            script.append({
                'speaker': 'host1',
                'text': f"{transition} {article['title']}."
            })
        else:
            script.append({
                'speaker': 'host1',
                'text': f"Let's start with our top story: {article['title']}."
            })
        
        # Host 2 provides details
        summary = article['summary'][:200] if len(article['summary']) > 200 else article['summary']
        script.append({
            'speaker': 'host2',
            'text': f"{summary}... This comes from {article['source']}."
        })
        
        # Host 1 reacts or adds context
        reaction = random.choice(reactions)
        
        # Add contextual commentary based on keywords
        if 'drilling' in article['title'].lower():
            context = "This could really impact drilling operations across the region."
        elif 'price' in article['title'].lower() or 'market' in article['title'].lower():
            context = "Market analysts will be paying close attention to this."
        elif 'technology' in article['title'].lower():
            context = "Innovation like this is what drives the industry forward."
        elif 'production' in article['title'].lower():
            context = "Production levels are always a key indicator for the sector."
        else:
            context = "This is definitely something our listeners should keep an eye on."
        
        script.append({
            'speaker': 'host1',
            'text': f"{reaction} {context}"
        })