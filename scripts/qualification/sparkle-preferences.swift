import Foundation
import CoreFoundation

// Restore only Sparkle's preference namespace after the isolated CLI test.
// Never imports/replaces the customer's complete preference domain.
let domain = "com.conduit-technologies.macCurrent" as CFString
func values() -> [String: Any] {
    let all = CFPreferencesCopyMultiple(nil, domain, kCFPreferencesCurrentUser, kCFPreferencesAnyHost) as? [String: Any] ?? [:]
    return all.filter { $0.key.hasPrefix("SU") || $0.key.hasPrefix("SPU") }
}
let path = URL(fileURLWithPath: CommandLine.arguments[2])
if CommandLine.arguments[1] == "save" {
    let data = try PropertyListSerialization.data(fromPropertyList: values(), format: .binary, options: 0)
    try data.write(to: path, options: .atomic)
} else {
    let before = try PropertyListSerialization.propertyList(from: Data(contentsOf: path), format: nil) as! [String: Any]
    for key in Set(values().keys).union(before.keys) {
        guard key.hasPrefix("SU") || key.hasPrefix("SPU") else { fatalError("Unexpected preference namespace") }
        CFPreferencesSetValue(key as CFString, before[key] as CFPropertyList?, domain, kCFPreferencesCurrentUser, kCFPreferencesAnyHost)
    }
    guard CFPreferencesSynchronize(domain, kCFPreferencesCurrentUser, kCFPreferencesAnyHost) else { fatalError("Preference restoration failed") }
}
