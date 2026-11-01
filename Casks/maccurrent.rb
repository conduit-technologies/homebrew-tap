cask "maccurrent" do
  version "1.2.0.68"
  sha256 "c88ea6c4874384af060602b9d249e934163b2b02208e932fed3076746166a5d3"

  url "https://downloads.maccurrent.com/releases/direct/#{version}/macCurrent-#{version}.dmg"
  name "macCurrent"
  desc "Find, install, and track supported application updates"
  homepage "https://maccurrent.com/"

  livecheck do
    url "https://downloads.maccurrent.com/releases/direct/appcast.xml"
    strategy :sparkle, &:short_version
  end

  auto_updates true
  depends_on macos: :sequoia

  app "macCurrent.app"

  preflight_steps do
    run "/bin/sh", args: ["-c", <<~SH, "--", "{{appdir}}/macCurrent.app", "{{version}}"]
      set -eu
      app="$1"
      expected="$2"
      if [ ! -e "$app" ]; then exit 0; fi
      if [ -L "$app" ]; then
        printf '%s\\n' 'The existing macCurrent app must not be a symbolic link.' >&2
        exit 1
      fi
      installed=$(/usr/libexec/PlistBuddy -c 'Print :CFBundleShortVersionString' "$app/Contents/Info.plist")
      if [ "$installed" != "$expected" ]; then
        printf '%s\\n' "The existing macCurrent copy is $installed, but this cask is $expected." >&2
        printf '%s\\n' 'Update the direct copy first, then adopt the matching release. Homebrew-owned copies use brew upgrade.' >&2
        exit 1
      fi
      exec /usr/bin/codesign --verify --deep --strict -R \\
        'anchor apple generic and identifier "com.conduit-technologies.macCurrent" and certificate leaf[subject.OU] = "D3B973F339"' "$app"
    SH
  end

  zap trash: [
    "~/Library/Application Support/macCurrent",
    "~/Library/Caches/com.conduit-technologies.macCurrent",
    "~/Library/Preferences/com.conduit-technologies.macCurrent.plist",
    "~/Library/Saved Application State/com.conduit-technologies.macCurrent.savedState",
  ]
end
