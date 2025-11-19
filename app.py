import streamlit as st
from typing import Dict, List, Optional
import json
from datetime import datetime
import os

# --- Configuration Data (Embedded) ---
SERVICES = {
    "Custom AI Apps": {
        "description": "Bespoke AI-powered applications tailored to your business needs",
        "benefits": ["Automate workflows by 70%+", "Scale without headcount", "Competitive advantage", "Seamless integration"],
        "use_cases": ["Document processing", "Predictive analytics", "Virtual agents", "Workflow automation"],
        "roi_points": "300-500% ROI within first year"
    },
    "PMS/CRM Systems": {
        "description": "AI-enhanced Project Management and CRM platforms",
        "benefits": ["Centralize client data", "AI-powered lead scoring", "Automated follow-ups", "Real-time analytics"],
        "use_cases": ["Sales pipeline management", "Resource allocation", "Customer lifecycle management", "Automated reporting"],
        "roi_points": "35% sales conversion increase, 60% admin time reduction"
    },
    "AI Marketplace": {
        "description": "Custom marketplace platforms with AI matching and pricing",
        "benefits": ["AI recommendations", "Intelligent search", "Automated matching", "Dynamic pricing"],
        "use_cases": ["B2B marketplaces", "E-commerce engines", "Talent platforms", "Resource sharing"],
        "roi_points": "45% transaction volume increase, 25% platform stickiness boost"
    },
    "AI Voice Agents": {
        "description": "24/7 intelligent voice assistants for customer service and sales",
        "benefits": ["Unlimited simultaneous calls", "Multi-language support", "Auto lead qualification", "80% cost reduction"],
        "use_cases": ["Customer support", "Sales calls", "Appointment scheduling", "Order taking"],
        "roi_points": "$50,000+ annual savings per rep replaced"
    },
    "Website & Funnels": {
        "description": "High-converting websites and sales funnels with AI optimization",
        "benefits": ["AI personalization", "Real-time A/B testing", "Intelligent chatbots", "CRO through ML"],
        "use_cases": ["Lead generation pages", "E-commerce funnels", "SaaS onboarding", "Event registration"],
        "roi_points": "2-3x conversion rate increase within 90 days"
    },
    "AI Automations": {
        "description": "End-to-end business process automation with AI",
        "benefits": ["Eliminate manual tasks", "Unified workflows", "Intelligent decisions", "Scale without hiring"],
        "use_cases": ["Data entry automation", "Email automation", "Social media management", "Report generation"],
        "roi_points": "20-30 hours saved per employee weekly"
    }
}

OBJECTIONS = {
    "Price/Budget": ["It's too expensive", "We don't have the budget", "Your competitors are cheaper", "Can you give us a discount?"],
    "Timing": ["We're not ready yet", "Maybe next quarter", "We need to discuss internally", "Call me back later"],
    "Trust/Skepticism": ["We've been burned before", "How do we know this will work?", "Can you guarantee results?", "Sounds too good to be true"],
    "DIY/In-House": ["We can build this in-house", "We have a tech team", "We're with another vendor", "We want to try ourselves first"],
    "Understanding": ["I don't understand AI", "This seems complicated", "We're not a tech company", "Will our team use this?"],
    "Need/Priority": ["We're doing fine", "Not a priority now", "We don't have this problem", "Focused on other initiatives"]
}

INDUSTRIES = {
    "Real Estate": "long sales cycles, lead qualification, property management, document processing",
    "Healthcare": "administrative burden, scheduling, patient communication, billing compliance",
    "Professional Services": "client onboarding, proposal generation, time tracking, resource utilization",
    "E-commerce": "customer support volume, order management, inventory, personalization",
    "SaaS": "lead qualification, onboarding, churn prevention, feature adoption",
    "Manufacturing": "supply chain, quality control, order processing, predictive maintenance",
    "Financial Services": "compliance, client reporting, data analysis, fraud detection",
    "Education": "student communication, enrollment, administrative tasks, personalized learning",
    "Retail": "inventory management, customer engagement, multi-channel, demand forecasting",
    "Hospitality": "booking management, guest communication, staff coordination, dynamic pricing"
}

