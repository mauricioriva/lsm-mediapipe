import argparse

from video_processing import VideoProcessing
from hand_detection import HandDetection
from database import Database
from hand_position import HandPosition


class StoreHandLandMarks:
    def __init__(self, video_location, hand_position: HandPosition):
        self.video = VideoProcessing(video_location)
        self.hand_position = hand_position

    def store(self):
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--video', required=True)
    parser.add_argument('-p', '--hand-position', type=HandPosition.from_string, required=True)
    args = parser.parse_args()
