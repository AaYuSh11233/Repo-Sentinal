import subprocess
import tempfile
import os
import logging

logger = logging.getLogger(__name__)

def run_checks(clone_url, branch):
    results = []
    
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            logger.info(f"Running checks for {clone_url} branch {branch}")
            
            # Change to temp directory
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            
            try:
                # Clone repository
                logger.info("Cloning repository...")
                subprocess.run(
                    ["git", "clone", "-b", branch, clone_url, "."], 
                    check=True, 
                    capture_output=True,
                    text=True
                )
                
                # Check if package.json exists (Node.js project)
                if os.path.exists("package.json"):
                    # Install dependencies
                    logger.info("Installing npm dependencies...")
                    install_result = subprocess.run(
                        ["npm", "install"], 
                        capture_output=True, 
                        text=True,
                        timeout=300  # 5 minute timeout
                    )
                    
                    if install_result.returncode != 0:
                        results.append(f"⚠️ **npm install failed:**\n```\n{install_result.stderr}\n```")
                        return results
                    
                    # Run ESLint
                    logger.info("Running ESLint...")
                    lint = subprocess.run(
                        ["npx", "eslint", "."], 
                        capture_output=True, 
                        text=True,
                        timeout=120  # 2 minute timeout
                    )
                    
                    if lint.returncode != 0:
                        results.append(f"⚠️ **Lint errors:**\n```\n{lint.stdout}\n```")
                    else:
                        results.append("✅ No lint errors.")

                    # Run npm audit
                    logger.info("Running npm audit...")
                    audit = subprocess.run(
                        ["npm", "audit", "--json"], 
                        capture_output=True, 
                        text=True,
                        timeout=120  # 2 minute timeout
                    )
                    
                    if audit.returncode != 0 or '"vulnerabilities"' in audit.stdout:
                        results.append("🔒 **Security risks detected.** Run `npm audit fix`.")
                    else:
                        results.append("✅ No known security vulnerabilities.")
                else:
                    # For non-Node.js projects, provide basic checks
                    results.append("ℹ️ **Non-Node.js project detected.** Basic checks completed.")
                    
                    # Check for common files
                    if os.path.exists("requirements.txt"):
                        results.append("✅ Python project detected (requirements.txt found)")
                    elif os.path.exists("pom.xml"):
                        results.append("✅ Java project detected (pom.xml found)")
                    elif os.path.exists("Gemfile"):
                        results.append("✅ Ruby project detected (Gemfile found)")
                    elif os.path.exists("go.mod"):
                        results.append("✅ Go project detected (go.mod found)")
                    else:
                        results.append("ℹ️ Project type not specifically identified")
                    
            finally:
                # Always return to original directory
                os.chdir(original_dir)
                
    except subprocess.TimeoutExpired:
        logger.error("Check operation timed out")
        results.append("⏰ **Operation timed out.** Please try again later.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Subprocess error: {str(e)}")
        results.append(f"❌ **Error running checks:** {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in checks: {str(e)}")
        results.append(f"❌ **Unexpected error:** {str(e)}")
    
    return results