TONES = {
    "Professional": "Formal, business-focused, data-driven",
    "Consultative": "Advisory, problem-solving, strategic",
    "Enthusiastic": "Energetic, exciting, opportunity-focused",
    "Direct": "Straight-forward, results-oriented",
    "Empathetic": "Understanding, relationship-focused"
}

SALES_STRATEGIES = {
    "Value-Based Selling": {
        "description": "Focus on economic value and ROI",
        "principles": ["Quantify status quo cost", "Align with business goals", "Prove ROI with data"]
    },
    "Challenger Sale": {
        "description": "Challenge assumptions and teach new perspectives",
        "principles": ["Teach unique insights", "Tailor to prospect role", "Take control of conversation"]
    },
    "Solution Selling": {
        "description": "Diagnose problems and craft tailored solutions",
        "principles": ["Ask open-ended questions", "Focus on the why", "Present comprehensive roadmap"]
    },
    "SPIN Selling": {
        "description": "Question-based selling methodology",
        "principles": ["Situation questions", "Problem questions", "Implication questions", "Need-payoff questions"]
    }
}

SCRIPT_TEMPLATES = {
    "Cold Call Opening": {"description": "Initial cold call to secure meeting", "duration": "30-45 seconds"},
    "Discovery Call": {"description": "Deep-dive conversation to uncover needs", "duration": "20-30 minutes"},
    "Demo Script": {"description": "Product demonstration with storytelling", "duration": "15-20 minutes"},
    "Closing Call": {"description": "Final pitch to secure deal", "duration": "10-15 minutes"},
    "Follow-Up Email": {"description": "Post-meeting email with value", "duration": "N/A"},
    "Voicemail Script": {"description": "Concise voicemail for callback", "duration": "20-30 seconds"}
}

AI_MODELS = ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]

SYSTEM_PROMPTS = {
    "pitch_generator": "You are an expert sales consultant for ATM Agency. Generate highly personalized, compelling sales pitches focused on quantifiable business outcomes.",
    "objection_handler": "You are a master sales trainer. Provide strategic, empathetic objection responses as JSON: {empathetic, logic, story, handling_tips}.",
    "script_writer": "You are an expert sales script writer. Create natural, conversational B2B scripts ready for immediate use."
}

# --- OpenAI Client Setup ---
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

def get_openai_client() -> Optional[OpenAI]:
    """Initialize OpenAI client"""
    api_key = st.session_state.get('openai_api_key') or os.environ.get('OPENAI_API_KEY')
    if api_key and OPENAI_AVAILABLE:
        try:
            return OpenAI(api_key=api_key)
        except Exception as e:
            st.error(f"Error: {str(e)}")
            return None
    return None

# --- Session State ---
def init_session():
    defaults = {
        'openai_api_key': os.environ.get('OPENAI_API_KEY', ''),
        'generated_scripts': [],
        'current_analysis': None,
        'ai_model': "gpt-4o-mini",
        'temperature': 0.7,
        'sales_strategy': "Value-Based Selling"
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

# --- AI Functions ---
def generate_pitch(service: str, industry: str, tone: str, pain_points: List[str], 
                   company_info: str, prospect_name: str, additional_context: str, strategy: str) -> str:
    client = get_openai_client()
    if not client:
        return "⚠️ OpenAI API key required. Please enter it above."
    
    service_info = SERVICES.get(service, {})
    strategy_info = SALES_STRATEGIES.get(strategy, {})
    
    prompt = f"""Generate a personalized sales pitch for ATM Agency.

SERVICE: {service}
Description: {service_info.get('description')}
Benefits: {', '.join(service_info.get('benefits', []))}
ROI: {service_info.get('roi_points')}

PROSPECT: {prospect_name or 'Prospect'} | Industry: {industry}
Pain Points: {', '.join(pain_points) if pain_points else 'General'}
Company: {company_info or 'Not provided'}
Context: {additional_context or 'None'}

STRATEGY: {strategy} - {', '.join(strategy_info.get('principles', []))}
TONE: {tone}

Requirements:
1. Personalized opening addressing {industry} pain points
2. Explain how {service} solves their challenges using {strategy}
3. Present concrete ROI relevant to {industry}
4. Strong call-to-action
5. {tone} tone throughout
6. 250-350 words

Generate now:"""

    try:
        response = client.chat.completions.create(
            model=st.session_state.ai_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPTS['pitch_generator']},
                {"role": "user", "content": prompt}
            ],
            temperature=st.session_state.temperature,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {str(e)}"

