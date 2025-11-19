# config.py

# --- SERVICES Configuration ---
SERVICES = {
    "Custom AI Apps": {
        "description": "Bespoke AI-powered applications tailored to your business needs, from complex workflow automation to proprietary machine learning models.",
        "benefits": [
            "Automate complex workflows and reduce manual tasks by 70% or more.",
            "Scale operations rapidly without increasing headcount.",
            "Gain a significant competitive advantage with proprietary AI solutions.",
            "Integrate seamlessly with all existing enterprise systems and data sources."
        ],
        "use_cases": [
            "Advanced document processing and intelligent data extraction (OCR/NLP).",
            "Predictive analytics, demand forecasting, and risk modeling.",
            "Intelligent customer support systems and virtual agents.",
            "Custom workflow automation and decision-making engines."
        ],
        "roi_points": "Typical ROI of 300-500% within the first year through efficiency gains and new revenue streams."
    },
    "PMS/CRM Systems": {
        "description": "AI-enhanced Project Management and Customer Relationship Management platforms, providing deep insights and automation across the sales and project lifecycle.",
        "benefits": [
            "Centralize all client data, project information, and communication history.",
            "AI-powered lead scoring, opportunity prediction, and churn risk analysis.",
            "Automated follow-ups, task management, and pipeline progression.",
            "Real-time analytics, performance tracking, and custom reporting dashboards."
        ],
        "use_cases": [
            "Sales pipeline management with predictive AI insights.",
            "Project tracking, resource allocation, and budget forecasting.",
            "Customer lifecycle management and personalized engagement.",
            "Automated reporting and compliance documentation."
        ],
        "roi_points": "Increase sales conversion rates by 35% and reduce administrative time by 60%."
    },
    "AI Marketplace": {
        "description": "Custom marketplace platforms powered by AI for intelligent matching, dynamic pricing, and personalized recommendations for buyers and sellers.",
        "benefits": [
            "AI-driven product/service recommendations, increasing average order value.",
            "Intelligent search and discovery, improving user experience.",
            "Automated vendor/buyer matching and dispute resolution.",
            "Dynamic pricing optimization based on real-time market conditions."
        ],
        "use_cases": [
            "B2B service and talent marketplaces.",
            "E-commerce product recommendation engines.",
            "Talent and freelancer platforms with skill matching.",
            "Equipment and resource sharing platforms."
        ],
        "roi_points": "Increase transaction volume by 45% and platform stickiness by 25% through better matching and recommendations."
    },
    "AI Voice Agents": {
        "description": "24/7 intelligent, human-like voice assistants for customer service, sales, and lead qualification, handling unlimited call volume.",
        "benefits": [
            "Handle unlimited calls simultaneously, eliminating hold times.",
            "Natural, conversational interactions in multiple languages.",
            "Qualify leads, book appointments, and process simple transactions automatically.",
            "Reduce call center operational costs by up to 80%."
        ],
        "use_cases": [
            "Inbound customer support, FAQ handling, and ticket creation.",
            "Outbound sales calls, lead qualification, and survey execution.",
            "Appointment scheduling, reminders, and rescheduling.",
            "Order taking, status updates, and basic technical support."
        ],
        "roi_points": "Save $50,000+ annually per customer service representative replaced or augmented."
    },
    "Website & Funnels": {
        "description": "High-converting websites and sales funnels built with modern frameworks and optimized using AI for maximum performance.",
        "benefits": [
            "AI-powered personalization for a unique experience for each visitor.",
            "Real-time A/B testing and continuous optimization.",
            "Intelligent chatbots and forms for superior lead capture.",
            "Conversion rate optimization (CRO) through Machine Learning models."
        ],
        "use_cases": [
            "High-volume lead generation landing pages.",
            "E-commerce product funnels and checkout optimization.",
            "SaaS onboarding flows and feature adoption campaigns.",
            "Event registration and webinar funnels."
        ],
        "roi_points": "Average 2-3x increase in conversion rates within 90 days of launch."
    },
    "AI Automations": {
        "description": "End-to-end business process automation using AI, connecting disparate systems and eliminating repetitive, error-prone manual tasks.",
        "benefits": [
            "Eliminate repetitive manual tasks across departments.",
            "Connect all your tools and platforms into a unified workflow.",
            "Intelligent decision-making embedded directly into workflows.",
            "Scale operations and increase throughput without hiring."
        ],
        "use_cases": [
            "Automated data entry, document processing, and invoice handling.",
            "Intelligent email and communication automation (e.g., triage, response drafting).",
            "Social media management, content scheduling, and engagement tracking.",
            "Automated report generation and distribution."
        ],
        "roi_points": "Save 20-30 hours per employee per week on manual, non-strategic tasks."
    }
}

# --- OBJECTIONS Configuration ---
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

# --- INDUSTRIES Configuration ---
INDUSTRIES = {
    "Real Estate": "long sales cycles, lead qualification, property management overhead, manual document processing",
    "Healthcare": "administrative burden, appointment scheduling, patient communication, complex billing and compliance",
    "Professional Services": "client onboarding, proposal generation, time tracking, resource utilization inefficiencies",
    "E-commerce": "customer support volume, order management, inventory tracking, personalized product recommendations",
    "SaaS": "lead qualification, customer onboarding, churn prevention, feature adoption tracking",
    "Manufacturing": "supply chain coordination, quality control, order processing, predictive maintenance",
    "Financial Services": "compliance documentation, client reporting, data analysis, fraud detection",
    "Education": "student communication, enrollment management, administrative tasks, personalized learning paths",
    "Retail": "inventory management, customer engagement, multi-channel coordination, demand forecasting",
    "Hospitality": "booking management, guest communication, staff coordination, dynamic pricing"
}

