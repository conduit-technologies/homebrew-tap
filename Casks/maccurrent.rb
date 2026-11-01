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

  zap trash: [
    "~/Library/Application Support/macCurrent",
    "~/Library/Caches/com.conduit-technologies.macCurrent",
    "~/Library/Preferences/com.conduit-technologies.macCurrent.plist",
    "~/Library/Saved Application State/com.conduit-technologies.macCurrent.savedState",
  ]
end
