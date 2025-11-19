import streamlit as st
from typing import Dict, List, Optional
import json
from datetime import datetime
import os

# Import configuration data
try:
    from config import SERVICES, OBJECTIONS, INDUSTRIES, TONES, SCRIPT_TEMPLATES, SALES_STRATEGIES, AI_MODELS, SYSTEM_PROMPTS
except ImportError:
    st.error("Configuration file (config.py) not found. Please ensure it is in the same directory.")
    st.stop()

# --- OpenAI Client Setup ---
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    st.warning("OpenAI library not available. Install with: pip install openai")

def get_openai_client() -> Optional[OpenAI]:
    """Initialize OpenAI client if API key is available"""
    api_key = st.session_state.get('openai_api_key') or os.environ.get('OPENAI_API_KEY')
    if api_key and OPENAI_AVAILABLE:
        try:
            # Base URL is pre-configured in the environment for Manus
            return OpenAI(api_key=api_key)
        except Exception as e:
            st.error(f"Error initializing OpenAI client: {str(e)}")
            return None
    return None

# --- Session State Initialization ---
def initialize_session_state():
    """Initialize all necessary session state variables."""
    if 'openai_api_key' not in st.session_state:
        st.session_state.openai_api_key = ""
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    if 'generated_scripts' not in st.session_state:
        st.session_state.generated_scripts = []
    if 'current_analysis' not in st.session_state:
        st.session_state.current_analysis = None
    if 'ai_model' not in st.session_state:
        st.session_state.ai_model = AI_MODELS[0] if AI_MODELS else "gpt-4o-mini"
    if 'temperature' not in st.session_state:
        st.session_state.temperature = 0.7
    if 'sales_strategy' not in st.session_state:
        st.session_state.sales_strategy = list(SALES_STRATEGIES.keys())[0]

# --- AI Generation Functions ---

@st.cache_data(show_spinner="Generating Personalized Sales Pitch...")
def generate_ai_pitch(service: str, industry: str, tone: str, pain_points: List[str], 
                     company_info: str, prospect_name: str, additional_context: str, strategy: str) -> str:
    """Generate AI-powered sales pitch using OpenAI"""
    client = get_openai_client()
    if not client:
        return "OpenAI API key required for AI generation. Please add your key in the sidebar."
    
    service_info = SERVICES.get(service, {})
    strategy_info = SALES_STRATEGIES.get(strategy, {})
    
    prompt = f"""
    ATM Agency specializes in: {', '.join(SERVICES.keys())}.
    
    SERVICE TO PITCH: {service}
    Description: {service_info.get('description', 'N/A')}
    Key Benefits: {', '.join(service_info.get('benefits', []))}
    
    SALES STRATEGY: {strategy}
    Strategy Principles: {', '.join(strategy_info.get('principles', []))}
    
    PROSPECT INFORMATION:
    Name: {prospect_name or 'Prospect'}
    Industry: {industry}
    Pain Points: {', '.join(pain_points)}
    Company Info: {company_info or 'Not provided'}
    Additional Context: {additional_context or 'None'}
    
    TONE: {tone} ({TONES.get(tone, 'N/A')})
    
    REQUIREMENTS:
    1. Create a personalized opening that addresses their specific pain points in the context of the {industry} industry.
    2. Clearly explain how {service} solves their exact challenges, adhering to the principles of the {strategy} strategy.
    3. Present ROI in concrete terms relevant to {industry} using data from the service configuration.
    4. End with a strong, clear call-to-action (e.g., "Schedule a 15-minute deep-dive").
    5. Keep it conversational, natural, and highly persuasive.
    6. Use the {tone} tone throughout.
    7. Length: 250-350 words (longer and more detailed than a simple pitch).
    
    Generate the sales pitch now:
    """

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
        return f"Error generating AI pitch: {str(e)}"

@st.cache_data(show_spinner="Generating Objection Handling Strategies...")
def generate_ai_objection_response(objection: str, context: str, prospect_info: str) -> Dict[str, str]:
    """Generate AI-powered objection responses with a focus on structured JSON output."""
    client = get_openai_client()
    if not client:
        return {"error": "OpenAI API key required"}
    
    prompt = f"""
    A sales rep encountered this objection:
    OBJECTION: "{objection}"
    
    CONTEXT: {context or 'No additional context provided'}
    PROSPECT INFO: {prospect_info or 'Not provided'}
    
    Generate 3 different strategic responses to this objection:
    1. Empathetic Approach - Acknowledge their concern and build trust.
    2. Logic-Based Approach - Use data, facts, and reasoning to reframe the value.
    3. Story-Based Approach - Use a relevant, anonymized case study or analogy to illustrate success.
    
    For each response, ensure it is a complete, persuasive paragraph.
    
    Format your response as a single JSON object with the following keys: 
    "empathetic", "logic", "story", and "handling_tips" (an array of 5 concise, actionable tips for the sales rep).
    """

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
        return {"error": f"Error generating response: {str(e)}"}

