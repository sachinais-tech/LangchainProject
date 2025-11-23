import streamlit as st
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun
import wikipedia

# Page configuration
st.set_page_config(
    page_title="YouTube Script Creator",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #FF0000;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF0000;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #CC0000;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'script_generated' not in st.session_state:
    st.session_state.script_generated = False
if 'generated_script' not in st.session_state:
    st.session_state.generated_script = ""

# Header
st.markdown('<p class="main-header">🎬 YouTube Script Creator</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Create engaging YouTube scripts with AI powered by Ollama</p>', unsafe_allow_html=True)

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Ollama model selection
    ollama_model = st.selectbox(
        "Select Ollama Model",
        [ "llama3", "llama2", "mistral", "codellama", "phi", "neural-chat"],
        help="Make sure the selected model is installed in Ollama"
    )
    
    # Script parameters
    st.subheader("Script Parameters")
    video_length = st.selectbox(
        "Video Length",
        ["5 minutes", "10 minutes", "15 minutes", "20 minutes", "30 minutes"],
        index=1
    )
    
    script_style = st.selectbox(
        "Script Style",
        ["Casual and Conversational", "Professional and Educational", "Entertaining and Humorous", 
         "Inspirational and Motivational", "Technical and Detailed"]
    )
    
    include_hook = st.checkbox("Include Hook/Introduction", value=True)
    include_outro = st.checkbox("Include Call-to-Action/Outro", value=True)
    include_timestamps = st.checkbox("Include Timestamps", value=False)
    
    # Research options
    st.subheader("🔍 Research Options")
    enable_google_search = st.checkbox("Enable Google Search", value=False, help="Search Google for current information about the topic")
    enable_wikipedia = st.checkbox("Enable Wikipedia Search", value=False, help="Search Wikipedia for detailed information about the topic")

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📝 Video Details")
    
    video_topic = st.text_input(
        "Video Topic/Title *",
        placeholder="e.g., How to Learn Python in 30 Days",
        help="Enter the main topic or title of your YouTube video"
    )
    
    target_audience = st.text_input(
        "Target Audience",
        placeholder="e.g., Beginners interested in programming",
        help="Who is your target audience?"
    )
    
    key_points = st.text_area(
        "Key Points to Cover",
        placeholder="Enter key points separated by commas or new lines:\n- Point 1\n- Point 2\n- Point 3",
        height=150,
        help="List the main points you want to cover in the video"
    )
    
    additional_notes = st.text_area(
        "Additional Notes/Requirements",
        placeholder="Any specific requirements or notes...",
        height=100
    )

with col2:
    st.header("🎯 Script Options")
    
    tone = st.selectbox(
        "Tone",
        ["Friendly", "Professional", "Energetic", "Calm", "Humorous", "Serious"]
    )
    
    language = st.selectbox(
        "Language",
        ["English", "Spanish", "French", "German", "Hindi"]
    )
    
    st.info("💡 **Tip:** Be specific with your topic and key points for better script quality!")

# Generate button
st.markdown("---")
generate_button = st.button("🚀 Generate YouTube Script", type="primary", use_container_width=True)

# Initialize Ollama LLM
@st.cache_resource
def load_ollama_model(model_name):
    try:
        llm = Ollama(model=model_name, base_url="http://127.0.0.1:11500", temperature=0.7)
        return llm
    except Exception as e:
        st.error(f"Error loading Ollama model: {str(e)}")
        st.info("Make sure Ollama is running. You can start it by running: `ollama serve`")
        return None

# Search functions
def search_google(query, max_results=3):
    """Search Google using DuckDuckGo"""
    try:
        search = DuckDuckGoSearchRun()
        # Try invoke first (newer API), fallback to run
        try:
            results = search.invoke(f"{query}")
        except:
            results = search.run(f"{query}")
        return results[:1500] if results else ""  # Limit to 1500 chars
    except Exception as e:
        st.warning(f"Google search error: {str(e)}")
        return ""

def search_wikipedia(query, max_results=2):
    """Search Wikipedia for information"""
    try:
        wikipedia.set_lang("en")
        search_results = wikipedia.search(query, results=max_results)
        wiki_info = ""
        
        for title in search_results:
            try:
                page = wikipedia.page(title, auto_suggest=False)
                wiki_info += f"\n\n**{page.title}:**\n{page.summary[:500]}\n"
            except wikipedia.exceptions.DisambiguationError as e:
                # If disambiguation, try the first option
                try:
                    page = wikipedia.page(e.options[0], auto_suggest=False)
                    wiki_info += f"\n\n**{page.title}:**\n{page.summary[:500]}\n"
                except:
                    continue
            except:
                continue
        
        return wiki_info
    except Exception as e:
        st.warning(f"Wikipedia search error: {str(e)}")
        return ""

def gather_research_info(topic, key_points, enable_google, enable_wiki):
    """Gather research information from Google and Wikipedia"""
    research_info = ""
    
    if enable_google or enable_wiki:
        search_query = f"{topic}"
        if key_points:
            search_query += f" {key_points[:100]}"
    
    if enable_google:
        with st.spinner("🔍 Searching Google..."):
            google_results = search_google(search_query)
            if google_results:
                research_info += f"\n\n=== GOOGLE SEARCH RESULTS ===\n{google_results}\n"
    
    if enable_wiki:
        with st.spinner("📚 Searching Wikipedia..."):
            wiki_results = search_wikipedia(topic)
            if wiki_results:
                research_info += f"\n\n=== WIKIPEDIA INFORMATION ===\n{wiki_results}\n"
    
    return research_info

# Generate script function
def generate_script(topic, audience, key_points, notes, length, style, tone, language, hook, outro, timestamps, enable_google=False, enable_wiki=False):
    # Gather research information if enabled
    research_info = ""
    if enable_google or enable_wiki:
        research_info = gather_research_info(topic, key_points, enable_google, enable_wiki)
    
    # Build the prompt
    research_section = f"""
    
RESEARCH INFORMATION (Use this to enhance accuracy and add current facts):
{research_info if research_info else "No research information available. Use your knowledge to create the script."}
""" if research_info else ""
    
    prompt_text = f"""Create a comprehensive YouTube script for a video with the following details:

Topic/Title: {topic}
Target Audience: {audience if audience else 'General audience'}
Video Length: {length}
Style: {style}
Tone: {tone}
Language: {language}

Key Points to Cover:
{key_points if key_points else 'Cover the topic comprehensively'}

Additional Notes:
{notes if notes else 'None'}
{research_section}
Requirements:
- {"Include an engaging hook/introduction at the beginning" if hook else ""}
- Create well-structured content with clear sections
- {"Include timestamps for major sections" if timestamps else ""}
- {"Include a call-to-action and outro at the end" if outro else ""}
- Make it engaging and suitable for YouTube
- Use natural, conversational language
- Include transitions between sections
- Make it approximately {length} in duration
- {"Use the research information provided above to ensure accuracy and include current facts" if research_info else ""}

Please create a complete YouTube script with:
1. {"[HOOK/INTRODUCTION]" if hook else ""}
2. Main content sections
3. {"[TIMESTAMPS]" if timestamps else ""}
4. {"[CALL-TO-ACTION/OUTRO]" if outro else ""}

Format the script clearly with speaker notes and natural dialogue."""

    prompt = PromptTemplate(
        input_variables=[],
        template=prompt_text
    )
    
    try:
        llm = load_ollama_model(ollama_model)
        if llm is None:
            return None
        
        # Use LangChain Expression Language (LCEL) - modern approach
        chain = prompt | llm
        
        with st.spinner("🤖 Generating your YouTube script... This may take a moment."):
            response = chain.invoke({})
        
        # Extract text from response if it's an AIMessage object
        if hasattr(response, 'content'):
            return response.content
        return str(response)
    except Exception as e:
        st.error(f"Error generating script: {str(e)}")
        return None

# Generate script when button is clicked
if generate_button:
    if not video_topic:
        st.error("⚠️ Please enter a video topic/title to generate the script.")
    else:
        script = generate_script(
            video_topic,
            target_audience,
            key_points,
            additional_notes,
            video_length,
            script_style,
            tone,
            language,
            include_hook,
            include_outro,
            include_timestamps,
            enable_google_search,
            enable_wikipedia
        )
        
        if script:
            st.session_state.generated_script = script
            st.session_state.script_generated = True
            st.success("✅ Script generated successfully!")

# Display generated script
if st.session_state.script_generated and st.session_state.generated_script:
    st.markdown("---")
    st.header("📄 Generated YouTube Script")
    
    # Script display with copy button
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("📋 Copy Script"):
            st.write("Script copied! (Use Ctrl+C to copy from the text area below)")
    
    script_text = st.text_area(
        "Your Script",
        value=st.session_state.generated_script,
        height=500,
        label_visibility="collapsed"
    )
    
    # Download button
    st.download_button(
        label="💾 Download Script as TXT",
        data=st.session_state.generated_script,
        file_name=f"youtube_script_{video_topic.replace(' ', '_')[:30]}.txt",
        mime="text/plain"
    )

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 1rem;'>"
    "Powered by Sachin and Youtube Script Generator @copyright2025  🚀"
    "</div>",
    unsafe_allow_html=True
)

