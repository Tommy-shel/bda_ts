import os
import urllib.request
import ctypes

def setup_winutils():
    if os.name != 'nt':
        return

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    hadoop_dir = os.path.join(BASE_DIR, "hadoop_bin")
    bin_dir = os.path.join(hadoop_dir, "bin")
    os.makedirs(bin_dir, exist_ok=True)

    files = {
        "winutils.exe": "https://raw.githubusercontent.com/cdarlint/winutils/master/hadoop-3.2.0/bin/winutils.exe",
        "hadoop.dll": "https://raw.githubusercontent.com/cdarlint/winutils/master/hadoop-3.2.0/bin/hadoop.dll"
    }

    for file_name, url in files.items():
        file_path = os.path.join(bin_dir, file_name)
        if not os.path.exists(file_path) or os.path.getsize(file_path) < 1000:
            print(f"⬇️ Downloading official Windows Hadoop utility ({file_name})...")
            try:
                urllib.request.urlretrieve(url, file_path)
                print(f"✅ Downloaded {file_name} successfully!")
            except Exception as e:
                print(f"⚠️ Could not download {file_name}: {e}")

    os.environ['HADOOP_HOME'] = hadoop_dir
    os.environ['PATH'] = bin_dir + os.pathsep + os.environ.get('PATH', '')
    
    # Try loading hadoop.dll into C-runtime
    try:
        hadoop_dll_path = os.path.join(bin_dir, "hadoop.dll")
        if os.path.exists(hadoop_dll_path):
            ctypes.cdll.LoadLibrary(hadoop_dll_path)
    except Exception as e:
        pass

if __name__ == "__main__":
    setup_winutils()