def generate_objection_response(objection: str, context: str, prospect_info: str) -> Dict:
    client = get_openai_client()
    if not client:
        return {"error": "API key required"}
    
    prompt = f"""Handle this sales objection:
OBJECTION: "{objection}"
CONTEXT: {context or 'None'}
PROSPECT: {prospect_info or 'None'}

Generate 3 strategic responses:
1. Empathetic - Build trust and acknowledge concern
2. Logic - Use data and facts
3. Story - Use case study or analogy

Format as JSON: {{"empathetic": "...", "logic": "...", "story": "...", "handling_tips": ["tip1", "tip2", "tip3", "tip4", "tip5"]}}
Return ONLY valid JSON."""

    try:
        response = client.chat.completions.create(
            model=st.session_state.ai_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPTS['objection_handler']},
                {"role": "user", "content": prompt}
            ],
            temperature=st.session_state.temperature,
            max_tokens=1200,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}

def generate_script(script_type: str, service: str, industry: str, requirements: str) -> str:
    client = get_openai_client()
    if not client:
        return "⚠️ API key required"
    
    template = SCRIPT_TEMPLATES.get(script_type, {})
    service_info = SERVICES.get(service, {})
    
    prompt = f"""Generate a complete {script_type} for ATM Agency.

TYPE: {script_type}
Description: {template.get('description')}
Duration: {template.get('duration')}

SERVICE: {service}
Description: {service_info.get('description')}

INDUSTRY: {industry}
Pain Points: {INDUSTRIES.get(industry)}

REQUIREMENTS: {requirements or 'Standard approach'}

Instructions:
1. Natural, conversational tone
2. Include ATM Agency value propositions
3. Address {industry} pain points specifically
4. Use clear section headings
5. Include transitions, pauses [PAUSE], alternatives *Option A/B*
6. Include anticipated objections section
7. Detailed and ready-to-use

Generate complete script:"""

    try:
        response = client.chat.completions.create(
            model=st.session_state.ai_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPTS['script_writer']},
                {"role": "user", "content": prompt}
            ],
            temperature=st.session_state.temperature,
            max_tokens=2000
        )
        script = response.choices[0].message.content
        st.session_state.generated_scripts.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": script_type,
            "service": service,
            "script": script
        })
        return script
    except Exception as e:
        return f"❌ Error: {str(e)}"

