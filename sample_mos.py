import os
import shutil


file_paths = {
    "unit_hifigan":"/home/yfliu/16k-hifi-gan/unit_hifigan/test_samples/",
    "hifigan":"/home/yfliu/16khifigan/mel/test_samples/",
    "divise":"/data1/yfliu/outputs/baseline/433h_8x_fixed/test_samples/",
    "revise":"/data1/yfliu/outputs/hifigandev/output433h/revise/433h_upsample/test_samples/",
    "gt": "/data1/yfliu/lrs3/test/",
    "gt_frames": "/data1/yfliu/lrs3/frames/test/",
}
# an example is FxtSMZKMdes

# Reference

# Destination directory
output_dir = "./audio"
ref_dir = file_paths["gt"]
os.makedirs(output_dir, exist_ok=True)

# Function to copy and overwrite files
def copy_and_overwrite_files(file_paths, output_dir):
    for subdir in os.listdir(ref_dir):
        sampled_test_subdir = os.path.join(ref_dir, subdir)
        if os.path.isdir(sampled_test_subdir):
            # Extract the identifier (e.g., 00002 from 6ra1MIKlYB0_00002)
            target_dir = os.path.join(ref_dir, subdir)
            identifier = os.listdir(target_dir)[0].split('.')[0]  # The first sample
            for name, path in file_paths.items():
                # Form the source file name
                source_file_no_prefix = os.path.join(path, subdir, identifier)
                postfixes = []
                if name == "gt":
                    postfixes.append(".flac")
                    postfixes.append(".mp4")
                    postfixes.append(".txt")
                elif name == "gt_frames":
                    postfixes.append(".jpg")
                else:
                    postfixes.append("_vc.mp3")
                    postfixes.append("_vc.mp4")
                for postfix in postfixes:
                    source_file_name = source_file_no_prefix+f"{postfix}"
                    if postfix == ".flac":
                        postfix = ".mp3"
                    target_file_no_prefix = os.path.join(output_dir, subdir)+"_"+identifier
                    target_file_name = os.path.join(target_file_no_prefix, f"{name}{postfix}")
                    os.makedirs(target_file_no_prefix, exist_ok=True)
                    # Copy and overwrite the file
                    shutil.copy2(source_file_name, target_file_name)
                    print(f"Copied {source_file_name} to {target_file_name}")

# Call the function
copy_and_overwrite_files(file_paths, output_dir)