@st.cache_data(show_spinner="Generating Comprehensive Sales Script...")
def generate_ai_script(script_type: str, service: str, industry: str, specific_requirements: str) -> str:
    """Generate complete call/email scripts using AI, with enhanced detail."""
    client = get_openai_client()
    if not client:
        return "OpenAI API key required"
    
    template = SCRIPT_TEMPLATES.get(script_type, {})
    service_info = SERVICES.get(service, {})
    
    prompt = f"""
    Generate a complete, ready-to-use {script_type} for ATM Agency sales representatives.
    
    SCRIPT TYPE: {script_type}
    Description: {template.get('description', 'N/A')}
    Required Structure: {', '.join(template.get('structure', []))}
    Target Duration: {template.get('duration', 'N/A')}
    
    SERVICE: {service}
    Description: {service_info.get('description', 'N/A')}
    
    TARGET INDUSTRY: {industry}
    Common Pain Points: {INDUSTRIES.get(industry, 'N/A')}
    
    SPECIFIC REQUIREMENTS: {specific_requirements or 'None'}
    
    INSTRUCTIONS:
    1. Follow the required structure exactly, using clear headings (e.g., **[SECTION NAME]**).
    2. Make it highly natural, conversational, and persuasive.
    3. Include specific ATM Agency value propositions and ROI points.
    4. Address {industry} pain points specifically and offer tailored solutions.
    5. Include transition phrases, suggested pauses (use [PAUSE]), and alternative phrases (use *Option A/B*).
    6. Include a section for **Anticipated Objections** and a brief, one-sentence response for each.
    7. The script must be significantly longer and more detailed than a basic template.
    
    Generate the complete script now:
    """

    try:
        response = client.chat.completions.create(
            model=st.session_state.ai_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPTS['script_writer']},
                {"role": "user", "content": prompt}
            ],
            temperature=st.session_state.temperature,
            max_tokens=2000 # Increased max tokens for longer output
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

# --- UI Components ---

