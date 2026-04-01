class Conduitai < Formula
  desc "Search, install, and manage AI tools for Claude Code"
  homepage "https://conduitai.app"
  version "0.7.0"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/conduit-technologies/conduitai-cli/releases/download/v0.7.0/conduitai-darwin-arm64"
      sha256 "0019dfc4b32d63c1392aa264aed2253c1e0c2fb09216f8e2cc269bbfb8bb49b5"
    end
    on_intel do
      url "https://github.com/conduit-technologies/conduitai-cli/releases/download/v0.7.0/conduitai-darwin-x64"
      sha256 "0019dfc4b32d63c1392aa264aed2253c1e0c2fb09216f8e2cc269bbfb8bb49b5"
    end
  end

  on_linux do
    url "https://github.com/conduit-technologies/conduitai-cli/releases/download/v0.7.0/conduitai-linux-x64"
    sha256 "0019dfc4b32d63c1392aa264aed2253c1e0c2fb09216f8e2cc269bbfb8bb49b5"
  end

  def install
    bin.install Dir["conduitai-*"].first => "conduitai"
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/conduitai --version")
  end
end
