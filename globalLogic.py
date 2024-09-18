try:
    from pytransform import pyarmor_runtime
    pyarmor_runtime()
except ImportError:
    print("pytransform module is not installed. Please install it using pip: pip install pytransform")
