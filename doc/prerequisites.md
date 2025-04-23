# How to Install Git, Python, and Set Up Conda

## Installing Git
### Windows
1. Download the Git installer from the official website:
   - [https://git-scm.com/download/win](https://git-scm.com/download/win)
2. Run the installer and follow the setup instructions:
   - Choose the default editor for Git (e.g., Vim, Notepad++, or VS Code).
   - Select how Git should handle line endings (recommended: Checkout Windows-style, commit Unix-style).
   - Choose the default terminal emulator (recommended: Use MinTTY for better compatibility).
3. Complete the installation and open **Git Bash** or **Command Prompt** to verify:
   ```sh
   git --version
   ```

### macOS
1. Install Git via Homebrew (recommended):
   ```sh
   brew install git
   ```
2. Alternatively, install it from the official Git website:
   - [https://git-scm.com/download/mac](https://git-scm.com/download/mac)
3. Verify the installation:
   ```sh
   git --version
   ```

### Linux (Debian/Ubuntu)
1. Update package lists:
   ```sh
   sudo apt update
   ```
2. Install Git:
   ```sh
   sudo apt install git -y
   ```
3. Verify the installation:
   ```sh
   git --version
   ```

### Linux (Fedora/RHEL)
1. Install Git using DNF:
   ```sh
   sudo dnf install git -y
   ```
2. Verify the installation:
   ```sh
   git --version
   ```

## Initial Git Configuration
After installation, set up your Git user information:
```sh
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```
To check your Git configuration:
```sh
git config --list
```

## Linking Git to Your GitHub Account
1. Generate an SSH key (if you haven't already):
   ```sh
   ssh-keygen -t ed25519 -C "your.email@example.com"
   ```
   - Press Enter to save the key in the default location.
   - Set a passphrase (optional but recommended).

2. Add the SSH key to the SSH agent:
   ```sh
   eval "$(ssh-agent -s)"
   ssh-add ~/.ssh/id_ed25519
   ```

3. Copy the public key to your clipboard:
   ```sh
   cat ~/.ssh/id_ed25519.pub
   ```

4. Add the SSH key to GitHub:
   - Go to **GitHub → Settings → SSH and GPG keys**.
   - Click **New SSH Key**.
   - Paste the copied key and save it.

5. Test the connection:
   ```sh
   ssh -T git@github.com
   ```
   - If successful, you'll see a message like: `Hi username! You've successfully authenticated.`

6. Set Git to use SSH for GitHub:
   ```sh
   git remote set-url origin git@github.com:username/repository.git
   ```

Now Git is ready to use with GitHub!

## Installing Python
Before installing Conda, ensure that Python is installed on your system.

### Windows
1. Download the latest Python installer from the official website:
   - [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)
2. Run the installer and check the box **Add Python to PATH**.
3. Click **Install Now** and follow the installation prompts.
4. Verify the installation by opening **Command Prompt** and running:
   ```sh
   python --version
   ```

### macOS
1. Install Python via Homebrew (recommended):
   ```sh
   brew install python
   ```
2. Verify the installation:
   ```sh
   python3 --version
   ```

### Linux (Debian/Ubuntu)
1. Update package lists:
   ```sh
   sudo apt update
   ```
2. Install Python:
   ```sh
   sudo apt install python3 python3-pip -y
   ```
3. Verify the installation:
   ```sh
   python3 --version
   ```

### Linux (Fedora/RHEL)
1. Install Python using DNF:
   ```sh
   sudo dnf install python3 python3-pip -y
   ```
2. Verify the installation:
   ```sh
   python3 --version
   ```

## Installing and Setting Up Conda
### Installing Miniconda (Recommended)
Miniconda is a minimal distribution of Conda that includes only the necessary packages.

1. Download Miniconda:
   - [Windows](https://docs.conda.io/en/latest/miniconda.html)
   - [macOS/Linux](https://docs.conda.io/en/latest/miniconda.html)

2. Follow the installation instructions for your OS.
   - Windows: Run the `.exe` installer and follow the prompts.
   - macOS/Linux: Run the `.sh` installer in the terminal.

3. Verify the installation:
   ```sh
   conda --version
   ```

### Creating and Activating a Conda Environment
To create and activate a Conda environment for your project, run:
```sh
conda create --name iq-index-tracking python=3.9 numpy requests
conda activate iq-index-tracking
```

### Verifying the Environment
To check that the environment is correctly set up:
```sh
conda info --envs
```

### Deactivating and Removing the Environment
To deactivate the environment:
```sh
conda deactivate
```
To remove the environment completely:
```sh
conda remove --name iq-index-tracking --all
```

Now you have Git, Python, and Conda properly set up!