def render_pitch_generator():
    """Renders the UI for the AI Sales Pitch Generator tab."""
    st.header("🎯 Personalized AI Sales Pitch Generator")
    st.markdown("Generate a highly customized, value-driven pitch for any service, tailored to your prospect's industry and pain points.")

    col1, col2 = st.columns(2)
    
    with col1:
        prospect_name = st.text_input("Prospect Name", placeholder="e.g., Sarah Connor")
        company_info = st.text_area("Prospect Company Info (Optional)", height=100, 
                                    placeholder="e.g., Mid-sized regional bank, 500 employees, recently merged with another bank.")
        additional_context = st.text_area("Additional Context/Goal (Optional)", height=100, 
                                          placeholder="e.g., Focus on their compliance issues. Goal is to book a follow-up demo.")
        
    with col2:
        service = st.selectbox("ATM Agency Service to Pitch", list(SERVICES.keys()))
        industry = st.selectbox("Prospect Industry", list(INDUSTRIES.keys()))
        tone = st.selectbox("Desired Pitch Tone", list(TONES.keys()))
        strategy = st.selectbox("Sales Strategy Framework", list(SALES_STRATEGIES.keys()), key='pitch_strategy')
        
        # Dynamic Pain Points based on Industry
        default_pain_points = INDUSTRIES.get(industry, "").split(', ')
        pain_points = st.multiselect(
            "Prospect's Specific Pain Points", 
            options=default_pain_points + ["High operational costs", "Low lead conversion", "Poor data quality", "Legacy systems"],
            default=default_pain_points
        )

    if st.button("Generate Pitch", use_container_width=True, type="primary"):
        if not get_openai_client():
            st.error("Please enter a valid OpenAI API key in the sidebar to generate content.")
        elif not service or not industry or not tone:
            st.error("Please select a Service, Industry, and Tone.")
        else:
            pitch = generate_ai_pitch(service, industry, tone, pain_points, company_info, prospect_name, additional_context, strategy)
            st.session_state.current_analysis = {
                "type": "pitch",
                "content": pitch,
                "service": service,
                "industry": industry,
                "tone": tone,
                "strategy": strategy
            }
            st.experimental_rerun()

    if st.session_state.current_analysis and st.session_state.current_analysis.get("type") == "pitch":
        st.subheader(f"Generated Pitch for {st.session_state.current_analysis['service']}")
        st.markdown(f"**Industry:** {st.session_state.current_analysis['industry']} | **Tone:** {st.session_state.current_analysis['tone']} | **Strategy:** {st.session_state.current_analysis['strategy']}")
        st.markdown(f"<div class='ai-pitch-box'>{st.session_state.current_analysis['content']}</div>", unsafe_allow_html=True)
        
        # Add a button to copy the pitch
        st.download_button(
            label="Download Pitch as Text",
            data=st.session_state.current_analysis['content'],
            file_name=f"pitch_{st.session_state.current_analysis['service'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )

def render_objection_handler():
    """Renders the UI for the Objection Handler tab."""
    st.header("🛡️ AI Objection Handler & Training")
    st.markdown("Get three strategic responses (Empathetic, Logic, Story) and actionable tips for any sales objection.")

    col1, col2 = st.columns(2)
    
    with col1:
        objection_category = st.selectbox("Select Common Objection Category", list(OBJECTIONS.keys()))
        
        # Allow user to select a pre-defined objection or enter a custom one
        predefined_objections = OBJECTIONS.get(objection_category, {}).get("objections", [])
        objection_text = st.selectbox("Or Select a Specific Objection", ["Custom"] + predefined_objections)
        
        if objection_text == "Custom":
            custom_objection = st.text_input("Enter Custom Objection", placeholder="e.g., We only work with vendors who have been in business for 10+ years.")
            final_objection = custom_objection
        else:
            final_objection = objection_text

    with col2:
        context = st.text_area("Context of the Conversation", height=100, 
                               placeholder="e.g., This was said after I presented the ROI for AI Automations.")
        prospect_info = st.text_area("Prospect/Company Details", height=100, 
                                     placeholder="e.g., CFO of a mid-sized manufacturing firm.")

    if st.button("Generate Objection Responses", use_container_width=True, type="primary"):
        if not get_openai_client():
            st.error("Please enter a valid OpenAI API key in the sidebar to generate content.")
        elif not final_objection:
            st.error("Please enter or select an objection.")
        else:
            response_data = generate_ai_objection_response(final_objection, context, prospect_info)
            st.session_state.current_analysis = {
                "type": "objection",
                "objection": final_objection,
                "data": response_data
            }
            st.experimental_rerun()

    if st.session_state.current_analysis and st.session_state.current_analysis.get("type") == "objection":
        data = st.session_state.current_analysis['data']
        if "error" in data:
            st.error(f"Error: {data['error']}")
        else:
            st.subheader(f"Strategic Responses for: *{st.session_state.current_analysis['objection']}*")
            
            st.markdown("---")
            st.markdown("#### 🤝 Empathetic Approach")
            st.markdown(f"<div class='response-box'>{data.get('empathetic', 'N/A')}</div>", unsafe_allow_html=True)

            st.markdown("#### 🧠 Logic-Based Approach")
            st.markdown(f"<div class='response-box'>{data.get('logic', 'N/A')}</div>", unsafe_allow_html=True)

            st.markdown("#### 📖 Story-Based Approach")
            st.markdown(f"<div class='response-box'>{data.get('story', 'N/A')}</div>", unsafe_allow_html=True)

            st.markdown("---")
            st.subheader("💡 Actionable Handling Tips")
            tips = data.get('handling_tips', [])
            if tips and isinstance(tips, list):
                for i, tip in enumerate(tips):
                    st.markdown(f"- **Tip {i+1}:** {tip}")
            else:
                st.warning("Could not parse handling tips.")

def render_script_generator():
    """Renders the UI for the Sales Script Generator tab."""
    st.header("📝 Comprehensive Sales Script Generator")
    st.markdown("Generate full, structured scripts for calls, emails, and voicemails based on proven sales frameworks.")

    col1, col2 = st.columns(2)
    
    with col1:
        script_type = st.selectbox("Select Script Type", list(SCRIPT_TEMPLATES.keys()))
        service = st.selectbox("Target ATM Agency Service", list(SERVICES.keys()))
        
    with col2:
        industry = st.selectbox("Target Prospect Industry", list(INDUSTRIES.keys()))
        specific_requirements = st.text_area("Specific Requirements (Optional)", height=100, 
                                             placeholder="e.g., Must mention the recent industry regulation change. Keep it under 5 minutes.")

    if st.button("Generate Full Script", use_container_width=True, type="primary"):
        if not get_openai_client():
            st.error("Please enter a valid OpenAI API key in the sidebar to generate content.")
        elif not script_type or not service or not industry:
            st.error("Please select a Script Type, Service, and Industry.")
        else:
            script = generate_ai_script(script_type, service, industry, specific_requirements)
            st.session_state.current_analysis = {
                "type": "script",
                "content": script,
                "script_type": script_type,
                "service": service,
                "industry": industry
            }
            st.experimental_rerun()

    if st.session_state.current_analysis and st.session_state.current_analysis.get("type") == "script":
        st.subheader(f"Generated {st.session_state.current_analysis['script_type']} Script")
        st.markdown(f"**Service:** {st.session_state.current_analysis['service']} | **Industry:** {st.session_state.current_analysis['industry']}")
        st.markdown(f"<div class='script-template'>{st.session_state.current_analysis['content']}</div>", unsafe_allow_html=True)
        
        # Add a button to copy the script
        st.download_button(
            label="Download Script as Markdown",
            data=st.session_state.current_analysis['content'],
            file_name=f"script_{st.session_state.current_analysis['script_type'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.md",
            mime="text/markdown"
        )

# --- Main Application Layout ---

def main():
    """Main function to run the Streamlit application."""
    initialize_session_state()
    
    # Page configuration (CSS is now in the main function)
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
        .ai-pitch-box {
            background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
            border-left: 4px solid #667eea;
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
            border: 1px solid #667eea40;
            white-space: pre-wrap; /* Ensures markdown formatting is respected */
        }
        .response-box {
            background-color: #f0fdf4;
            border-left: 4px solid #22c55e;
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
            white-space: pre-wrap;
        }
        .script-template {
            background-color: #fef3c7;
            border-left: 4px solid #f59e0b;
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
            white-space: pre-wrap;
        }
        .api-status {
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
            font-weight: 600;
            text-align: center;
        }
        .api-active {
            background-color: #d1fae5;
            color: #065f46;
        }
        .api-inactive {
            background-color: #fee2e2;
            color: #991b1b;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 class='main-header'>ATM Agency - AI Sales Assistant 🚀</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Your personal AI co-pilot for generating hyper-personalized pitches, handling objections, and creating full sales scripts.</p>", unsafe_allow_html=True)

    # --- Sidebar ---
    with st.sidebar:
        st.header("Configuration")
        
        # API Key Input
        st.session_state.openai_api_key = st.text_input(
            "OpenAI API Key", 
            type="password", 
            placeholder="sk-...",
            value=st.session_state.openai_api_key
        )
        
        # API Status
        if get_openai_client():
            st.markdown("<div class='api-status api-active'>✅ API Key Active</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='api-status api-inactive'>❌ API Key Required</div>", unsafe_allow_html=True)

        st.subheader("AI Model Settings")
        st.session_state.ai_model = st.selectbox("Model", AI_MODELS, index=AI_MODELS.index(st.session_state.ai_model) if st.session_state.ai_model in AI_MODELS else 0)
        st.session_state.temperature = st.slider("Creativity (Temperature)", 0.0, 1.0, st.session_state.temperature, 0.05)
        
        st.subheader("Sales Strategy")
        st.session_state.sales_strategy = st.selectbox("Default Strategy", list(SALES_STRATEGIES.keys()), key='sidebar_strategy')
        st.markdown(f"**{st.session_state.sales_strategy}:** {SALES_STRATEGIES[st.session_state.sales_strategy]['description']}")
        
        st.subheader("History")
        if st.button("Clear History & Cache", use_container_width=True):
            st.session_state.generated_scripts = []
            st.session_state.current_analysis = None
            st.cache_data.clear()
            st.success("History and cache cleared!")
            st.experimental_rerun()
            
        if st.session_state.generated_scripts:
            st.markdown("---")
            st.caption("Recent Scripts")
            for script_entry in st.session_state.generated_scripts[-5:]:
                st.markdown(f"- {script_entry['type']} for {script_entry['service']} ({script_entry['timestamp'].split(' ')[1]})")


    # --- Main Tabs ---
    tab1, tab2, tab3, tab4 = st.tabs(["Pitch Generator", "Objection Handler", "Script Generator", "Service Catalog"])

    with tab1:
        render_pitch_generator()

    with tab2:
        render_objection_handler()

    with tab3:
        render_script_generator()
        
    with tab4:
        st.header("📚 ATM Agency Service Catalog")
        st.markdown("A detailed overview of the high-impact AI solutions we offer.")
        
        for service_name, data in SERVICES.items():
            with st.expander(f"**{service_name}** - *{data['description']}*"):
                st.subheader("Key Benefits")
                st.markdown("\n".join([f"- {b}" for b in data['benefits']]))
                
                st.subheader("Primary Use Cases")
                st.markdown("\n".join([f"- {uc}" for uc in data['use_cases']]))
                
                st.subheader("Quantifiable ROI")
                st.markdown(f"**{data['roi_points']}**")


if __name__ == "__main__":
    st.set_page_config(
        page_title="ATM Agency - AI Sales Assistant",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    main()
