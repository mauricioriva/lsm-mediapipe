import cv2

from input_video import InputVideo


class VideoProcessing:
    def __init__(self, video_location):
        self.video = InputVideo(video_location)
        self.cap = cv2.VideoCapture(self.video.get_location())
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.frame_width = int(self.cap.get(3))
        self.frame_height = int(self.cap.get(4))

    def get_next_image(self):
        if not self.cap.isOpened():
            raise Exception('Video Capture is not opened')
        success, image = self.cap.read()
        if not success:
            # Empty camera frame
            self.cap.release()
            return None
        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        return image
