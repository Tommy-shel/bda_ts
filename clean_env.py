import os
import shutil
import site

site_packages = site.getsitepackages()
for sp in site_packages:
    if os.path.exists(sp):
        for item in os.listdir(sp):
            if item.startswith("~"):
                full_path = os.path.join(sp, item)
                print(f"🧹 Cleaning corrupted package folder: {full_path}")
                try:
                    if os.path.isdir(full_path):
                        shutil.rmtree(full_path, ignore_errors=True)
                    else:
                        os.remove(full_path)
                except Exception as e:
                    print(f"Could not remove {full_path}: {e}")

print("✨ Cleanup complete!")
