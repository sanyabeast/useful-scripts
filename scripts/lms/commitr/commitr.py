#!/usr/bin/env python3
"""
Git Commit Assistant with LMStudio Integration

A CLI tool that integrates with LMStudio (LLM API) to automatically generate 
meaningful Git commit messages and descriptions by analyzing staged files.

Usage:
    commitr [--model MODEL_NAME] [--dry-run] [--verbose]

Options:
    --model: LMStudio model name to use (default: auto-detect first available)
    --dry-run: Generate commit message without actually committing
    --verbose: Show detailed output including diffs
    --help: Show this help message
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path
from typing import List, Dict, Optional
import lmstudio as lms
from pydantic import BaseModel


class CommitSummary(BaseModel):
    """Pydantic model for structured LLM response about file changes."""
    summary: str
    impact: str
    category: str


class CommitMessage(BaseModel):
    """Pydantic model for structured LLM response for final commit message."""
    title: str
    description: str


def check_git_repository() -> bool:
    """Check if current directory is inside a valid Git repository."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode == 0
    except FileNotFoundError:
        print("❌ Error: Git is not installed or not in PATH")
        return False


def get_staged_files() -> List[str]:
    """Get list of files currently staged for commit."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True,
            text=True,
            check=True
        )
        files = [f.strip() for f in result.stdout.strip().split('\n') if f.strip()]
        return files
    except subprocess.CalledProcessError as e:
        print(f"❌ Error getting staged files: {e}")
        return []


def get_file_diff(file_path: str) -> str:
    """Get the diff content for a specific staged file."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", file_path],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Error getting diff for {file_path}: {e}")
        return ""


def get_project_name() -> str:
    """Get the project name from git remote or directory name."""
    try:
        # Try to get from git remote
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            url = result.stdout.strip()
            # Extract project name from URL
            if url:
                project_name = url.split('/')[-1].replace('.git', '')
                return project_name
    except:
        pass
    
    # Fallback to directory name
    return Path.cwd().name


def analyze_file_changes(file_path: str, diff_content: str, model, project_name: str) -> Optional[CommitSummary]:
    """Analyze changes in a single file using LLM."""
    if not diff_content.strip():
        return None
    
    try:
        chat = lms.Chat()
        
        prompt = f"""
You are a Git commit assistant analyzing code changes for the "{project_name}" project.

File: {file_path}
Git Diff:
```diff
{diff_content}
```

Analyze these changes and provide:

1. **Summary**: A concise description of what was changed in this file (1-2 sentences)
2. **Impact**: What effect these changes have (bug fix, new feature, refactor, etc.)
3. **Category**: One word category (feat, fix, refactor, docs, style, test, chore)

Focus on:
- What functionality was added, removed, or modified
- The purpose and intent of the changes
- Technical details that matter for understanding the change

Provide your response as valid JSON with this exact structure:

```json
{{
    "summary": "Brief description of changes made to this file",
    "impact": "Description of the effect/purpose of these changes", 
    "category": "feat|fix|refactor|docs|style|test|chore"
}}
```
"""
        
        chat.add_user_message(prompt)
        response = model.respond(chat, response_format=CommitSummary)
        
        # Extract the parsed response
        if hasattr(response, 'parsed'):
            return CommitSummary(**response.parsed)
        else:
            print(f"⚠️ Warning: Unexpected response format for {file_path}")
            return None
            
    except Exception as e:
        print(f"❌ Error analyzing {file_path}: {e}")
        return None


def generate_commit_message(file_summaries: List[Dict], model, project_name: str) -> Optional[CommitMessage]:
    """Generate final commit message based on all file summaries."""
    try:
        chat = lms.Chat()
        
        # Prepare summaries text
        summaries_text = "\n".join([
            f"• {summary['file']}: {summary['analysis'].summary} ({summary['analysis'].category})"
            for summary in file_summaries
        ])
        
        # Determine primary category
        categories = [s['analysis'].category for s in file_summaries]
        primary_category = max(set(categories), key=categories.count)
        
        prompt = f"""
You are a Git commit message generator for the "{project_name}" project.

File Changes Summary:
{summaries_text}

Primary Category: {primary_category}

Generate a professional Git commit message following conventional commit format:

**Requirements:**
1. **Title**: One line, max 50 characters, format: "type: brief description"
2. **Description**: Multi-line detailed explanation (if needed)

**Guidelines:**
- Use conventional commit types: feat, fix, refactor, docs, style, test, chore
- Title should be imperative mood ("add", "fix", "update", not "added", "fixed", "updated")
- Description should explain WHY the change was made, not just WHAT
- If only one file changed, focus on that specific change
- If multiple files, focus on the overall goal/feature

Provide your response as valid JSON:

```json
{{
    "title": "type: concise description under 50 chars",
    "description": "Detailed explanation of why this change was made and its impact (optional, can be empty string if title is sufficient)"
}}
```
"""
        
        chat.add_user_message(prompt)
        response = model.respond(chat, response_format=CommitMessage)
        
        # Extract the parsed response
        if hasattr(response, 'parsed'):
            return CommitMessage(**response.parsed)
        else:
            print("⚠️ Warning: Unexpected response format for commit message")
            return None
            
    except Exception as e:
        print(f"❌ Error generating commit message: {e}")
        return None


