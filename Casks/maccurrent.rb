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

  preflight do
    existing = appdir/"macCurrent.app"
    next unless existing.exist?

    raise "The existing macCurrent app must not be a symbolic link" if existing.symlink?

    installed_version = system_command("/usr/libexec/PlistBuddy",
                                       args: ["-c", "Print :CFBundleShortVersionString", existing/"Contents/Info.plist"]).stdout.strip
    unless installed_version == version.to_s
      raise "The existing macCurrent copy is #{installed_version}, but this cask is #{version}. " \
            "Update the direct copy first, then adopt the matching release. Homebrew-owned copies use brew upgrade."
    end

    system_command "/usr/bin/codesign",
                   args: ["--verify", "--deep", "--strict", "-R",
                          'anchor apple generic and identifier "com.conduit-technologies.macCurrent" ' \
                          'and certificate leaf[subject.OU] = "D3B973F339"', existing]
  end

  zap trash: [
    "~/Library/Application Support/macCurrent",
    "~/Library/Caches/com.conduit-technologies.macCurrent",
    "~/Library/Preferences/com.conduit-technologies.macCurrent.plist",
    "~/Library/Saved Application State/com.conduit-technologies.macCurrent.savedState",
  ]
end
