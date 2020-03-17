# This is installation script for Mobile Test Helper (MTH).

class Mth < Formula
    homepage "http://TEST.COM"
    url "https://github.com/maxim-filkov/mobile-test-helper.git"
    version "1.0.0"

    depends_on 'bash'
    depends_on 'python'
    depends_on 'ffmpeg'
    depends_on 'tiff2png'
    # depends_on cask: 'android-sdk'
    # depends_on 'bash-completion'
    depends_on 'ideviceinstaller'
    depends_on 'libimobiledevice'

    def install
        inreplace 'mth' do |t|
            t.gsub! /\$\{UTILS_SHARE_PREFIX\}/, share/""
        end
        bin.install 'mth'
        (share/"mth/action").install Dir["action/*"]
        (share/"mth/framework").install Dir["framework/*"]
        (share/"mth/framework").install Dir["install/requirements.txt"]
    end

    def post_install
        # Mth.install_android_sdk_platform_tools
        Mth.install_py_packages
        # Mth.activate_python_argcomplete
        # Mth.set_colorized_logs_format
        # Mth.enable_bash_completion
        # Mth.enable_updated_bash
        # `source ~/.bash_profile`
        # `reset`
        Mth.show_colorized("MTH has been installed successfully! Use the command 'mth' to start", "green")
    end

    def self.set_android_home
        sdk_ver = `ls /usr/local/Cellar/android-sdk/ | head -1`
        bash_profile = `cat ~/.bash_profile 2>&1`
        unless bash_profile.include? "ANDROID_HOME="
            `echo "\nexport ANDROID_HOME=/usr/local/Cellar/android-sdk/#{sdk_ver.strip}/\n" >> ~/.bash_profile`
        end
    end

    def self.install_android_sdk_platform_tools
        Mth.show_colorized("Installing Android SDK platform-tools...", "green")
        `echo "y" | android update sdk --no-ui --filter 'platform-tools'`
    end

    def self.activate_python_argcomplete
        `/usr/local/bin/activate-global-python-argcomplete --dest=/usr/local/etc/bash_completion.d`
    end

    def self.install_py_packages()
        Mth.show_colorized("Installing Python packages", "green")
        `pip install -r "/usr/local/share/mth/framework/requirements.txt"`
        if $?.exitstatus != 0
            exit(1)
        end
    end

    def self.enable_bash_completion
        bash_profile = `cat ~/.bash_profile 2>&1`
        unless bash_profile.include? "/etc/bash_completion"
            open(File.expand_path("~/.bash_profile"), "a") { |f|
                f.puts "\nif [ -f `brew --prefix`/etc/bash_completion ]; then\n\t. `brew --prefix`/etc/bash_completion\nfi\n"
            }
            `source ~/.bash_profile`
        end
    end

    def self.set_colorized_logs_format
        bash_profile = `cat ~/.bash_profile 2>&1`
        unless bash_profile.include? "COLOREDLOGS_LOG_FORMAT"
            `echo "\nexport COLOREDLOGS_LOG_FORMAT='%(message)s'\n" >> ~/.bash_profile`
        end
    end

    def self.enable_updated_bash
        etc_shells = `cat /etc/shells 2>&1`
        unless etc_shells.include? "/usr/local/bin/bash"
            `bash -c 'echo /usr/local/bin/bash >> /etc/shells'`
        end
        `chsh -s '/usr/local/bin/bash'`
    end

    def self.show_colorized(msg, color)
        if color == "red"
            puts "\e[\033[31m#{msg}\e[0m"
        end
        if color == "green"
            puts "\e[\033[32m#{msg}\e[0m"
        end
    end

end
