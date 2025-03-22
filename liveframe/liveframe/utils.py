import cv2
import numpy as np

def modify_frame(frame):
    # Load the reference image
    overlay_frame=""
    reference_image = cv2.imread('static/pic1.jpeg', cv2.IMREAD_GRAYSCALE)
    if reference_image is None:
        print("Reference image not found.")
        return

    # Initialize ORB detector
    orb = cv2.ORB_create()

    # Detect keypoints and compute descriptors for the reference image
    kp_ref, des_ref = orb.detectAndCompute(reference_image, None)

    # Start the live camera feed
    # camera = cv2.VideoCapture(camera_url)
    video_capture = cv2.VideoCapture('static/vid1.mp4')

    # if not camera.isOpened() or not video_capture.isOpened():
    #     print("Error: Cannot open video feed or camera.")
    #     return

    

    # Convert frame to grayscale for feature detection
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect keypoints and compute descriptors in the live frame
    kp_frame, des_frame = orb.detectAndCompute(gray_frame, None)

    # If descriptors are detected, proceed to feature matching
    if des_frame is not None and des_ref is not None:
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des_ref, des_frame)

        # Sort matches by distance and use the best 20 matches
        matches = sorted(matches, key=lambda x: x.distance)[:20]

        # Find the bounding box of the matched keypoints
        if matches:
            src_pts = np.float32([kp_ref[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp_frame[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

            # Compute the homography
            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

            if M is not None:
                h, w = reference_image.shape
                pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
                dst = cv2.perspectiveTransform(pts, M)

                # Overlay the video only on the detected area
                ret, video_frame = video_capture.read()
                if not ret:
                    # If the video has ended, restart it from the beginning
                    video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    ret, video_frame = video_capture.read()
                if ret:
                    h_v, w_v, _ = frame.shape
                    video_frame_resized = cv2.resize(video_frame, (w, h))

                    # Create a mask for the detected region
                    mask = np.zeros_like(frame, dtype=np.uint8)
                    cv2.fillPoly(mask, [np.int32(dst)], (255, 255, 255))

                    # Warp the video frame to fit the detected area
                    warped_video = cv2.warpPerspective(video_frame_resized, M, (w_v, h_v))

                    # Blend only the detected area with the video
                    overlay_frame = cv2.bitwise_and(warped_video, mask) + cv2.bitwise_and(frame, cv2.bitwise_not(mask))

                    # Display the resulting frame
                    # cv2.imshow("Feature Matching Overlay", overlay_frame)
    return overlay_frame









''''
import cv2
import numpy as np


def initialize_camera(url):
    """Initialize the phone camera stream."""
    cap = cv2.VideoCapture(url)
    if not cap.isOpened():
        raise ValueError(f"Error: Cannot access phone camera at {url}!")
    return cap


def initialize_overlay_video(video_path):
    """Initialize the overlay video."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Error: Cannot open overlay video at {video_path}!")
    return cap


def find_homography_and_draw(template_kp, frame_kp, matches, template_shape):
    """Find the homography matrix and draw the detected region."""
    src_pts = np.float32([template_kp[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([frame_kp[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

    # Compute homography
    matrix, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    if matrix is None:
        return None, None

    # Template corners for perspective transformation
    h, w = template_shape
    corners = np.float32([[0, 0], [0, h], [w, h], [w, 0]]).reshape(-1, 1, 2)
    transformed_corners = cv2.perspectiveTransform(corners, matrix)

    return matrix, transformed_corners


def apply_overlay(frame_live, overlay_frame, corners):
    """Warp overlay frame to match the detected area and blend it with the live video frame."""
    overlay_h, overlay_w = overlay_frame.shape[:2]
    src_overlay_pts = np.float32([[0, 0], [0, overlay_h], [overlay_w, overlay_h], [overlay_w, 0]])
    dst_overlay_pts = np.float32(corners)

    transform_matrix = cv2.getPerspectiveTransform(src_overlay_pts, dst_overlay_pts)
    warped_overlay = cv2.warpPerspective(overlay_frame, transform_matrix, (frame_live.shape[1], frame_live.shape[0]))

    # Create mask for overlay
    mask = np.zeros_like(frame_live, dtype=np.uint8)
    cv2.fillPoly(mask, [np.int32(corners)], (255, 255, 255))

    # Blend overlay with live frame
    mask_inv = cv2.bitwise_not(mask)
    frame_background = cv2.bitwise_and(frame_live, mask_inv)
    overlay_foreground = cv2.bitwise_and(warped_overlay, mask)

    return cv2.add(frame_background, overlay_foreground)


def modify_frame(frame_live):
    # Load the template image
    template = cv2.imread('static/pic1.jpeg', 0)
    if template is None:
        raise ValueError("Error: Template image not found!")

    # Initialize feature detector (ORB for speed)
    orb = cv2.ORB_create(nfeatures=1000)
    template_keypoints, template_descriptors = orb.detectAndCompute(template, None)
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)

    # Camera and overlay video initialization
    overlay_video_path = 'static/vid1.mp4'
    cap_overlay = initialize_overlay_video(overlay_video_path)

    # Resize live frame for faster processing
    frame_live_resized = cv2.resize(frame_live, (640, 360))

    # Read overlay video frame
    ret_overlay, frame_overlay = cap_overlay.read()
    if not ret_overlay:
        cap_overlay.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret_overlay, frame_overlay = cap_overlay.read()

    # Resize overlay for better blending performance
    frame_overlay_resized = cv2.resize(frame_overlay, (320, 180))

    frame_gray = cv2.cvtColor(frame_live_resized, cv2.COLOR_BGR2GRAY)
    frame_keypoints, frame_descriptors = orb.detectAndCompute(frame_gray, None)

    # Match descriptors
    if frame_descriptors is not None and template_descriptors is not None:
        raw_matches = matcher.knnMatch(template_descriptors, frame_descriptors, k=2)

        # Apply Lowe's ratio test
        good_matches = [m for m, n in raw_matches if m.distance < 0.75 * n.distance]

        # Proceed if sufficient matches are found
        if len(good_matches) > 10:
            matrix, transformed_corners = find_homography_and_draw(
                template_keypoints, frame_keypoints, good_matches, template.shape
            )

            if matrix is not None:
                # Scale transformed corners to match original frame size
                scale_x = frame_live.shape[1] / frame_live_resized.shape[1]
                scale_y = frame_live.shape[0] / frame_live_resized.shape[0]
                transformed_corners *= [scale_x, scale_y]

                # Apply overlay
                frame_live = apply_overlay(frame_live, frame_overlay_resized, transformed_corners)

    return frame_live

    '''