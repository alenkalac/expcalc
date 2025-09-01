import mss, cv2, numpy as np, time, os
import pyautogui
import pygetwindow as gw

def get_window_bbox(window_name):
    windows = gw.getWindowsWithTitle(window_name)
    if not windows:
        raise Exception(f"Window '{window_name}' not found!")

    win = windows[0]  # take first match
    if not win.isActive:
        win.activate()
        time.sleep(0.2)

    # Bounding box
    left, top = win.left, win.top
    width, height = win.width, win.height
    return {"top": top, "left": left, "width": width, "height": height}

def capture_frames(output_dir="frames", num_frames=200, interval=0.3):
    os.makedirs(output_dir, exist_ok=True)

    monitor = get_window_bbox("Maplestory Worlds-Artale(Global)")

    with mss.mss() as sct:
        for i in range(num_frames):
            frame = np.array(sct.grab(monitor))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            cv2.imwrite(f"{output_dir}/frame_{i:04d}.png", frame)
            print(f"Captured frame {i}")
            time.sleep(interval)


def stitch_images(img1, img2):
    orb = cv2.ORB_create(4000)
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)[:50]

    src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1,1,2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1,1,2)

    H, _ = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0)

    h, w = img1.shape[:2]
    result = cv2.warpPerspective(img2, H, (w*2, h))
    result[0:h, 0:w] = img1
    return result

def build_map(frames_dir="frames", output_file="map.png"):
    files = sorted([f for f in os.listdir(frames_dir) if f.endswith(".png")])
    base = cv2.imread(os.path.join(frames_dir, files[0]))
    panorama = base

    for f in files[1:]:
        img = cv2.imread(os.path.join(frames_dir, f))
        panorama = stitch_images(panorama, img)
        print(f"Stitched {f}")

    cv2.imwrite(output_file, panorama)
    print(f"Saved stitched map: {output_file}")


def extract_anchors(map_file="map.png", output_dir="anchors", num=5, size=60):
    os.makedirs(output_dir, exist_ok=True)
    img = cv2.imread(map_file)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    corners = cv2.goodFeaturesToTrack(gray, num, 0.01, 200)
    corners = np.intp(corners)

    for i, c in enumerate(corners):
        x, y = c.ravel()
        patch = img[y-size:y+size, x-size:x+size]
        if patch.size > 0:
            cv2.imwrite(f"{output_dir}/anchor_{i}.png", patch)
            cv2.rectangle(img, (x-size,y-size), (x+size,y+size), (0,0,255), 2)

    cv2.imwrite("map_with_anchors.png", img)
    print(f"Extracted {len(corners)} anchors into {output_dir}/")


# Step 1: Capture frames
#capture_frames(num_frames=300, interval=0.25)

# Step 2: Build panorama
#build_map(frames_dir="frames", output_file="map.png")

# Step 3: Extract anchors
#extract_anchors(map_file="map.png", num=8, size=50)

if __name__ == "__main__":
    #capture_frames(num_frames=300, interval=0.25)
    build_map(frames_dir="frames", output_file="map.png")