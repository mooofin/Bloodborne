import os
import struct
import argparse

class BloodborneResolutionPatcher:
    def __init__(self, eboot_path):
        self.eboot_path = eboot_path
        self.resolutions = {
            "480p": (720, 480),
            "720p": (1280, 720),
            "1080p": (1920, 1080),
            "1440p": (2560, 1440),
            "4K": (3840, 2160)
        }
        
    def patch_resolution(self, target_res):
        if target_res not in self.resolutions:
            raise ValueError("Unsupported resolution")
            
        width, height = self.resolutions[target_res]
        
        try:
            backup_path = self.eboot_path + ".backup"
            if not os.path.exists(backup_path):
                with open(self.eboot_path, "rb") as src, open(backup_path, "wb") as dst:
                    dst.write(src.read())
            
            with open(self.eboot_path, "r+b") as f:
                f.seek(0x400000)
                f.write(struct.pack("<I", width))
                
                f.seek(0x400004)
                f.write(struct.pack("<I", height))
                
            print(f"Successfully patched resolution to {width}x{height}")
            
        except Exception as e:
            print(f"Error patching file: {str(e)}")
            if os.path.exists(backup_path):
                os.replace(backup_path, self.eboot_path)
            raise

def main():
    parser = argparse.ArgumentParser(description="Bloodborne Resolution Patcher for ShadPS4")
    parser.add_argument("eboot_path", help="Path to EBOOT.BIN file")
    parser.add_argument("resolution", choices=["480p", "720p", "1080p", "1440p", "4K"],
                      help="Target resolution")
    
    args = parser.parse_args()
    
    patcher = BloodborneResolutionPatcher(args.eboot_path)
    patcher.patch_resolution(args.resolution)

if __name__ == "__main__":
    main()