# --- Main App ---
def main():
    init_session()
    
    st.set_page_config(page_title="ATM Agency - AI Sales Assistant", page_icon="🎯", layout="wide")
    
    # Custom CSS
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }
        .pitch-box {
            background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
            border-left: 4px solid #667eea;
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
            white-space: pre-wrap;
        }
        .response-box {
            background-color: #f0fdf4;
            border-left: 4px solid #22c55e;
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
        }
        .script-box {
            background-color: #fef3c7;
            border-left: 4px solid #f59e0b;
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
            white-space: pre-wrap;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
        }
        .stTabs [data-baseweb="tab"] {
            font-size: 1.1rem;
            font-weight: 600;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1 class='main-header'>🎯 ATM Agency - AI Sales Assistant</h1>", unsafe_allow_html=True)
    st.markdown("Generate hyper-personalized pitches, handle objections, and create complete sales scripts powered by AI.")
    
    # API Key Input at top
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        api_key_input = st.text_input(
            "OpenAI API Key",
            type="password",
            value=st.session_state.openai_api_key,
            placeholder="sk-...",
            help="Enter your OpenAI API key to use AI generation features"
        )
        if api_key_input != st.session_state.openai_api_key:
            st.session_state.openai_api_key = api_key_input
            st.rerun()
    
    with col2:
        st.session_state.ai_model = st.selectbox("Model", AI_MODELS, index=AI_MODELS.index(st.session_state.ai_model))
    
    with col3:
        st.session_state.temperature = st.slider("Creativity", 0.0, 1.0, st.session_state.temperature, 0.1)
    
    st.markdown("---")
    
    # Main Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Pitch Generator", "🛡️ Objection Handler", "📝 Script Generator", "📚 Service Catalog"])
    
    # TAB 1: Pitch Generator
    with tab1:
        st.subheader("Personalized AI Sales Pitch Generator")
        
        col1, col2 = st.columns(2)
        with col1:
            prospect_name = st.text_input("Prospect Name", placeholder="Sarah Connor")
            company_info = st.text_area("Company Info (Optional)", height=80, placeholder="Mid-sized regional bank, 500 employees...")
            additional_context = st.text_area("Additional Context (Optional)", height=80, placeholder="Focus on compliance issues...")
        
        with col2:
            service = st.selectbox("Service to Pitch", list(SERVICES.keys()))
            industry = st.selectbox("Prospect Industry", list(INDUSTRIES.keys()))
            tone = st.selectbox("Pitch Tone", list(TONES.keys()))
            strategy = st.selectbox("Sales Strategy", list(SALES_STRATEGIES.keys()))
            
            default_pains = INDUSTRIES.get(industry, "").split(', ')
            pain_points = st.multiselect(
                "Specific Pain Points",
                options=default_pains + ["High costs", "Low conversion", "Poor data quality", "Legacy systems"],
                default=default_pains[:2]
            )
        
        if st.button("🚀 Generate Pitch", use_container_width=True, type="primary"):
            if not get_openai_client():
                st.error("⚠️ Please enter your OpenAI API key above")
            else:
                with st.spinner("Generating personalized pitch..."):
                    pitch = generate_pitch(service, industry, tone, pain_points, company_info, prospect_name, additional_context, strategy)
                    st.session_state.current_analysis = {"type": "pitch", "content": pitch, "service": service, "industry": industry, "tone": tone}
                    st.rerun()
        
        if st.session_state.current_analysis and st.session_state.current_analysis.get("type") == "pitch":
            st.markdown("### Generated Pitch")
            st.markdown(f"**Service:** {st.session_state.current_analysis['service']} | **Industry:** {st.session_state.current_analysis['industry']} | **Tone:** {st.session_state.current_analysis['tone']}")
            st.markdown(f"<div class='pitch-box'>{st.session_state.current_analysis['content']}</div>", unsafe_allow_html=True)
            st.download_button("📥 Download as TXT", st.session_state.current_analysis['content'], f"pitch_{datetime.now().strftime('%Y%m%d')}.txt")
    
    # TAB 2: Objection Handler
    with tab2:
        st.subheader("AI Objection Handler & Training")
        
        col1, col2 = st.columns(2)
        with col1:
            objection_cat = st.selectbox("Objection Category", list(OBJECTIONS.keys()))
            predefined = OBJECTIONS.get(objection_cat, [])
            objection_select = st.selectbox("Select or Enter Custom", ["Custom"] + predefined)
            
            if objection_select == "Custom":
                final_objection = st.text_input("Custom Objection", placeholder="We only work with vendors who...")
            else:
                final_objection = objection_select
        
        with col2:
            context = st.text_area("Conversation Context", height=100, placeholder="Said after ROI presentation...")
            prospect_info = st.text_area("Prospect Details", height=100, placeholder="CFO of manufacturing firm...")
        
        if st.button("💡 Generate Responses", use_container_width=True, type="primary"):
            if not get_openai_client():
                st.error("⚠️ Please enter your OpenAI API key above")
            elif not final_objection:
                st.error("Please enter or select an objection")
            else:
                with st.spinner("Generating strategic responses..."):
                    data = generate_objection_response(final_objection, context, prospect_info)
                    st.session_state.current_analysis = {"type": "objection", "objection": final_objection, "data": data}
                    st.rerun()
        
        if st.session_state.current_analysis and st.session_state.current_analysis.get("type") == "objection":
            data = st.session_state.current_analysis['data']
            if "error" in data:
                st.error(f"Error: {data['error']}")
            else:
                st.markdown(f"### Responses for: *{st.session_state.current_analysis['objection']}*")
                st.markdown("#### 🤝 Empathetic Approach")
                st.markdown(f"<div class='response-box'>{data.get('empathetic', 'N/A')}</div>", unsafe_allow_html=True)
                st.markdown("#### 🧠 Logic-Based Approach")
                st.markdown(f"<div class='response-box'>{data.get('logic', 'N/A')}</div>", unsafe_allow_html=True)
                st.markdown("#### 📖 Story-Based Approach")
                st.markdown(f"<div class='response-box'>{data.get('story', 'N/A')}</div>", unsafe_allow_html=True)
                st.markdown("#### 💡 Handling Tips")
                for i, tip in enumerate(data.get('handling_tips', []), 1):
                    st.markdown(f"**{i}.** {tip}")
    
    # TAB 3: Script Generator
    with tab3:
        st.subheader("Comprehensive Sales Script Generator")
        
        col1, col2 = st.columns(2)
        with col1:
            script_type = st.selectbox("Script Type", list(SCRIPT_TEMPLATES.keys()))
            service = st.selectbox("Target Service", list(SERVICES.keys()), key="script_service")
        
        with col2:
            industry = st.selectbox("Target Industry", list(INDUSTRIES.keys()), key="script_industry")
            requirements = st.text_area("Specific Requirements (Optional)", height=100, placeholder="Mention recent regulation changes...")
        
        if st.button("📝 Generate Script", use_container_width=True, type="primary"):
            if not get_openai_client():
                st.error("⚠️ Please enter your OpenAI API key above")
            else:
                with st.spinner("Generating complete script..."):
                    script = generate_script(script_type, service, industry, requirements)
                    st.session_state.current_analysis = {"type": "script", "content": script, "script_type": script_type, "service": service}
                    st.rerun()
        
        if st.session_state.current_analysis and st.session_state.current_analysis.get("type") == "script":
            st.markdown(f"### Generated {st.session_state.current_analysis['script_type']}")
            st.markdown(f"**Service:** {st.session_state.current_analysis['service']}")
            st.markdown(f"<div class='script-box'>{st.session_state.current_analysis['content']}</div>", unsafe_allow_html=True)
            st.download_button("📥 Download as MD", st.session_state.current_analysis['content'], f"script_{datetime.now().strftime('%Y%m%d')}.md", mime="text/markdown")
    
    # TAB 4: Service Catalog
    with tab4:
        st.subheader("ATM Agency Service Catalog")
        for service_name, data in SERVICES.items():
            with st.expander(f"**{service_name}** - {data['description']}", expanded=False):
                st.markdown("**Key Benefits:**")
                for b in data['benefits']:
                    st.markdown(f"- {b}")
                st.markdown("**Use Cases:**")
                for uc in data['use_cases']:
                    st.markdown(f"- {uc}")
                st.info(f"**ROI:** {data['roi_points']}")

if __name__ == "__main__":
    main()
