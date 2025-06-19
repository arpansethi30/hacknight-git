#!/usr/bin/env python3
import sys
sys.path.append('.')

try:
    import friendli
    print("✅ Basic import works")
    print(f"Friendli path: {friendli.__path__}")
    
    # Try to explore what's available
    import pkgutil
    print("\n📦 Available modules:")
    for importer, modname, ispkg in pkgutil.iter_modules(friendli.__path__):
        print(f"  {modname} (package: {ispkg})")
    
except Exception as e:
    print(f"❌ Import error: {e}")

# Try different import patterns
try:
    from friendli import AsyncFriendli, SyncFriendli
    print("✅ AsyncFriendli and SyncFriendli imported successfully")
except ImportError as e:
    print(f"❌ AsyncFriendli import failed: {e}")

try:
    from friendli.client import AsyncClient
    print("✅ AsyncClient imported successfully")
except ImportError as e:
    print(f"❌ AsyncClient import failed: {e}")

try:
    import friendli.chat
    print("✅ friendli.chat imported successfully")
except ImportError as e:
    print(f"❌ friendli.chat import failed: {e}")

# Check what's actually in the main friendli module
print(f"\n🔍 Dir of friendli module: {dir(friendli)}") 