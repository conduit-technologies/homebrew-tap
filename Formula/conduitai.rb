class Conduitai < Formula
  desc "Search, install, and manage AI tools for Claude Code"
  homepage "https://conduitai.app"
  version "0.9.2"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/conduit-technologies/conduitai-cli/releases/download/cli-v0.9.2/conduitai-darwin-arm64"
      sha256 "ac42d48146f0b89a3dc580c3e7ecbbc5acbfb052a285f5c65635d1f8fbbe6835"
    end
    on_intel do
      url "https://github.com/conduit-technologies/conduitai-cli/releases/download/cli-v0.9.2/conduitai-darwin-x64"
      sha256 "d002423f6e580463293884fb12ae7bdc8fd7e1f274f1bf9c8e02cb416c2cbb89"
    end
  end

  on_linux do
    url "https://github.com/conduit-technologies/conduitai-cli/releases/download/cli-v0.9.2/conduitai-linux-x64"
    sha256 "4e65382c97cd932731299648ef9a0aedd65d6285983d7691930b4c61515464b4"
  end

  def install
    bin.install Dir["conduitai-*"].first => "conduitai"
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/conduitai --version")
  end
end