def commit_changes(title: str, description: str) -> bool:
    """Execute the git commit with the generated message."""
    try:
        commit_message = title
        if description.strip():
            commit_message = f"{title}\n\n{description}"
        
        result = subprocess.run(
            ["git", "commit", "-m", commit_message],
            capture_output=True,
            text=True,
            check=True
        )
        
        print("✅ Commit successful!")
        print(f"📝 Commit message: {title}")
        if description.strip():
            print(f"📄 Description: {description}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error committing changes: {e}")
        print(f"Git output: {e.stderr}")
        return False


def get_available_models() -> List[str]:
    """Get list of available LMStudio models."""
    try:
        # This is a placeholder - LMStudio package might have a different way to list models
        # For now, we'll rely on the user providing the model name
        return []
    except:
        return []


def main():
    parser = argparse.ArgumentParser(
        description="Git Commit Assistant with LMStudio Integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        "-m", "--model", 
        help="LMStudio model name to use for generating commit messages"
    )
    parser.add_argument(
        "--dry-run", 
        action="store_true", 
        help="Generate commit message without actually committing"
    )
    parser.add_argument(
        "-v", "--verbose", 
        action="store_true", 
        help="Show detailed output including diffs"
    )
    
    args = parser.parse_args()
    
    # Check if we're in a Git repository
    print("🔍 Checking Git repository...")
    if not check_git_repository():
        print("❌ Error: Not inside a valid Git repository")
        print("💡 Please navigate to a Git repository and try again")
        sys.exit(1)
    
    print("✅ Git repository detected")
    
    # Get staged files
    print("📋 Checking staged files...")
    staged_files = get_staged_files()
    
    if not staged_files:
        print("⚠️ No files are currently staged for commit")
        print("💡 Please stage some files first using 'git add <files>' and try again")
        sys.exit(1)
    
    print(f"✅ Found {len(staged_files)} staged file(s):")
    for file in staged_files:
        print(f"   • {file}")
    
    # Load LMStudio model
    if not args.model:
        print("❌ Error: Model name is required")
        print("💡 Please specify a model using --model MODEL_NAME")
        print("   Example: commitr --model gemma-3-4b-it-qat")
        sys.exit(1)
    
    print(f"🤖 Loading LMStudio model: {args.model}...")
    try:
        model = lms.llm(args.model)
        print("✅ Model loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        print("💡 Make sure LMStudio is running and the model name is correct")
        sys.exit(1)
    
    # Get project name
    project_name = get_project_name()
    print(f"📁 Project: {project_name}")
    
    # Analyze each staged file
    print("\n🔍 Analyzing file changes...")
    file_summaries = []
    
    for file_path in staged_files:
        print(f"   📄 Analyzing {file_path}...")
        
        # Get diff for this file
        diff_content = get_file_diff(file_path)
        
        if args.verbose:
            print(f"      Diff preview: {len(diff_content)} characters")
        
        # Analyze changes with LLM
        analysis = analyze_file_changes(file_path, diff_content, model, project_name)
        
        if analysis:
            file_summaries.append({
                'file': file_path,
                'analysis': analysis
            })
            print(f"      ✅ {analysis.category}: {analysis.summary}")
        else:
            print(f"      ⚠️ Could not analyze changes")
    
    if not file_summaries:
        print("❌ Could not analyze any file changes")
        sys.exit(1)
    
    # Generate commit message
    print("\n💭 Generating commit message...")
    commit_msg = generate_commit_message(file_summaries, model, project_name)
    
    if not commit_msg:
        print("❌ Could not generate commit message")
        sys.exit(1)
    
    # Display generated commit message
    print("\n" + "="*60)
    print("📝 GENERATED COMMIT MESSAGE")
    print("="*60)
    print(f"Title: {commit_msg.title}")
    if commit_msg.description.strip():
        print(f"\nDescription:\n{commit_msg.description}")
    print("="*60)
    
    # Ask for user confirmation (unless dry-run)
    if args.dry_run:
        print("\n🏃 Dry run mode - no commit will be made")
        return
    
    while True:
        choice = input("\n❓ Do you want to commit with this message? [y/n/e]: ").lower().strip()
        
        if choice in ['y', 'yes']:
            success = commit_changes(commit_msg.title, commit_msg.description)
            if success:
                print("🎉 All done!")
            else:
                sys.exit(1)
            break
        elif choice in ['n', 'no']:
            print("❌ Commit cancelled")
            break
        elif choice in ['e', 'edit']:
            print("✏️ Edit mode not implemented yet")
            print("💡 You can manually commit using: git commit -m \"your message\"")
            break
        else:
            print("Please enter 'y' (yes), 'n' (no), or 'e' (edit)")


if __name__ == "__main__":
    main()