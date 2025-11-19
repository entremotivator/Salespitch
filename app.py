import streamlit as st
from typing import Dict, List, Optional
import json
from datetime import datetime

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    st.warning("OpenAI library not available. Install with: pip install openai")

# Page configuration
st.set_page_config(
    page_title="ATM Agency - AI Sales Assistant",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        color: #64748b;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .pitch-box {
        background-color: #f8fafc;
        border-left: 4px solid #667eea;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .ai-pitch-box {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        border-left: 4px solid #667eea;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border: 1px solid #667eea40;
    }
    .objection-box {
        background-color: #fef2f2;
        border-left: 4px solid #ef4444;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .response-box {
        background-color: #f0fdf4;
        border-left: 4px solid #22c55e;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .service-card {
        background: white;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e2e8f0;
        margin: 0.5rem 0;
    }
    .api-status {
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        font-weight: 600;
    }
    .api-active {
        background-color: #d1fae5;
        color: #065f46;
    }
    .api-inactive {
        background-color: #fee2e2;
        color: #991b1b;
    }
    .script-template {
        background-color: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

if 'openai_api_key' not in st.session_state:
    st.session_state.openai_api_key = ""
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'generated_scripts' not in st.session_state:
    st.session_state.generated_scripts = []
if 'current_analysis' not in st.session_state:
    st.session_state.current_analysis = None
if 'ai_model' not in st.session_state:
    st.session_state.ai_model = "gpt-4o-mini"
if 'temperature' not in st.session_state:
    st.session_state.temperature = 0.7


SERVICES = {
    "Custom AI Apps": {
        "description": "Bespoke AI-powered applications tailored to your business needs",
        "benefits": [
            "Automate complex workflows and reduce manual tasks by 70%",
            "Scale operations without increasing headcount",
            "Gain competitive advantage with proprietary AI solutions",
            "Integrate seamlessly with existing systems"
        ],
        "use_cases": [
            "Document processing and data extraction",
            "Predictive analytics and forecasting",
            "Intelligent customer support systems",
            "Custom workflow automation"
        ],
        "roi_points": "Typical ROI of 300-500% within first year through automation savings"
    },
    "PMS/CRM Systems": {
        "description": "AI-enhanced Project Management and Customer Relationship Management platforms",
        "benefits": [
            "Centralize all client data and project information",
            "AI-powered lead scoring and opportunity prediction",
            "Automated follow-ups and task management",
            "Real-time analytics and performance tracking"
        ],
        "use_cases": [
            "Sales pipeline management with AI insights",
            "Project tracking and resource allocation",
            "Customer lifecycle management",
            "Automated reporting and forecasting"
        ],
        "roi_points": "Increase sales conversion rates by 35% and reduce admin time by 60%"
    },
    "AI Marketplace": {
        "description": "Custom marketplace platforms powered by AI for intelligent matching and recommendations",
        "benefits": [
            "AI-driven product/service recommendations",
            "Intelligent search and discovery",
            "Automated vendor/buyer matching",
            "Dynamic pricing optimization"
        ],
        "use_cases": [
            "B2B service marketplaces",
            "Product recommendation engines",
            "Talent and freelancer platforms",
            "Equipment and resource sharing platforms"
        ],
        "roi_points": "Increase transaction volume by 45% through better matching and recommendations"
    },
    "AI Voice Agents": {
        "description": "24/7 intelligent voice assistants for customer service and sales",
        "benefits": [
            "Handle unlimited calls simultaneously",
            "Natural conversations in multiple languages",
            "Qualify leads and book appointments automatically",
            "Reduce call center costs by up to 80%"
        ],
        "use_cases": [
            "Inbound customer support and FAQ handling",
            "Outbound sales calls and lead qualification",
            "Appointment scheduling and reminders",
            "Order taking and status updates"
        ],
        "roi_points": "Save $50,000+ annually per customer service representative replaced"
    },
    "Website & Funnels": {
        "description": "High-converting websites and sales funnels with AI optimization",
        "benefits": [
            "AI-powered personalization for each visitor",
            "Real-time A/B testing and optimization",
            "Intelligent chatbots for lead capture",
            "Conversion rate optimization through ML"
        ],
        "use_cases": [
            "Lead generation landing pages",
            "E-commerce product funnels",
            "SaaS onboarding flows",
            "Event registration and webinar funnels"
        ],
        "roi_points": "Average 2-3x increase in conversion rates within 90 days"
    },
    "AI Automations": {
        "description": "End-to-end business process automation using AI",
        "benefits": [
            "Eliminate repetitive manual tasks",
            "Connect all your tools and platforms",
            "Intelligent decision-making in workflows",
            "Scale operations without hiring"
        ],
        "use_cases": [
            "Data entry and document processing",
            "Email and communication automation",
            "Social media management and posting",
            "Report generation and distribution"
        ],
        "roi_points": "Save 20-30 hours per employee per week on manual tasks"
    }
}


OBJECTIONS = {
    "Price/Budget": {
        "objections": [
            "It's too expensive",
            "We don't have the budget right now",
            "Your competitors are cheaper",
            "Can you give us a discount?"
        ],
        "responses": [
            "I understand budget is a concern. Let's look at this as an investment rather than a cost. Our clients typically see ROI within 3-6 months through efficiency gains. What if we could show you a clear path to saving more than the investment cost within the first year?",
            "I appreciate you being upfront about budget. Many of our best clients felt the same way initially. The question is: what's the cost of NOT solving this problem? If we can demonstrate that our solution pays for itself, would it make sense to explore flexible payment options?",
            "Price is definitely important, but let's talk about value. While we might not be the cheapest, we deliver complete solutions with ongoing support and optimization. Our clients stay with us because we drive measurable results. Would you like to see case studies from companies similar to yours?",
            "I'm happy to work within your budget. Let's start with the highest-impact solution first - typically our AI Voice Agents or Automations deliver immediate ROI. We can phase the implementation to match your cash flow. What's your biggest pain point right now?"
        ]
    },
    "Timing": {
        "objections": [
            "We're not ready yet",
            "Maybe next quarter",
            "We need to discuss this internally first",
            "Call me back in a few months"
        ],
        "responses": [
            "I completely understand wanting to get the timing right. Can I ask - what needs to happen before you'd be ready? Often while companies wait for the 'perfect time,' they're losing money daily on inefficiencies. What if we could start small and scale as you're ready?",
            "Timing is important, and I respect that. However, let me share something: our clients who started sooner rather than later consistently tell us they wish they'd begun earlier. Every month you wait, that's another month of manual processes and missed opportunities. What would make NOW the right time?",
            "Internal discussion is definitely important. To help that conversation, what if I provided you with an ROI analysis and implementation timeline specific to your needs? That way, you'll have concrete data to present. Who else needs to be involved in this decision?",
            "I appreciate you being direct. Rather than calling you back in a few months, what if we scheduled a brief check-in call in 4 weeks? In the meantime, I can send you relevant case studies and resources. Fair enough?"
        ]
    },
    "Trust/Skepticism": {
        "objections": [
            "We've been burned by agencies before",
            "How do we know this will work?",
            "Can you guarantee results?",
            "This sounds too good to be true"
        ],
        "responses": [
            "I'm sorry to hear you've had bad experiences - unfortunately, that's common in our industry. Here's how we're different: we start with a pilot project with clear, measurable KPIs. You only expand if we hit those targets. We also provide full transparency with weekly updates. Would you like to see our client retention rate and testimonials?",
            "That's a fair question, and I won't make promises I can't keep. What I can show you is our process: we start with a thorough audit, define specific metrics for success, and build in phases with checkpoints. You have full visibility and control. Our track record speaks for itself - 95% client retention. Can I share some case studies?",
            "I can't guarantee specific results because every business is unique, but I can guarantee our commitment and process. We include performance benchmarks in our contracts, and if we're not hitting milestones, we adjust at no extra cost. We've helped companies like [similar company] achieve [specific result]. What specific outcomes would make this a success for you?",
            "I understand your skepticism - AI and automation have been overhyped. Here's the reality: we focus on practical, proven solutions that deliver measurable value. No magic, just smart technology applied to real problems. How about we start with a free audit to identify opportunities? No commitment, just data."
        ]
    },
    "DIY/In-House": {
        "objections": [
            "We can build this in-house",
            "We already have a tech team",
            "We're working with another vendor",
            "We want to do it ourselves first"
        ],
        "responses": [
            "Having an in-house team is great! Many of our clients have excellent technical teams, and we work alongside them. The question is: do they have the specialized AI/ML expertise and time to build this while maintaining your current systems? We can actually help your team move faster. Would you be open to a collaborative approach?",
            "That's excellent that you have a tech team. We typically work in three ways: we can augment your team's capabilities, handle the specialized AI components while they focus on core business logic, or provide training and tools. Which model would complement your team best?",
            "I respect existing relationships. Can I ask - are you getting everything you need from your current vendor? We often work alongside other providers, handling the AI-specific components. If there are gaps in your current solution, we might be able to fill them without disrupting what's working. What's working well, and what could be better?",
            "DIY is definitely an option, and I respect that approach. The reality is: AI development has a steep learning curve and opportunity cost. While you're learning and building, you're missing out on revenue. We can have you up and running in weeks vs. months. What if we provided the solution now, and trained your team to manage it, so you get both immediate results AND long-term capability?"
        ]
    },
    "Understanding/Clarity": {
        "objections": [
            "I don't understand how AI works",
            "This seems too complicated",
            "We're not a tech company",
            "Will our team be able to use this?"
        ],
        "responses": [
            "You don't need to understand the technical details - that's our job! Think of it like driving a car: you don't need to know how the engine works to get value from it. We handle all the complexity and deliver simple, intuitive tools your team can use day one. Let me show you how simple it is with a quick demo?",
            "I understand it can seem complicated, but that's why we exist - to make it simple for you. Our solutions have user-friendly interfaces, and we provide complete training. Our average user is up and running in under an hour. The complexity is under the hood, not in your experience. Want to see how easy it is?",
            "You don't need to be a tech company to benefit from tech! In fact, non-tech companies often see the biggest gains because they have more manual processes to automate. We've worked with [industry examples], and they love how it simplifies their operations. What industry are you in? I can share relevant examples.",
            "Ease of use is our top priority. We design everything to be intuitive, and include comprehensive training and ongoing support. Plus, we build in automated processes that work behind the scenes - your team barely has to think about it. What specific concerns do you have about adoption?"
        ]
    },
    "Need/Priority": {
        "objections": [
            "We're doing fine without it",
            "This isn't a priority right now",
            "We don't have this problem",
            "We're focused on other initiatives"
        ],
        "responses": [
            "I'm glad things are going well! The best time to innovate is actually when things are good - that's when you can invest in getting ahead, not just catching up. Our most successful clients came to us when they were doing fine but wanted to dominate their market. Are you interested in going from good to exceptional?",
            "I understand you have competing priorities. Can I ask - what are your top 3 priorities right now? Often, our solutions directly support strategic initiatives like growth, efficiency, or customer satisfaction. We might be able to accelerate your other priorities rather than compete with them.",
            "That's great if you truly don't have operational inefficiencies or growth limitations. Most companies don't realize the opportunities until they see them. Would you be open to a free operational audit? We often identify 5-10 quick wins that businesses didn't know existed. No obligation, just insights.",
            "Focus is important. What if our solution actually freed up time and resources to focus more on those initiatives? By automating routine tasks and improving efficiency, your team would have more bandwidth for strategic work. What initiatives are you focused on? Let's see if we can help."
        ]
    }
}


INDUSTRIES = {
    "Real Estate": "long sales cycles, lead qualification, property management overhead",
    "Healthcare": "administrative burden, appointment scheduling, patient communication",
    "Professional Services": "client onboarding, proposal generation, time tracking",
    "E-commerce": "customer support volume, order management, inventory tracking",
    "SaaS": "lead qualification, customer onboarding, churn prevention",
    "Manufacturing": "supply chain coordination, quality control, order processing",
    "Financial Services": "compliance documentation, client reporting, data analysis",
    "Education": "student communication, enrollment management, administrative tasks",
    "Retail": "inventory management, customer engagement, multi-channel coordination",
    "Hospitality": "booking management, guest communication, staff coordination"
}

TONES = {
    "Professional": "formal, business-focused, data-driven",
    "Consultative": "advisory, problem-solving, strategic",
    "Enthusiastic": "energetic, exciting, opportunity-focused",
    "Direct": "straight-forward, no-nonsense, results-oriented",
    "Empathetic": "understanding, relationship-focused, supportive"
}

SCRIPT_TEMPLATES = {
    "Cold Call Opening": {
        "description": "Initial cold call script to capture attention",
        "structure": ["Hook", "Introduction", "Value Proposition", "Permission to Continue"],
        "duration": "30-45 seconds"
    },
    "Discovery Call": {
        "description": "In-depth qualification and needs assessment",
        "structure": ["Rapport Building", "Situation Questions", "Problem Questions", "Implication Questions", "Need-Payoff Questions"],
        "duration": "20-30 minutes"
    },
    "Demo Script": {
        "description": "Product demonstration with storytelling",
        "structure": ["Context Setting", "Problem Acknowledgment", "Solution Walkthrough", "Benefits Highlight", "Next Steps"],
        "duration": "15-20 minutes"
    },
    "Closing Call": {
        "description": "Final pitch and commitment request",
        "structure": ["Summary of Value", "Address Concerns", "Present Offer", "Ask for Commitment", "Handle Final Objections"],
        "duration": "10-15 minutes"
    },
    "Follow-Up Email": {
        "description": "Email sequence after initial contact",
        "structure": ["Subject Line", "Opening", "Value Add", "Call to Action", "Signature"],
        "duration": "N/A"
    },
    "Voicemail Script": {
        "description": "Compelling voicemail to get callbacks",
        "structure": ["Name & Company", "Reason for Call", "Value Teaser", "Call to Action", "Contact Info"],
        "duration": "20-30 seconds"
    }
}

def get_openai_client() -> Optional[OpenAI]:
    """Initialize OpenAI client if API key is available"""
    if st.session_state.openai_api_key and OPENAI_AVAILABLE:
        try:
            return OpenAI(api_key=st.session_state.openai_api_key)
        except Exception as e:
            st.error(f"Error initializing OpenAI client: {str(e)}")
            return None
    return None

def generate_ai_pitch(service: str, industry: str, tone: str, pain_points: List[str], 
                     company_info: str, prospect_name: str, additional_context: str) -> str:
    """Generate AI-powered sales pitch using OpenAI"""
    client = get_openai_client()
    if not client:
        return "OpenAI API key required for AI generation. Please add your key in the sidebar."
    
    service_info = SERVICES[service]
    
    prompt = f"""You are an expert sales consultant for ATM Agency, an AI technology marketing agency. Generate a highly personalized and compelling sales pitch.

COMPANY CONTEXT:
ATM Agency specializes in: Custom AI Apps, PMS/CRM Systems, AI Marketplace, AI Voice Agents, Website & Funnels, and AI Automations.

SERVICE TO PITCH: {service}
Service Description: {service_info['description']}
Key Benefits: {', '.join(service_info['benefits'])}

PROSPECT INFORMATION:
Name: {prospect_name or 'Prospect'}
Industry: {industry}
Pain Points: {', '.join(pain_points)}
Company Info: {company_info or 'Not provided'}
Additional Context: {additional_context or 'None'}

TONE: {tone} ({TONES[tone]})

REQUIREMENTS:
1. Create a personalized opening that addresses their specific pain points
2. Clearly explain how {service} solves their exact challenges
3. Include industry-specific examples and use cases
4. Present ROI in concrete terms relevant to {industry}
5. End with a strong, clear call-to-action
6. Keep it conversational and natural, not robotic
7. Use the {tone} tone throughout
8. Length: 200-300 words

Generate the sales pitch now:"""

    try:
        response = client.chat.completions.create(
            model=st.session_state.ai_model,
            messages=[
                {"role": "system", "content": "You are an expert sales professional specializing in AI technology solutions. You create compelling, personalized pitches that resonate with prospects and drive action."},
                {"role": "user", "content": prompt}
            ],
            temperature=st.session_state.temperature,
            max_tokens=800
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating AI pitch: {str(e)}"

def generate_ai_objection_response(objection: str, context: str, prospect_info: str) -> Dict[str, str]:
    """Generate AI-powered objection responses"""
    client = get_openai_client()
    if not client:
        return {"error": "OpenAI API key required"}
    
    prompt = f"""You are an expert sales trainer. A sales rep encountered this objection:

OBJECTION: "{objection}"

CONTEXT: {context or 'No additional context provided'}
PROSPECT INFO: {prospect_info or 'Not provided'}

Generate 3 different strategic responses to this objection:
1. Empathetic Approach - Acknowledge their concern and build trust
2. Logic-Based Approach - Use data, facts, and reasoning
3. Story-Based Approach - Use a relevant case study or analogy

For each response:
- Start by acknowledging their concern
- Reframe the objection as an opportunity
- Provide a clear path forward
- Include a question to continue dialogue

Format your response as JSON with keys: "empathetic", "logic", "story", and "tips" (array of 3-5 handling tips)."""

    try:
        response = client.chat.completions.create(
            model=st.session_state.ai_model,
            messages=[
                {"role": "system", "content": "You are a master sales trainer who excels at handling objections. You provide strategic, empathetic, and effective responses."},
                {"role": "user", "content": prompt}
            ],
            temperature=st.session_state.temperature,
            max_tokens=1000,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": f"Error generating response: {str(e)}"}

def generate_ai_script(script_type: str, service: str, industry: str, duration: str, 
                      specific_requirements: str) -> str:
    """Generate complete call/email scripts using AI"""
    client = get_openai_client()
    if not client:
        return "OpenAI API key required"
    
    template = SCRIPT_TEMPLATES[script_type]
    service_info = SERVICES[service]
    
    prompt = f"""Generate a complete {script_type} for ATM Agency sales representatives.

SCRIPT TYPE: {script_type}
Description: {template['description']}
Required Structure: {', '.join(template['structure'])}
Target Duration: {template['duration']}

SERVICE: {service}
{service_info['description']}

TARGET INDUSTRY: {industry}
Common Pain Points: {INDUSTRIES[industry]}

SPECIFIC REQUIREMENTS: {specific_requirements or 'None'}

INSTRUCTIONS:
1. Follow the required structure exactly
2. Make it natural and conversational
3. Include specific ATM Agency value propositions
4. Address {industry} pain points specifically
5. Include transition phrases and pauses
6. Add [PAUSE] markers for timing
7. Include alternative phrases for flexibility
8. Make it actionable and ready to use

Generate the complete script with clear sections and formatting:"""

    try:
        response = client.chat.completions.create(
            model=st.session_state.ai_model,
            messages=[
                {"role": "system", "content": "You are an expert sales script writer who creates natural, effective scripts for B2B technology sales. Your scripts feel conversational, not robotic."},
                {"role": "user", "content": prompt}
            ],
            temperature=st.session_state.temperature,
            max_tokens=1500
        )
        
        script = response.choices[0].message.content
        
        # Save to history
        st.session_state.generated_scripts.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": script_type,
            "service": service,
            "industry": industry,
            "script": script
        })
        
        return script
    except Exception as e:
        return f"Error generating script: {str(e)}"

def analyze_pitch_effectiveness(pitch_text: str) -> Dict:
    """Analyze a pitch for effectiveness using AI"""
    client = get_openai_client()
    if not client:
        return {"error": "OpenAI API key required"}
    
    prompt = f"""Analyze this sales pitch for effectiveness:

PITCH:
{pitch_text}

Provide analysis in JSON format with:
1. "score" (0-100): Overall effectiveness score
2. "strengths" (array): 3-5 strong points
3. "weaknesses" (array): 3-5 areas for improvement
4. "suggestions" (array): 3-5 specific improvements
5. "tone_analysis": Description of the current tone
6. "clarity_score" (0-100): How clear and understandable it is
7. "persuasiveness_score" (0-100): How persuasive it is
8. "call_to_action": Evaluation of the CTA (present/absent, strength)"""

    try:
        response = client.chat.completions.create(
            model=st.session_state.ai_model,
            messages=[
                {"role": "system", "content": "You are an expert sales coach who analyzes pitches for effectiveness, clarity, and persuasiveness."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=800,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": f"Analysis error: {str(e)}"}


def generate_pitch(service: str, industry: str, tone: str, pain_points: List[str], include_roi: bool) -> str:
    """Generate a customized sales pitch"""
    service_info = SERVICES[service]
    
    openings = {
        "Professional": f"Thank you for your time. I'm reaching out from ATM Agency because we specialize in helping {industry} companies overcome challenges around {', '.join(pain_points[:2])}.",
        "Consultative": f"I appreciate the opportunity to speak with you. Based on my experience working with {industry} businesses, I've noticed that {pain_points[0]} is a common challenge. Is that something you're experiencing?",
        "Enthusiastic": f"I'm excited to connect with you! ATM Agency has been doing incredible work with {industry} companies, and I think you'll love what we've been achieving around {pain_points[0]}.",
        "Direct": f"Let me get straight to the point: we help {industry} companies eliminate {pain_points[0]} and {pain_points[1] if len(pain_points) > 1 else 'operational inefficiencies'}. Here's how.",
        "Empathetic": f"I know how challenging it can be to deal with {pain_points[0]} in the {industry} space. We've worked with companies facing similar situations, and I'd love to share what's worked for them."
    }
    
    pitch = f"{openings[tone]}\n\n"
    pitch += f"**The Solution: {service}**\n\n"
    pitch += f"{service_info['description']}\n\n"
    pitch += "**Key Benefits for Your Business:**\n"
    for benefit in service_info['benefits'][:3]:
        pitch += f"• {benefit}\n"
    
    pitch += f"\n**Real-World Applications in {industry}:**\n"
    for use_case in service_info['use_cases'][:2]:
        pitch += f"• {use_case}\n"
    
    if include_roi:
        pitch += f"\n**Return on Investment:**\n"
        pitch += f"• {service_info['roi_points']}\n"
        pitch += "• Typical payback period: 3-6 months\n"
        pitch += "• Ongoing monthly savings through automation and efficiency\n"
    
    closings = {
        "Professional": "\nI'd welcome the opportunity to discuss how we can customize this solution for your specific needs. Would you be available for a 30-minute discovery call this week?",
        "Consultative": "\nBased on what I've shared, does this approach resonate with your situation? I'd love to dive deeper into your specific challenges and explore if there's a fit.",
        "Enthusiastic": "\nI'm confident we can deliver amazing results for your business! When can we schedule a demo to show you this in action?",
        "Direct": "\nBottom line: we can solve this problem for you quickly and effectively. Let's schedule 30 minutes to map out a solution. What does your calendar look like?",
        "Empathetic": "\nI'd love to learn more about your specific situation and see how we might be able to help. No pressure - just a conversation. Would that be valuable to you?"
    }
    
    pitch += closings[tone]
    
    return pitch

with st.sidebar:
    st.image("https://placeholder.svg?height=80&width=200&text=ATM+Agency", use_container_width=True)
    
    st.markdown("---")
    
    # API Configuration Section
    st.markdown("### 🤖 AI Configuration")
    
    if OPENAI_AVAILABLE:
        api_key_input = st.text_input(
            "OpenAI API Key",
            type="password",
            value=st.session_state.openai_api_key,
            help="Enter your OpenAI API key to enable AI-powered generation"
        )
        
        if api_key_input != st.session_state.openai_api_key:
            st.session_state.openai_api_key = api_key_input
        
        if st.session_state.openai_api_key:
            st.markdown('<div class="api-status api-active">✓ AI Features Active</div>', unsafe_allow_html=True)
            
            # AI Model Selection
            ai_model = st.selectbox(
                "AI Model",
                ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"],
                index=0,
                help="Select the AI model for generation"
            )
            st.session_state.ai_model = ai_model
            
            # Temperature control
            temperature = st.slider(
                "Creativity Level",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                step=0.1,
                help="Higher values = more creative, Lower values = more focused"
            )
            st.session_state.temperature = temperature
        else:
            st.markdown('<div class="api-status api-inactive">✗ AI Features Inactive</div>', unsafe_allow_html=True)
            st.info("Add your OpenAI API key to unlock AI-powered pitch generation, script creation, and analysis.")
            with st.expander("How to get an API key"):
                st.markdown("""
                1. Go to [platform.openai.com](https://platform.openai.com)
                2. Sign up or log in
                3. Navigate to API keys section
                4. Create a new secret key
                5. Copy and paste it above
                """)
    else:
        st.warning("Install OpenAI: `pip install openai`")
    
    st.markdown("---")
    
    # Navigation
    st.markdown("### Navigation")
    tool_mode = st.radio(
        "Select Tool",
        ["📝 Pitch Generator", "🤖 AI Script Generator", "🛡️ Objection Handler", 
         "📊 Pitch Analyzer", "📚 Service Library", "💡 Quick Tips", "📜 Script History"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Quick Stats
    st.markdown("### 📈 Quick Stats")
    st.metric("Sessions Today", len(st.session_state.conversation_history))
    st.metric("Scripts Generated", len(st.session_state.generated_scripts))
    
    st.markdown("---")
    
    st.markdown("### About ATM Agency")
    st.markdown("""
    **Artificial Intelligence Technology Marketing Agency**
    
    We transform businesses through:
    - Custom AI Applications
    - Intelligent Automation
    - Voice AI Agents
    - Smart CRM/PMS Systems
    """)

# Main App Layout
st.markdown('<h1 class="main-header">🎯 ATM Agency AI Sales Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-Powered Sales Pitch, Script Generator & Objection Handler</p>', unsafe_allow_html=True)

# Main content area
if tool_mode == "📝 Pitch Generator":
    st.header("Generate Customized Sales Pitches")
    
    # Toggle between standard and AI generation
    generation_mode = st.radio(
        "Generation Mode",
        ["Standard Template", "AI-Powered (Recommended)"],
        horizontal=True
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Prospect Information")
        
        selected_service = st.selectbox(
            "Select Service to Pitch",
            list(SERVICES.keys()),
            help="Choose the primary service you want to focus on"
        )
        
        selected_industry = st.selectbox(
            "Prospect's Industry",
            list(INDUSTRIES.keys()),
            help="Select the prospect's industry for targeted messaging"
        )
        
        selected_tone = st.selectbox(
            "Pitch Tone",
            list(TONES.keys()),
            help="Choose the tone that matches your prospect's style"
        )
        
        st.markdown(f"*{TONES[selected_tone]}*")
    
    with col2:
        st.subheader("Customization Options")
        
        default_pain_points = INDUSTRIES[selected_industry]
        pain_points_input = st.text_area(
            "Key Pain Points (comma-separated)",
            value=default_pain_points,
            help="Customize the pain points specific to this prospect"
        )
        pain_points = [p.strip() for p in pain_points_input.split(",")]
        
        include_roi = st.checkbox("Include ROI Information", value=True)
        include_case_study = st.checkbox("Include Case Study Reference", value=False)
        
        prospect_name = st.text_input("Prospect Name (optional)", placeholder="John Smith")
        company_name = st.text_input("Company Name (optional)", placeholder="Acme Corp")
    
    # AI-specific fields
    company_info = ""
    additional_context = ""
    if generation_mode == "AI-Powered (Recommended)":
        st.subheader("Additional Context for AI")
        company_info = st.text_area(
            "Company Information",
            placeholder="e.g., 50 employees, $5M annual revenue, currently using Salesforce...",
            help="More context = better pitch"
        )
        additional_context = st.text_area(
            "Meeting Context / Notes",
            placeholder="e.g., Spoke last week, interested in automation, concerned about implementation time...",
            help="Any additional information that will help personalize the pitch"
        )
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        generate_btn = st.button("🚀 Generate Pitch", type="primary", use_container_width=True)
    with col_btn2:
        regenerate_btn = st.button("🔄 Regenerate", use_container_width=True)
    
    if generate_btn or (generation_mode == "AI-Powered (Recommended)" and regenerate_btn):
        with st.spinner("Crafting your perfect pitch..."):
            if generation_mode == "AI-Powered (Recommended)" and st.session_state.openai_api_key:
                pitch = generate_ai_pitch(
                    selected_service, selected_industry, selected_tone, 
                    pain_points, company_info,
                    prospect_name, additional_context
                )
                box_class = "ai-pitch-box"
                title = "Your AI-Generated Pitch"
            else:
                pitch = generate_pitch(selected_service, selected_industry, selected_tone, pain_points, include_roi)
                box_class = "pitch-box"
                title = "Your Customized Pitch"
            
            if prospect_name and generation_mode != "AI-Powered (Recommended)":
                pitch = f"Hi {prospect_name},\n\n" + pitch
            if company_name and generation_mode != "AI-Powered (Recommended)":
                pitch = pitch.replace("your business", f"{company_name}")
            
            st.markdown(f'<div class="{box_class}">', unsafe_allow_html=True)
            st.markdown(f"### {title}")
            st.markdown(pitch)
            
            if include_case_study:
                st.markdown(f"\n**Case Study Reference:**")
                st.markdown(f"*We recently worked with a {selected_industry} company facing similar challenges. They saw a 45% reduction in operational costs and 3x faster processing times within the first 90 days. I'd be happy to share the detailed case study with you.*")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            col_dl1, col_dl2, col_dl3 = st.columns(3)
            with col_dl1:
                st.download_button(
                    label="📥 Download Pitch",
                    data=pitch,
                    file_name=f"pitch_{selected_service.replace(' ', '_')}_{selected_industry.replace(' ', '_')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            with col_dl2:
                if st.button("📋 Copy to Clipboard", use_container_width=True):
                    st.code(pitch, language=None)
            with col_dl3:
                if generation_mode == "AI-Powered (Recommended)" and st.session_state.openai_api_key:
                    if st.button("📊 Analyze This Pitch", use_container_width=True):
                        with st.spinner("Analyzing..."):
                            analysis = analyze_pitch_effectiveness(pitch)
                            if "error" not in analysis:
                                st.session_state.current_analysis = analysis
                                st.success("Analysis complete! Check the Pitch Analyzer tab.")

elif tool_mode == "🤖 AI Script Generator":
    st.header("AI-Powered Script Generator")
    
    if not st.session_state.openai_api_key:
        st.warning("⚠️ OpenAI API key required. Please add your API key in the sidebar to use this feature.")
        st.info("The AI Script Generator creates complete, ready-to-use scripts for calls, emails, and more.")
    else:
        st.success("✓ AI Script Generation Active")
        
        col1, col2 = st.columns(2)
        
        with col1:
            script_type = st.selectbox(
                "Script Type",
                list(SCRIPT_TEMPLATES.keys()),
                help="Select the type of script you need"
            )
            
            template_info = SCRIPT_TEMPLATES[script_type]
            st.info(f"**{template_info['description']}**\nDuration: {template_info['duration']}")
            
            selected_service_script = st.selectbox(
                "Service Focus",
                list(SERVICES.keys()),
                key="script_service"
            )
            
            selected_industry_script = st.selectbox(
                "Target Industry",
                list(INDUSTRIES.keys()),
                key="script_industry"
            )
        
        with col2:
            specific_requirements = st.text_area(
                "Specific Requirements",
                placeholder="e.g., Emphasize quick implementation, address budget concerns, mention competitor weaknesses...",
                height=150,
                help="Any specific points you want included in the script"
            )
            
            st.markdown("**Script Structure:**")
            for section in template_info['structure']:
                st.markdown(f"• {section}")
        
        if st.button("✨ Generate Complete Script", type="primary", use_container_width=True):
            with st.spinner(f"Generating your {script_type}..."):
                script = generate_ai_script(
                    script_type, selected_service_script, 
                    selected_industry_script, template_info['duration'],
                    specific_requirements
                )
                
                st.markdown('<div class="script-template">', unsafe_allow_html=True)
                st.markdown(f"### {script_type}")
                st.markdown(script)
                st.markdown('</div>', unsafe_allow_html=True)
                
                col_s1, col_s2 = st.columns(2)
                with col_s1:
                    st.download_button(
                        "📥 Download Script",
                        data=script,
                        file_name=f"{script_type.lower().replace(' ', '_')}_{selected_industry_script}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                with col_s2:
                    st.success(f"✓ Saved to Script History")

elif tool_mode == "🛡️ Objection Handler":
    st.header("Objection Handler & Response Generator")
    
    # Toggle between standard and AI
    objection_mode = st.radio(
        "Response Mode",
        ["Standard Responses", "AI-Powered Custom Response"],
        horizontal=True
    )
    
    if objection_mode == "Standard Responses":
        st.subheader("Select Objection Category")
        
        objection_category = st.selectbox(
            "Objection Type",
            list(OBJECTIONS.keys()),
            help="Choose the category that best matches the objection you're facing"
        )
        
        category_data = OBJECTIONS[objection_category]
        
        selected_objection = st.radio(
            "Specific Objection",
            category_data["objections"]
        )
        
        if st.button("💡 Get Response Strategies", type="primary"):
            st.markdown('<div class="objection-box">', unsafe_allow_html=True)
            st.markdown(f"### Objection: *\"{selected_objection}\"*")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("### Recommended Responses")
            
            for idx, response in enumerate(category_data["responses"], 1):
                st.markdown('<div class="response-box">', unsafe_allow_html=True)
                st.markdown(f"**Response Option {idx}:**")
                st.markdown(response)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with st.expander("🎯 Pro Tips for Handling This Objection"):
                if objection_category == "Price/Budget":
                    st.markdown("""
                    - Never apologize for your pricing
                    - Reframe as investment, not cost
                    - Use ROI calculations and case studies
                    - Offer payment plans or phased approach
                    - Ask about cost of NOT solving the problem
                    """)
                elif objection_category == "Timing":
                    st.markdown("""
                    - Create urgency with opportunity cost
                    - Offer pilot program or limited engagement
                    - Understand what "ready" means to them
                    - Get commitment for follow-up
                    - Share what competitors are doing
                    """)
                elif objection_category == "Trust/Skepticism":
                    st.markdown("""
                    - Acknowledge past bad experiences
                    - Offer proof: case studies, references, demos
                    - Start small with pilot project
                    - Provide guarantees or performance clauses
                    - Build relationship before asking for commitment
                    """)
                elif objection_category == "DIY/In-House":
                    st.markdown("""
                    - Respect their existing resources
                    - Highlight specialized expertise and speed
                    - Offer collaborative approach
                    - Discuss opportunity cost
                    - Position as augmentation, not replacement
                    """)
                elif objection_category == "Understanding/Clarity":
                    st.markdown("""
                    - Simplify the explanation
                    - Use analogies and real-world examples
                    - Offer demo or trial
                    - Focus on outcomes, not technology
                    - Provide educational resources
                    """)
                elif objection_category == "Need/Priority":
                    st.markdown("""
                    - Challenge their status quo
                    - Uncover hidden costs of current approach
                    - Align with their strategic goals
                    - Offer audit to reveal opportunities
                    - Show competitive disadvantage of waiting
                    """)
    
    else:  # AI-Powered Custom Response
        if not st.session_state.openai_api_key:
            st.warning("⚠️ OpenAI API key required for AI-powered objection handling.")
        else:
            st.subheader("AI-Powered Custom Objection Handler")
            
            custom_objection = st.text_area(
                "Enter the objection you're facing",
                placeholder="Example: We're currently locked into a 2-year contract with another vendor...",
                height=100
            )
            
            context = st.text_area(
                "Additional Context",
                placeholder="Meeting notes, prospect background, previous conversations...",
                height=80
            )
            
            prospect_info = st.text_input(
                "Prospect Info",
                placeholder="Company size, industry, decision maker role..."
            )
            
            if st.button("🧠 Generate AI Response Strategy", type="primary"):
                if custom_objection:
                    with st.spinner("Analyzing objection and generating responses..."):
                        responses = generate_ai_objection_response(custom_objection, context, prospect_info)
                        
                        if "error" not in responses:
                            st.markdown('<div class="objection-box">', unsafe_allow_html=True)
                            st.markdown(f"### Objection: *\"{custom_objection}\"*")
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            st.markdown("### AI-Generated Response Strategies")
                            
                            # Empathetic Response
                            st.markdown('<div class="response-box">', unsafe_allow_html=True)
                            st.markdown("**🤝 Empathetic Approach:**")
                            st.markdown(responses.get("empathetic", "N/A"))
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            # Logic-Based Response
                            st.markdown('<div class="response-box">', unsafe_allow_html=True)
                            st.markdown("**📊 Logic-Based Approach:**")
                            st.markdown(responses.get("logic", "N/A"))
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            # Story-Based Response
                            st.markdown('<div class="response-box">', unsafe_allow_html=True)
                            st.markdown("**📖 Story-Based Approach:**")
                            st.markdown(responses.get("story", "N/A"))
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            # Pro Tips
                            if "tips" in responses:
                                with st.expander("🎯 Handling Tips"):
                                    for tip in responses["tips"]:
                                        st.markdown(f"• {tip}")
                        else:
                            st.error(responses["error"])
                else:
                    st.warning("Please enter an objection to get response strategies")

elif tool_mode == "📊 Pitch Analyzer":
    st.header("AI Pitch Analyzer")
    
    if not st.session_state.openai_api_key:
        st.warning("⚠️ OpenAI API key required for pitch analysis.")
    else:
        if st.session_state.current_analysis:
            st.success("Previous analysis found. Displaying below or clear to analyze new pitch.")
            analysis = st.session_state.current_analysis
            col_score1, col_score2, col_score3 = st.columns(3)
            
            with col_score1:
                st.metric("Overall Score", f"{analysis.get('score', 0)}/100")
            with col_score2:
                st.metric("Clarity", f"{analysis.get('clarity_score', 0)}/100")
            with col_score3:
                st.metric("Persuasiveness", f"{analysis.get('persuasiveness_score', 0)}/100")
            
            col_analysis1, col_analysis2 = st.columns(2)
            
            with col_analysis1:
                st.markdown("### ✅ Strengths")
                for strength in analysis.get('strengths', []):
                    st.success(f"• {strength}")
                
                st.markdown("### 💡 Suggestions")
                for suggestion in analysis.get('suggestions', []):
                    st.info(f"• {suggestion}")
            
            with col_analysis2:
                st.markdown("### ⚠️ Areas for Improvement")
                for weakness in analysis.get('weaknesses', []):
                    st.warning(f"• {weakness}")
                
                st.markdown("### 🎭 Tone Analysis")
                st.write(analysis.get('tone_analysis', 'N/A'))
                
                st.markdown("### 📞 Call-to-Action")
                st.write(analysis.get('call_to_action', 'N/A'))
            
            if st.button("Clear Analysis", key="clear_analysis"):
                st.session_state.current_analysis = None
                st.rerun()

        st.info("Paste your sales pitch below to get detailed AI analysis and improvement suggestions.")
        
        pitch_to_analyze = st.text_area(
            "Your Sales Pitch",
            placeholder="Paste your pitch here...",
            height=200
        )
        
        if st.button("🔍 Analyze Pitch", type="primary"):
            if pitch_to_analyze:
                with st.spinner("Analyzing your pitch..."):
                    analysis = analyze_pitch_effectiveness(pitch_to_analyze)
                    
                    if "error" not in analysis:
                        st.session_state.current_analysis = analysis
                        st.success("Analysis complete! Displaying results below.")
                        
                        col_score1, col_score2, col_score3 = st.columns(3)
                        
                        with col_score1:
                            st.metric("Overall Score", f"{analysis.get('score', 0)}/100")
                        with col_score2:
                            st.metric("Clarity", f"{analysis.get('clarity_score', 0)}/100")
                        with col_score3:
                            st.metric("Persuasiveness", f"{analysis.get('persuasiveness_score', 0)}/100")
                        
                        col_analysis1, col_analysis2 = st.columns(2)
                        
                        with col_analysis1:
                            st.markdown("### ✅ Strengths")
                            for strength in analysis.get('strengths', []):
                                st.success(f"• {strength}")
                            
                            st.markdown("### 💡 Suggestions")
                            for suggestion in analysis.get('suggestions', []):
                                st.info(f"• {suggestion}")
                        
                        with col_analysis2:
                            st.markdown("### ⚠️ Areas for Improvement")
                            for weakness in analysis.get('weaknesses', []):
                                st.warning(f"• {weakness}")
                            
                            st.markdown("### 🎭 Tone Analysis")
                            st.write(analysis.get('tone_analysis', 'N/A'))
                            
                            st.markdown("### 📞 Call-to-Action")
                            st.write(analysis.get('call_to_action', 'N/A'))
                    else:
                        st.error(analysis["error"])
            else:
                st.warning("Please enter a pitch to analyze")

elif tool_mode == "📚 Service Library":
    st.header("Complete Service Catalog")
    st.markdown("*Detailed information about all ATM Agency services*")
    
    for service_name, service_info in SERVICES.items():
        with st.expander(f"🔹 {service_name}", expanded=False):
            st.markdown(f"**{service_info['description']}**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### Key Benefits")
                for benefit in service_info['benefits']:
                    st.markdown(f"✅ {benefit}")
            
            with col2:
                st.markdown("##### Use Cases")
                for use_case in service_info['use_cases']:
                    st.markdown(f"💡 {use_case}")
            
            st.markdown("##### ROI Information")
            st.info(service_info['roi_points'])
            
            if st.button(f"Generate Quick Pitch for {service_name}", key=f"quick_{service_name}"):
                quick_pitch = f"""
**Quick Pitch for {service_name}:**

{service_info['description']}

**Top 3 Benefits:**
1. {service_info['benefits'][0]}
2. {service_info['benefits'][1]}
3. {service_info['benefits'][2]}

**ROI:** {service_info['roi_points']}

**Next Step:** "Would you like to see a demo of how this would work specifically for your business?"
                """
                st.success(quick_pitch)

elif tool_mode == "📜 Script History":
    st.header("Generated Scripts History")
    
    if len(st.session_state.generated_scripts) == 0:
        st.info("No scripts generated yet. Use the AI Script Generator to create your first script!")
    else:
        st.success(f"You have {len(st.session_state.generated_scripts)} saved scripts")
        
        for idx, script_data in enumerate(reversed(st.session_state.generated_scripts)):
            with st.expander(f"{script_data['type']} - {script_data['service']} ({script_data['timestamp']})"):
                st.markdown(f"**Industry:** {script_data['industry']}")
                st.markdown(f"**Generated:** {script_data['timestamp']}")
                st.markdown("---")
                st.markdown(script_data['script'])
                
                col_h1, col_h2 = st.columns(2)
                with col_h1:
                    st.download_button(
                        "📥 Download",
                        data=script_data['script'],
                        file_name=f"{script_data['type']}_{script_data['timestamp']}.txt",
                        key=f"download_{idx}"
                    )
                with col_h2:
                    if st.button("🗑️ Delete", key=f"delete_{idx}"):
                        st.session_state.generated_scripts.remove(script_data)
                        st.rerun()

else:  # Quick Tips
    st.header("💡 Sales Tips & Best Practices")
    
    tips_category = st.selectbox(
        "Select Topic",
        ["Discovery Questions", "Closing Techniques", "Follow-Up Strategies", "Value Proposition", "Competitive Positioning"]
    )
    
    if tips_category == "Discovery Questions":
        st.markdown("""
        ### Powerful Discovery Questions
        
        **Current State Questions:**
        - "Walk me through your current process for [relevant task]..."
        - "How much time does your team spend on [manual task] each week?"
        - "What systems are you currently using for [operation]?"
        - "What's working well with your current approach?"
        
        **Pain Point Questions:**
        - "What's the most frustrating part of [process] for your team?"
        - "If you could wave a magic wand and fix one thing, what would it be?"
        - "What's keeping you up at night regarding [business area]?"
        - "Where are you losing money due to inefficiency?"
        
        **Impact Questions:**
        - "How does this challenge affect your bottom line?"
        - "What would it mean for your business if you could solve this?"
        - "How is this limiting your growth?"
        - "What opportunities are you missing because of this?"
        
        **Decision Process Questions:**
        - "Who else is involved in decisions like this?"
        - "What's your typical evaluation process?"
        - "What criteria are most important to you?"
        - "When do you need this solution in place?"
        
        **Vision Questions:**
        - "Where do you want your company to be in 3 years?"
        - "What does success look like for this project?"
        - "How will you measure ROI?"
        - "What would make this a home run for you?"
        """)
    
    elif tips_category == "Closing Techniques":
        st.markdown("""
        ### Effective Closing Techniques
        
        **1. Assumptive Close**
        - "When would you like to start the implementation?"
        - "Should we schedule the onboarding for next week or the following?"
        
        **2. Summary Close**
        - "So we've agreed that [benefit 1], [benefit 2], and [benefit 3] are important. Let's move forward with making this happen."
        
        **3. Puppy Dog Close**
        - "Let's do a 30-day pilot. If you don't see value, we'll part ways as friends."
        
        **4. Alternative Choice Close**
        - "Would the Pro package or Enterprise package work better for your needs?"
        
        **5. Urgency Close**
        - "We have availability to start in the next two weeks. After that, we're booked until Q2. Should we lock in your spot?"
        
        **6. ROI Close**
        - "Based on our analysis, you'll save $X per month. The investment pays for itself in Y months. When should we get started?"
        
        **7. Takeaway Close**
        - "I'm not sure we're the right fit if [criterion]. Are you confident you can [requirement]?"
        
        **8. Trial Close**
        - "How does everything sound so far?"
        - "Do you see how this would work for your team?"
        - "Is there anything holding you back from moving forward?"
        """)
    
    elif tips_category == "Follow-Up Strategies":
        st.markdown("""
        ### Strategic Follow-Up Approaches
        
        **Timing:**
        - First follow-up: 24 hours after initial meeting
        - Second follow-up: 3-4 days later
        - Third follow-up: 7 days later
        - Monthly check-ins for longer sales cycles
        
        **Follow-Up Templates:**
        
        **Day 1 - Thank You + Value:**
