import cv2

def main():
    filename = 'video.mp4'
    vidcap = cv2.VideoCapture(filename)
    count = 0
    success = True
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))
    width = int(vidcap.get(3))
    height = int(vidcap.get(4))
    video = cv2.VideoWriter('timelapse.avi', 0, 30, (width, height))

    frames = 0
    while success:
        success, image = vidcap.read()
        if count % (3 * fps) == 0:
            video.write(image)
            print(f'successfully {frames}')
            frames += 1
        count += 1
    video.release()
    cv2.destroyAllWindows()

main()