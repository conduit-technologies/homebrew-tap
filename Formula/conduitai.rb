class Conduitai < Formula
  desc "Search, install, and manage AI tools for Claude Code, Cursor, and Windsurf"
  homepage "https://conduitai.app"
  url "https://registry.npmjs.org/@conduitai-app/cli/-/cli-0.6.0.tgz"
  sha256 "865bc5728575d4f4ce8551995fac47c1109efc04f4f86972f706df01567e5a25"
  license "MIT"

  depends_on "node@22"

  def install
    system "npm", "install", *std_npm_args
    bin.install_symlink libexec.glob("bin/*")
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/conduitai --version")
  end
end
