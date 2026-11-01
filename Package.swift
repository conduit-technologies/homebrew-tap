// swift-tools-version: 6.0
import PackageDescription

// Give CodeQL's Swift autobuilder a build entry point for the standalone
// qualification helper. This does not add a dependency to the Homebrew cask.
let package = Package(
    name: "macCurrentDistributionQualification",
    platforms: [.macOS(.v15)],
    products: [
        .executable(name: "sparkle-preferences", targets: ["SparklePreferences"]),
    ],
    targets: [
        .executableTarget(
            name: "SparklePreferences",
            path: "scripts/qualification",
            exclude: ["qualify-distribution.py"],
            sources: ["sparkle-preferences.swift"]
        ),
    ],
    swiftLanguageModes: [.v5]
)
