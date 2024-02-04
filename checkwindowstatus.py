import psutil
import speedtest
import platform
import socket
import subprocess
import wmi
import ctypes

def get_installed_software():
    installed_software = subprocess.check_output(['wmic', 'product', 'get', 'name']).decode('utf-8').split('\n')
    return [line.strip() for line in installed_software if line.strip()]

def get_internet_speed():
    st = speedtest.Speedtest()
    download_speed = st.download() / 1024 / 1024  # Convert to Mbps
    upload_speed = st.upload() / 1024 / 1024  # Convert to Mbps
    return download_speed, upload_speed

def get_screen_resolution():
    user32 = ctypes.windll.user32
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

def get_cpu_info():
    cpu_info = {}
    cpu_info['model'] = platform.processor()
    cpu_info['cores'] = psutil.cpu_count(logical=False)
    cpu_info['threads'] = psutil.cpu_count(logical=True)
    return cpu_info

def get_gpu_info():
    try:
        w = wmi.WMI()
        for gpu in w.Win32_VideoController():
            return gpu.Name
    except Exception as e:
        return "GPU information not available"

def get_ram_size():
  return round(psutil.virtual_memory().total / (1024.0 ** 3), 2)

def get_screen_size():
  return "Not available"  # Screen size retrieval might need additional library or hardware detection

def get_mac_addresses():
  for interface, snics in psutil.net_if_addrs().items():
      for snic in snics:
          if 'Ethernet' in interface or 'Wi-Fi' in interface:
              return snic.address

def get_public_ip():
  try:
      return socket.gethostbyname(socket.gethostname())
  except:
      return "Not available"

def get_windows_version():
  return platform.platform()

if __name__ == "__main__":
  print("1. All Installed software's list:", get_installed_software())
  download_speed, upload_speed = get_internet_speed()
  print("2. Internet Speed (Download/Upload Mbps):", download_speed, "/", upload_speed)
  print("3. Screen Resolution:", get_screen_resolution())
  print("4. CPU model and Cores/Threads:", get_cpu_info())
  print("5. GPU model:", get_gpu_info())
  print("6. RAM Size (In GB):", get_ram_size())
  print("7. Screen size:", get_screen_size())
  print("8. Wifi/Ethernet mac address:", get_mac_addresses())
  print("9. Public IP address:", get_public_ip())
  print("10. Windows version:", get_windows_version())