# --- TONES Configuration ---
TONES = {
    "Professional": "formal, business-focused, data-driven, emphasizing measurable results and reliability.",
    "Consultative": "advisory, problem-solving, strategic, positioning the rep as a trusted expert.",
    "Enthusiastic": "energetic, exciting, opportunity-focused, highlighting future potential and innovation.",
    "Direct": "straight-forward, no-nonsense, results-oriented, focusing on speed and efficiency.",
    "Empathetic": "understanding, relationship-focused, supportive, prioritizing the client's feelings and needs."
}

# --- SCRIPT TEMPLATES Configuration ---
SCRIPT_TEMPLATES = {
    "Cold Call Opening": {
        "description": "Initial cold call script designed to capture attention and secure a brief follow-up meeting.",
        "structure": ["Hook (Problem/Opportunity)", "Introduction (Who You Are)", "Value Proposition (Specific Benefit)", "Permission to Continue (Micro-Commitment)"],
        "duration": "30-45 seconds"
    },
    "Discovery Call": {
        "description": "A structured script for a deep-dive conversation to uncover the prospect's needs and qualify the opportunity (SPIN Selling framework).",
        "structure": ["Rapport Building", "Situation Questions", "Problem Questions", "Implication Questions", "Need-Payoff Questions", "Next Steps"],
        "duration": "20-30 minutes"
    },
    "Demo Script": {
        "description": "A product demonstration script focused on storytelling and connecting features directly to the prospect's pain points.",
        "structure": ["Context Setting & Agenda", "Problem Acknowledgment & Re-Validation", "Solution Walkthrough (Feature-Benefit-Impact)", "Benefits Highlight & ROI Summary", "Next Steps & Q&A"],
        "duration": "15-20 minutes"
    },
    "Closing Call": {
        "description": "The final pitch and commitment request, designed to address last-minute concerns and secure the deal.",
        "structure": ["Summary of Value & Agreement", "Address Final Concerns (The 'Ask')", "Present Offer & Terms", "Ask for Commitment (The Close)", "Handle Final Objections & Logistics"],
        "duration": "10-15 minutes"
    },
    "Follow-Up Email": {
        "description": "A compelling email template to send after an initial meeting or call, providing value and a clear call-to-action.",
        "structure": ["Subject Line (Personalized)", "Opening (Reference Past Conversation)", "Value Add (Resource/Insight)", "Call to Action (Specific Next Step)", "Signature"],
        "duration": "N/A"
    },
    "Voicemail Script": {
        "description": "A concise, value-driven voicemail designed to pique interest and maximize the chance of a callback.",
        "structure": ["Name & Company", "Reason for Call (Relevant Pain Point)", "Value Teaser (Specific Benefit)", "Call to Action (Simple Request)", "Contact Info"],
        "duration": "20-30 seconds"
    },
    "Value Proposition Script": {
        "description": "A detailed, long-form script focused on a specific value argument (e.g., Build vs. Buy), ideal for email sequences, landing page copy, or in-depth sales calls.",
        "structure": ["Core Argument/Hook", "Lifetime Ownership = Lifetime Savings", "Full Flexibility + Custom Features", "Your Brand, Your Identity", "No More Limits", "AI Powered — But 100% Your Data", "Custom Automations", "Instant ROI and Long-Term Asset Value", "System Grows as You Grow", "Final Call to Action"],
        "duration": "5-10 minutes (for presentation)"
    }
}

# --- NEW: SALES STRATEGY TEMPLATES ---
SALES_STRATEGIES = {
    "Value-Based Selling": {
        "description": "Focuses on the economic value and ROI the solution provides, rather than features or price.",
        "principles": [
            "Quantify the cost of the status quo.",
            "Align solution benefits with prospect's strategic business goals.",
            "Use case studies and data to prove potential ROI."
        ]
    },
    "Challenger Sale": {
        "description": "Challenges the prospect's assumptions about their business and teaches them a new way to think about their problem.",
        "principles": [
            "Teach: Offer unique, valuable insights.",
            "Tailor: Customize the message to the prospect's specific role.",
            "Take Control: Guide the conversation and next steps."
        ]
    },
    "Solution Selling": {
        "description": "Focuses on diagnosing the prospect's problem and crafting a tailored solution, often involving multiple products/services.",
        "principles": [
            "Ask open-ended questions to uncover deep needs.",
            "Focus on the 'why' behind the problem.",
            "Present a comprehensive solution roadmap."
        ]
    }
}

# --- NEW: AI MODEL CONFIGURATION ---
AI_MODELS = [
    "gpt-4o-mini",
    "gpt-4o",
    "gpt-3.5-turbo"
]

# --- NEW: SYSTEM PROMPTS ---
SYSTEM_PROMPTS = {
    "pitch_generator": "You are an expert sales consultant for ATM Agency, an AI technology marketing agency. Generate a highly personalized and compelling sales pitch. Your tone must be professional, persuasive, and focused on quantifiable business outcomes.",
    "objection_handler": "You are a master sales trainer who excels at handling objections. You provide strategic, empathetic, and effective responses, formatted as a JSON object.",
    "script_writer": "You are an expert sales script writer who creates natural, effective scripts for B2B technology sales. Your scripts feel conversational, not robotic, and are ready for immediate use by a sales representative."
}
