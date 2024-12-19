# 🚀 GitHub Profile README Generator

This is a web app that generates an awesome GitHub profile README using the power of Groq's LLaMA 3 model! You can customize your README with various sections, stats, and more, then directly push it to your GitHub repository.

## 📥 Installation

To run this project, follow the steps below:

1. Install the required Python packages:

    ```bash
    pip install streamlit PyGithub requests groq
    ```

2. Run the app:

    ```bash
    streamlit run app.py
    ```

## 🚀 How to Use

1. Create a GitHub repository with the same name as your GitHub username.
2. Generate a [GitHub Personal Access Token](https://github.com/settings/tokens) with the `repo` scope.
3. Get your [Groq API Key](https://www.groq.com/) from the Groq dashboard.
4. Enter both the tokens in the sidebar of the app.
5. Describe how you want your README to look by providing a prompt.
6. Click on "🎨 Generate Markdown" to see the preview of your generated README.
7. Review the markdown and preview, and click "📤 Push to GitHub" to update your README.

## 🔧 Features

- **Generate a personalized GitHub README**: Describes your skills, projects, contact info, and more.
- **Include GitHub stats**: Visualize your GitHub statistics and contributions.
- **Display your top languages**: Showcase your coding expertise in popular languages.
- **Contribution streaks**: Highlight your GitHub contribution streaks.

## 🔒 Security

Ensure your GitHub Personal Access Token and Groq API key are kept secure. They are used to authenticate your GitHub account and access Groq's model for generating the README.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

Created with ❤️ by [Your Name](https://github.com/your-username)
