class Conduitai < Formula
  desc "Search, install, and manage AI tools for Claude Code"
  homepage "https://conduitai.app"
  version "0.9.3"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/conduit-technologies/conduitai-cli/releases/download/cli-v0.9.3/conduitai-darwin-arm64"
      sha256 "4a526fa2fd956e6b831ab9d71eb13147264848e15dd706eb04583f626e13c381"
    end
    on_intel do
      url "https://github.com/conduit-technologies/conduitai-cli/releases/download/cli-v0.9.3/conduitai-darwin-x64"
      sha256 "a9358f5d2d697012d50409b11bd2974dca5a33a9a62d673d5e44d3a1b42cc962"
    end
  end

  on_linux do
    url "https://github.com/conduit-technologies/conduitai-cli/releases/download/cli-v0.9.3/conduitai-linux-x64"
    sha256 "7291b283cd087b65c79a57007d37fcf91cde8ecda5123b403a2906a7fa0a1cb2"
  end

  def install
    bin.install Dir["conduitai-*"].first => "conduitai"
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/conduitai --version")
  end
end
