import os
import shutil


file_paths = {
    "unit_hifigan":"/home/yfliu/16k-hifi-gan/unit_hifigan/test_samples/",
    "hifigan":"/home/yfliu/16khifigan/mel/test_samples/",
    "divise":"/data1/yfliu/outputs/baseline/433h_8x_fixed/test_samples/",
    "revise":"/data1/yfliu/outputs/hifigandev/output433h/revise/433h_upsample/test_samples/",
    "gt": "/data1/yfliu/lrs3/test/"
}
# an example is FxtSMZKMdes

# Reference

# Destination directory
output_dir = "./audio"
ref_dir = './audio_feb'
os.makedirs(output_dir, exist_ok=True)

# Function to copy and overwrite files
def copy_and_overwrite_files(file_paths, output_dir):
    for subdir in os.listdir(ref_dir):
        path_old_feb = os.path.join(ref_dir, subdir)
        if os.path.isdir(path_old_feb):
            # Extract the identifier (e.g., 00002 from 6ra1MIKlYB0_00002)
            target_file_no_prefix = os.path.join(output_dir, subdir)
            subdir, identifier = subdir.split('_')
            for name, path in file_paths.items():
                # Form the source file name
                source_file_no_prefix = os.path.join(path, subdir, identifier)
                postfixes = []
                if name != "gt":
                    postfixes.append("_vc.mp3")
                    postfixes.append("_vc.mp4")
                    if name == "divise":
                        postfixes.append("_gf.mp3")
                        postfixes.append("_gf.mp4")
                else:
                    postfixes.append(".flac")
                    postfixes.append(".mp4")
                    postfixes.append(".txt")
                    postfixes.append(".png")
                for postfix in postfixes:
                    source_file_name = source_file_no_prefix+f"{postfix}"
                    if postfix == ".flac":
                        postfix = ".mp3"
                    target_file_name = os.path.join(target_file_no_prefix, f"{name}{postfix}")
                    os.makedirs(target_file_no_prefix, exist_ok=True)
                    # Copy and overwrite the file
                    shutil.copy2(source_file_name, target_file_name)
                    print(f"Copied {source_file_name} to {target_file_name}")

# Call the function
copy_and_overwrite_files(file_paths, output_dir)