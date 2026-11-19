import streamlit as st
from few_shot import FewShotPosts
from post_generator import (
    generate_post,
    generate_idea_post,
    generate_certificate_post,
    generate_hiring_post
)

# Page configuration
st.set_page_config(
    page_title="LinkedIn Post Crafter AI",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for polished, modern LinkedIn aesthetic
st.markdown("""
<style>
    /* Global styles */
    .main {
        background-color: #f8fafc;
    }
    
    /* Header styling */
    .app-header {
        background: linear-gradient(135deg, #0A66C2 0%, #004182 100%);
        color: white;
        padding: 24px 28px;
        border-radius: 12px;
        margin-bottom: 24px;
        box-shadow: 0 4px 14px rgba(10, 102, 194, 0.2);
    }
    .app-header h1 {
        color: white !important;
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .app-header p {
        color: #e0e7ff;
        margin: 8px 0 0 0;
        font-size: 1rem;
    }

    /* LinkedIn Card Simulator */
    .linkedin-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 22px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        margin-top: 15px;
        margin-bottom: 15px;
    }
    .card-header {
        display: flex;
        align-items: center;
        margin-bottom: 14px;
    }
    .avatar {
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, #0A66C2 0%, #0077b5 100%);
        color: white;
        font-weight: bold;
        font-size: 1.1rem;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 12px;
    }
    .author-info h4 {
        margin: 0;
        font-size: 1.05rem;
        color: #1e293b;
    }
    .author-info p {
        margin: 0;
        font-size: 0.82rem;
        color: #64748b;
    }
    .post-content {
        color: #1e293b;
        font-size: 0.98rem;
        line-height: 1.6;
        white-space: pre-wrap;
        word-wrap: break-word;
        padding: 10px 0;
    }
    .social-bar {
        border-top: 1px solid #f1f5f9;
        padding-top: 12px;
        margin-top: 12px;
        display: flex;
        gap: 20px;
        color: #64748b;
        font-size: 0.88rem;
    }
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        background: #e0f2fe;
        color: #0369a1;
        margin-right: 6px;
        margin-bottom: 6px;
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if "generated_post" not in st.session_state:
    st.session_state.generated_post = ""
if "post_meta" not in st.session_state:
    st.session_state.post_meta = {"type": "Welcome", "tag": "General"}
if "post_history" not in st.session_state:
    st.session_state.post_history = []

# Initialize FewShot instance
@st.cache_resource
def load_few_shot_data():
    return FewShotPosts()

fs = load_few_shot_data()

# Shared constants
length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish"]
tone_options = [
    "Engaging & Thought-Provoking",
    "Storytelling & Personal",
    "Actionable & Educational",
    "Direct & Concise",
    "Inspirational & Motivational"
]

# Sidebar Analytics & Insights
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png", width=42)
    st.title("Post Studio")
    st.caption("AI-powered LinkedIn Content Generator")
    
    st.markdown("---")
    st.subheader("🎯 Generator Modes")
    st.markdown("""
    - **💡 Raw Idea**: Turn rough thoughts into viral stories.
    - **🎓 Certificate**: Celebrate milestones with humility.
    - **📢 Hiring Post**: Attract top talent with clear JDs.
    - **📊 Influencer Style**: Topic-based few-shot posts.
    """)
    
    st.markdown("---")
    st.subheader("📊 Dataset Knowledge")
    col_sb1, col_sb2 = st.columns(2)
    with col_sb1:
        st.metric(label="Total Posts", value=len(fs.df) if fs.df is not None else 0)
    with col_sb2:
        st.metric(label="Topics", value=len(fs.get_tags()))

    if st.session_state.post_history:
        st.markdown("---")
        st.subheader("🕒 Session History")
        for idx, item in enumerate(reversed(st.session_state.post_history[-6:])):
            btn_label = f"📄 {item.get('title', 'Post')} ({item.get('mode', 'General')})"
            if st.button(btn_label, key=f"hist_{idx}"):
                st.session_state.generated_post = item['content']
                st.session_state.post_meta = {"type": item.get('mode', 'Post'), "tag": item.get('title', 'Saved')}
                st.rerun()

# App Header
st.markdown("""
<div class="app-header">
    <h1>💼 LinkedIn Post Generator AI</h1>
    <p>Generate high-performing, authentic LinkedIn posts for Ideas, Certifications, Job Openings, or Influencer topics.</p>
</div>
""", unsafe_allow_html=True)

# Main Studio Layout
col_controls, col_preview = st.columns([1.15, 1.35], gap="large")

with col_controls:
    st.subheader("⚙️ Select Generator Mode")
    
    tab_idea, tab_cert, tab_hiring, tab_topic = st.tabs([
        "💡 Raw Idea to Post",
        "🎓 Certificate / Milestone",
        "📢 HR / Job Opening",
        "📊 Influencer (Few-Shot)"
    ])
    
    # ------------------ TAB 1: RAW IDEA ------------------
    with tab_idea:
        st.caption("Turn your rough notes, real-life experience, or random thoughts into an engaging LinkedIn post.")
        raw_idea_input = st.text_area(
            "What's on your mind? (Your raw idea / story)",
            placeholder="e.g. Yesterday I interviewed a fresher. His communication wasn't fluent, but his problem-solving attitude was phenomenal. I hired him on the spot. Skills can be taught, attitude cannot.",
            height=130
        )
        col_i1, col_i2 = st.columns(2)
        with col_i1:
            idea_length = st.selectbox("Length", options=length_options, index=1, key="idea_len")
        with col_i2:
            idea_lang = st.selectbox("Language", options=language_options, key="idea_lang")
            
        idea_tone = st.selectbox("Tone & Vibe", options=tone_options, index=1, key="idea_tone")
        
        if st.button("✨ Transform Idea into Post", type="primary", key="btn_idea", use_container_width=True):
            if not raw_idea_input.strip():
                st.warning("Please type your idea or thought first!")
            else:
                with st.spinner("🤖 Crafting story with hook, structure, and takeaway..."):
                    try:
                        post = generate_idea_post(
                            raw_idea=raw_idea_input,
                            length=idea_length,
                            language=idea_lang,
                            tone=idea_tone
                        )
                        st.session_state.generated_post = post
                        st.session_state.post_meta = {"type": "Raw Idea", "tag": "Thought Leadership"}
                        st.session_state.post_history.append({
                            "title": raw_idea_input[:25] + "...",
                            "mode": "Idea",
                            "content": post
                        })
                        st.success("Post created successfully!")
                    except Exception as e:
                        st.error(f"Error: {e}")

    # ------------------ TAB 2: CERTIFICATE ------------------
    with tab_cert:
        st.caption("Share your new certification, degree, or achievement in an inspiring, non-boastful way.")
        cert_name = st.text_input("🎓 Certification / Course Name", placeholder="e.g. AWS Certified Solutions Architect - Associate")
        issuer_org = st.text_input("🏢 Issued By / Platform", placeholder="e.g. Amazon Web Services (AWS) / Coursera / Udemy")
        key_learnings = st.text_area(
            "🧠 What were your 2-3 biggest learnings?",
            placeholder="e.g. High-availability cloud architectures, cost optimization, and VPC peering.",
            height=90
        )
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            cert_length = st.selectbox("Length", options=length_options, index=1, key="cert_len")
        with col_c2:
            cert_lang = st.selectbox("Language", options=language_options, key="cert_lang")
            
        if st.button("🎓 Generate Certificate Post", type="primary", key="btn_cert", use_container_width=True):
            if not cert_name.strip():
                st.warning("Please provide the certificate or course name!")
            else:
                with st.spinner("🤖 Writing humble, inspiring achievement post..."):
                    try:
                        post = generate_certificate_post(
                            cert_name=cert_name,
                            issuer=issuer_org,
                            key_learnings=key_learnings,
                            length=cert_length,
                            language=cert_lang
                        )
                        st.session_state.generated_post = post
                        st.session_state.post_meta = {"type": "Certificate", "tag": cert_name}
                        st.session_state.post_history.append({
                            "title": cert_name,
                            "mode": "Certificate",
                            "content": post
                        })
                        st.success("Certificate post generated!")
                    except Exception as e:
                        st.error(f"Error: {e}")

    # ------------------ TAB 3: HIRING / JOB OPENING ------------------
    with tab_hiring:
        st.caption("Create an eye-catching, structured hiring announcement to attract top applicants.")
        col_h1, col_h2 = st.columns(2)
        with col_h1:
            job_title = st.text_input("💼 Role / Job Title", placeholder="e.g. Senior Python / GenAI Engineer")
        with col_h2:
            company_name = st.text_input("🏢 Company Name (Optional)", placeholder="e.g. TechCorp Solutions")
            
        col_h3, col_h4 = st.columns(2)
        with col_h3:
            experience = st.text_input("⏳ Experience Required", placeholder="e.g. 2-4 Years / Freshers welcome")
        with col_h4:
            work_mode = st.text_input("📍 Location / Work Mode", placeholder="e.g. Remote / Hybrid (Pune)")
            
        key_skills = st.text_area("🛠️ Key Skills / Requirements", placeholder="e.g. Python, FastAPI, Docker, LangChain, Groq API", height=70)
        col_h5, col_h6 = st.columns(2)
        with col_h5:
            apply_method = st.text_input("📩 How to Apply", placeholder="e.g. Email resume to jobs@company.com or DM")
        with col_h6:
            hiring_lang = st.selectbox("Language", options=language_options, key="hiring_lang")
            
        perks = st.text_input("🎁 Perks & Culture (Optional)", placeholder="e.g. Flexible hours, ESOPs, learning stipend")
        
        if st.button("📢 Generate Hiring Post", type="primary", key="btn_hiring", use_container_width=True):
            if not job_title.strip() or not apply_method.strip():
                st.warning("Please fill at least the Job Title and How to Apply method!")
            else:
                with st.spinner("🤖 Formatting structured, high-conversion job post..."):
                    try:
                        post = generate_hiring_post(
                            job_title=job_title,
                            company_name=company_name,
                            experience=experience,
                            location=work_mode,
                            skills=key_skills,
                            apply_method=apply_method,
                            perks=perks,
                            language=hiring_lang
                        )
                        st.session_state.generated_post = post
                        st.session_state.post_meta = {"type": "Job Alert", "tag": job_title}
                        st.session_state.post_history.append({
                            "title": job_title,
                            "mode": "Hiring",
                            "content": post
                        })
                        st.success("Hiring post created!")
                    except Exception as e:
                        st.error(f"Error: {e}")

    # ------------------ TAB 4: INFLUENCER TOPIC (FEW SHOT) ------------------
    with tab_topic:
        st.caption("Conditioned on past posts from influencer dataset using Few-Shot RAG learning.")
        tags = fs.get_tags()
        selected_tag = st.selectbox("📌 Select Topic", options=tags, key="topic_tag")
        
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            selected_length = st.selectbox("📏 Length", options=length_options, index=1, key="topic_len")
        with col_t2:
            selected_language = st.selectbox("🌐 Language", options=language_options, key="topic_lang")
            
        selected_tone = st.selectbox("🎭 Tone", options=tone_options, index=0, key="topic_tone")
        custom_instructions = st.text_area(
            "✍️ Specific Angle / Highlight (Optional)",
            placeholder="e.g. Focus on habits for college students...",
            height=70,
            key="topic_custom"
        )
        
        if st.button("✨ Generate Topic Post", type="primary", key="btn_topic", use_container_width=True):
            with st.spinner("🤖 Analyzing dataset & writing few-shot post..."):
                try:
                    post = generate_post(
                        length=selected_length,
                        language=selected_language,
                        tag=selected_tag,
                        custom_instructions=custom_instructions,
                        tone=selected_tone
                    )
                    st.session_state.generated_post = post
                    st.session_state.post_meta = {"type": "Influencer Topic", "tag": selected_tag}
                    st.session_state.post_history.append({
                        "title": selected_tag,
                        "mode": "Topic",
                        "content": post
                    })
                    st.success("Topic post created!")
                except Exception as e:
                    st.error(f"Error: {e}")

        # Expandable Few-Shot Examples Inspector
        with st.expander("🔍 View Matching Writing Samples from Dataset"):
            examples = fs.get_filtered_posts(selected_length, selected_language, selected_tag)
            if examples:
                st.info(f"Found {len(examples)} historical posts matching this combination:")
                for i, ex in enumerate(examples[:2]):
                    st.markdown(f"**Sample {i+1}:**")
                    st.caption(ex['text'])
            else:
                st.caption("No exact match in past dataset for this combination. LLM will generalize from topic context.")


# ------------------ RIGHT COLUMN: PREVIEW & POST TOOLS ------------------
with col_preview:
    st.subheader("👁️ Live LinkedIn Post Preview")
    
    if st.session_state.generated_post:
        current_post = st.session_state.generated_post
        meta_info = st.session_state.post_meta
        
        # Calculate post metrics
        words = len(current_post.split())
        chars = len(current_post)
        reading_time = max(1, round(words / 3.5)) # approx seconds
        
        # Badges
        st.markdown(f"""
        <div>
            <span class="badge">📂 {meta_info.get('type', 'Post')}</span>
            <span class="badge">🏷️ {meta_info.get('tag', 'General')}</span>
            <span class="badge">📝 {words} words</span>
            <span class="badge">🔤 {chars} characters</span>
            <span class="badge">⏱️ ~{reading_time}s read</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Simulated LinkedIn Card
        st.markdown(f"""
        <div class="linkedin-card">
            <div class="card-header">
                <div class="avatar">U</div>
                <div class="author-info">
                    <h4>Your Name <span style="color:#0A66C2; font-size:0.85rem;">• 1st</span></h4>
                    <p>Professional | Creator | Building with AI</p>
                    <p>Just now • 🌐</p>
                </div>
            </div>
            <div class="post-content">{current_post}</div>
            <div class="social-bar">
                <span>👍 Like (248)</span>
                <span>💬 Comment (34)</span>
                <span>🔁 Repost (19)</span>
                <span>📤 Send</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Post Tools (Copy & Edit)
        st.markdown("### 🛠️ Post Actions")
        tab_copy, tab_edit = st.tabs(["📋 Quick Copy", "✏️ Edit & Polish"])
        
        with tab_copy:
            st.caption("Click the copy icon in the upper-right corner of the code block:")
            st.code(current_post, language="text")
            
        with tab_edit:
            edited_text = st.text_area(
                "Fine-tune and edit your post directly:",
                value=current_post,
                height=220,
                key="editor_area"
            )
            if st.button("💾 Update Preview with Changes", use_container_width=True):
                st.session_state.generated_post = edited_text
                st.rerun()

    else:
        st.info("👈 Select a mode on the left and click **Generate** to see your live simulated LinkedIn post here!")
        st.markdown("""
        <div class="linkedin-card" style="opacity: 0.65; text-align: center; padding: 45px 20px;">
            <p style="font-size: 1.15rem; color: #64748b; margin: 0;">Your generated LinkedIn post preview will appear here.</p>
            <p style="font-size: 0.85rem; color: #94a3b8; margin-top: 8px;">Supports Raw Thoughts, Certifications, Job Postings, and Influencer topics.</p>
        </div>
        """, unsafe_allow_html=True)
