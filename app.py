import streamlit as st
import requests
from github import Github
import base64
import os
from datetime import datetime
from groq import Groq

def initialize_github_client(access_token):
    """Initialize GitHub client with access token"""
    return Github(access_token)

def initialize_groq_client(groq_api_key):
    """Initialize Groq client with API key"""
    return Groq(api_key=groq_api_key)

def check_special_repository(username, g):
    """Check if the special username repository exists"""
    try:
        repo = g.get_user().get_repo(username)
        return repo
    except Exception as e:
        st.error(f"Repository {username}/{username} not found. Please create it first.")
        return None

def generate_readme_content(prompt, groq_client):
    """Generate README content using Groq's LLaMA 3 model"""
    try:
        system_prompt = """You are a professional GitHub README.md generator. 
        Create a well-structured, engaging markdown file based on the user's requirements.
        The README should be professional and showcase the user's profile effectively.
        You must only return the markdown content without any explanations, code comments, or extra text."""
        
        user_prompt = f"""Generate a GitHub profile README.md file with the following requirements:
        {prompt}
        
        Please ensure to:
        1. Use appropriate markdown formatting
        2. Include relevant emojis
        3. Create clear sections
        4. Make it visually appealing
        5. Include common GitHub profile sections like Skills, Projects, Contact
        6. Add any badges or stats if mentioned
        
        Return only the markdown code without any explanations, code comments, or additional text."""
        
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="llama3-70b-8192",
            temperature=0.7,
            max_tokens=2048,
            top_p=1,
            stream=False
        )
        
        return chat_completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating content: {str(e)}")
        return None



def update_readme(repo, content, branch="main"):
    """Update README.md in the repository"""
    try:
        # Try to get the existing file to get its SHA
        contents = repo.get_contents("README.md", ref=branch)
        repo.update_file(
            contents.path,
            f"Update README.md via Profile Generator",
            content,
            contents.sha,
            branch=branch
        )
        return True
    except Exception as e:
        try:
            # File doesn't exist, create it
            repo.create_file(
                "README.md",
                f"Create README.md via Profile Generator",
                content,
                branch=branch
            )
            return True
        except Exception as e:
            st.error(f"Error updating README: {str(e)}")
            return False

def main():
    st.title("🚀 GitHub Profile README Generator")
    st.write("Generate an awesome GitHub profile README using LLaMA 3!")

    # Initialize session state for storing markdown content
    if 'markdown_content' not in st.session_state:
        st.session_state.markdown_content = None

    # Sidebar for API keys
    with st.sidebar:
        st.header("API Configuration")
        github_token = st.text_input(
            "GitHub Personal Access Token",
            type="password",
            help="Create a token with 'repo' scope at https://github.com/settings/tokens"
        )
        groq_api_key = st.text_input(
            "Groq API Key",
            type="password",
            help="Get your API key from Groq dashboard"
        )

    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Prompt input
        readme_prompt = st.text_area(
            "Describe how you want your README to look",
            height=150,
            placeholder="""Example: I'm a full-stack developer specializing in React and Node.js. 
            Include my top skills, current projects, and GitHub stats. 
            Add a section about my open source contributions and how to reach me."""
        )

        # Advanced options
        with st.expander("Advanced Options"):
            include_stats = st.checkbox("Include GitHub Stats", value=True)
            include_languages = st.checkbox("Include Top Languages", value=True)
            include_streak = st.checkbox("Include Contribution Streak", value=True)

        # Generate Markdown button
        if st.button("🎨 Generate Markdown", key="generate"):
            if not groq_api_key:
                st.error("Please enter your Groq API key in the sidebar!")
            else:
                with st.spinner("Generating markdown..."):
                    groq_client = initialize_groq_client(groq_api_key)
                    
                    # Add selected options to the prompt
                    full_prompt = f"{readme_prompt}\n\n"
                    if include_stats:
                        full_prompt += "Include GitHub statistics visualization.\n"
                    if include_languages:
                        full_prompt += "Add a top languages card.\n"
                    if include_streak:
                        full_prompt += "Include the GitHub streak stats.\n"
                    
                    st.session_state.markdown_content = generate_readme_content(full_prompt, groq_client)

    # Display generated markdown and GitHub push option
    if st.session_state.markdown_content:
        st.subheader("📝 Generated Markdown")
        
        # Display raw markdown
        st.code(st.session_state.markdown_content, language="markdown")
        
        # Preview
        with st.expander("Preview Rendered README"):
            st.markdown(st.session_state.markdown_content)
        
        # GitHub push section
        st.subheader("📤 Push to GitHub")
        if github_token:
            try:
                g = initialize_github_client(github_token)
                user = g.get_user()
                username = user.login
                
                # Check repository
                repo = check_special_repository(username, g)
                if repo:
                    if st.button("Push to GitHub", key="push"):
                        with st.spinner("Pushing to GitHub..."):
                            if update_readme(repo, st.session_state.markdown_content):
                                st.success("🎉 README updated successfully!")
                                st.balloons()
                else:
                    st.warning(f"Please create a repository named '{username}' first!")
            except Exception as e:
                st.error(f"GitHub authentication error: {str(e)}")
        else:
            st.warning("Please enter your GitHub token in the sidebar to push changes!")

    # Instructions
    with st.expander("ℹ️ How to use this app"):
        st.markdown("""
        1. Create a GitHub repository with the same name as your username
        2. Generate a GitHub Personal Access Token with 'repo' scope
        3. Get your Groq API key from the Groq dashboard
        4. Enter both tokens in the sidebar
        5. Describe how you want your README to look
        6. Click 'Generate Markdown' to see the preview
        7. Review the generated markdown and preview
        8. Click 'Push to GitHub' to publish
        
        Note: The special repository name must match your GitHub username exactly!
        """)

if __name__ == "__main__":
    main()