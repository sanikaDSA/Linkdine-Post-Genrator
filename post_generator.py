from llm_helper import llm
from few_shot import FewShotPosts

few_shot = FewShotPosts()


def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    if length == "Medium":
        return "6 to 10 lines"
    if length == "Long":
        return "11 to 15 lines"
    return "6 to 10 lines"


def generate_post(length, language, tag, custom_instructions="", tone=""):
    prompt = get_prompt(length, language, tag, custom_instructions, tone)
    response = llm.invoke(prompt)
    return response.content


def get_prompt(length, language, tag, custom_instructions="", tone=""):
    length_str = get_length_str(length)

    prompt = f'''
    Generate a LinkedIn post using the below information. No preamble.

    1) Topic: {tag}
    2) Length: {length_str}
    3) Language: {language}
    If Language is Hinglish then it means it is a mix of Hindi and English. 
    The script for the generated post should always be English.
    '''
    if tone and tone.strip():
        prompt += f"\n    4) Desired Tone: {tone.strip()}"
    if custom_instructions and custom_instructions.strip():
        prompt += f"\n    5) Specific Points / Context to Include: {custom_instructions.strip()}"

    examples = few_shot.get_filtered_posts(length, language, tag)

    if len(examples) > 0:
        prompt += "4) Use the writing style as per the following examples."

    for i, post in enumerate(examples):
        post_text = post['text']
        prompt += f'\n\n Example {i+1}: \n\n {post_text}'

        if i == 1: # Use max two samples
            break

    return prompt


def generate_idea_post(raw_idea, length="Medium", language="English", tone="Storytelling & Engaging"):
    length_str = get_length_str(length)
    prompt = f"""
    You are an expert LinkedIn copywriter.
    Transform the user's raw idea/experience/thought into a high-engagement LinkedIn post.
    
    User's Raw Thought/Idea:
    \"\"\"{raw_idea}\"\"\"
    
    Guidelines:
    1) Length: {length_str}
    2) Language: {language} (If Hinglish, use a natural blend of Hindi and English written strictly in English Latin script).
    3) Tone: {tone}
    4) Hook: Start with a strong first line that creates curiosity or stops the scroll.
    5) Formatting: Use short, readable paragraphs (1-2 sentences each) with clean white space.
    6) Value & Takeaway: Highlight a clear learning, insight, or moral.
    7) Call to Action (CTA): Conclude with an open-ended question to spark discussion in the comments.
    8) Add 3-5 relevant hashtags at the bottom.
    9) Return ONLY the post text without any introductory or concluding meta-commentary (no preamble).
    """
    response = llm.invoke(prompt)
    return response.content


def generate_certificate_post(cert_name, issuer, key_learnings="", length="Medium", language="English"):
    length_str = get_length_str(length)
    prompt = f"""
    You are an expert LinkedIn content creator.
    Generate a humble, inspiring, and authentic LinkedIn post celebrating a newly achieved certification/milestone.
    
    Details:
    - Certification/Course: {cert_name}
    - Issuing Organization/Platform: {issuer}
    - Key Learnings/Highlights: {key_learnings if key_learnings else 'Upgraded skills and completed hands-on projects'}
    - Target Length: {length_str}
    - Language: {language} (If Hinglish, conversational mix in Latin script)
    
    Best practices for a Certificate post:
    1) Avoid being boastful or cliché (avoid starting with "I am thrilled to announce" or "Proud moment").
    2) Start with the journey, challenge, or reason for pursuing this certification.
    3) Summarize 2-3 practical takeaways or skills learned.
    4) Thank mentors, the platform, or the community genuinely.
    5) Look forward to applying these skills in practical projects.
    6) Add 3-5 relevant hashtags (e.g. #{cert_name.replace(' ', '') if cert_name else 'SkillUp'}, #ContinuousLearning, #CareerGrowth).
    7) Return ONLY the post text, no preamble.
    """
    response = llm.invoke(prompt)
    return response.content


def generate_hiring_post(job_title, company_name, experience, location, skills, apply_method, perks="", language="English"):
    prompt = f"""
    You are an expert Talent Acquisition specialist and LinkedIn recruiter.
    Create a compelling, professional, and visually clear LinkedIn hiring post to attract top talent.
    
    Job Details:
    - Role / Title: {job_title}
    - Company: {company_name if company_name else 'Our growing team'}
    - Experience Required: {experience}
    - Location / Work Mode: {location} (e.g. Remote, Hybrid, On-site)
    - Key Skills / Requirements: {skills}
    - Perks / Highlights: {perks if perks else 'Competitive compensation, supportive team culture, learning opportunities'}
    - How to Apply: {apply_method}
    - Language: {language}
    
    Guidelines:
    1) Eye-catching opening: Announce the opportunity clearly with excitement (e.g., "We're Hiring!", "Join our team!").
    2) Role snapshot: Brief explanation of what the candidate will be doing or building.
    3) Bullet points for "What we are looking for" (Key skills).
    4) Bullet points for "What we offer" (Perks, culture, flexibility).
    5) Clear, unmistakable call to action: "How to Apply" (email, link, or DM).
    6) Encourage network to share / repost ("Tag someone looking for this role").
    7) Professional emojis for readability.
    8) Include 3-5 relevant hashtags (e.g., #Hiring, #{job_title.replace(' ', '') if job_title else 'Jobs'}, #JobOpportunity, #Career).
    9) Return ONLY the post text, no preamble.
    """
    response = llm.invoke(prompt)
    return response.content


if __name__ == "__main__":
    print(generate_post("Medium", "English", "Mental Health"))
