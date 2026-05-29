#!/usr/bin/env python3
"""
Quick test script to validate config module and output integration.
Run this from the project root: python test_config_integration.py
"""

def test_config_defaults():
    """Test that config module loads defaults correctly"""
    from labware.config import config, DEFAULT_CONFIG

    print("[TEST] Config defaults...")
    assert "symbols" in DEFAULT_CONFIG
    assert "styles" in DEFAULT_CONFIG
    assert "logging" in DEFAULT_CONFIG
    assert "log_formats" in DEFAULT_CONFIG

    # Test getting values
    info_symbol = config.get("symbols", "info")
    assert info_symbol == "[✚]", f"Expected '[✚]' but got {info_symbol}"

    info_style = config.get("styles", "info")
    assert info_style == "dodger_blue1", f"Expected 'dodger_blue1' but got {info_style}"

    print("  ✓ Defaults loaded correctly")
    print(f"  ✓ info symbol: {info_symbol}")
    print(f"  ✓ info style: {info_style}")

def test_config_types():
    """Test type-safe getters"""
    from labware.config import config

    print("\n[TEST] Config type getters...")

    # Test getint
    log_level = config.getint("logging", "level")
    assert isinstance(log_level, int), f"Expected int but got {type(log_level)}"
    assert log_level == 20, f"Expected 20 but got {log_level}"
    print(f"  ✓ getint works: logging.level = {log_level}")

    # Test getbool with fallback
    bool_val = config.getbool("logging", "nonexistent", fallback=True)
    assert isinstance(bool_val, bool), f"Expected bool but got {type(bool_val)}"
    assert bool_val is True, f"Expected True but got {bool_val}"
    print(f"  ✓ getbool with fallback works: {bool_val}")

def test_output_module_import():
    """Test that output module can import and use config"""
    print("\n[TEST] Output module integration...")

    try:
        from labware.output import console, _theme
        print("  ✓ output module imports successfully")
        print(f"  ✓ console object: {type(console)}")
        print(f"  ✓ theme object: {type(_theme)}")
    except Exception as e:
        print(f"  ✗ FAILED to import output: {e}")
        raise

def test_config_singleton():
    """Test that config is a singleton"""
    print("\n[TEST] Config singleton pattern...")

    from labware.config import config, get_config

    instance1 = get_config()
    instance2 = get_config()

    assert instance1 is instance2, "get_config() should return same instance"
    assert instance1 is config, "module config should be the singleton"
    print("  ✓ Singleton pattern works correctly")

def test_fallback_defaults():
    """Test fallback mechanism works"""
    print("\n[TEST] Fallback defaults...")

    from labware.config import config

    # Request non-existent option with fallback
    result = config.get("nonexistent", "option", fallback="my_fallback")
    assert result == "my_fallback", f"Expected 'my_fallback' but got {result}"
    print("  ✓ Fallback mechanism works")

    # Request non-existent with no fallback (should return empty string)
    result = config.get("nonexistent", "option")
    assert result == "", f"Expected empty string but got {result}"
    print("  ✓ Empty fallback works")

if __name__ == "__main__":
    print("=" * 60)
    print("Config Module Integration Tests")
    print("=" * 60)

    try:
        test_config_defaults()
        test_config_types()
        test_output_module_import()
        test_config_singleton()
        test_fallback_defaults()

        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED")
        print("=" * 60)
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        exit(1)
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

