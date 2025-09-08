from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
import glob
import os
import pygame

DIR = "Frames/"

def createMovieFromFrame(total_frame, base_filename, dir_output, fps_vid):

    image_files = sorted(glob.glob(f'{DIR}{base_filename}_*.png'))
    clip = ImageSequenceClip(image_files, fps=fps_vid)
    if not os.path.exists(f'OUTPUT/{dir_output}'):
        os.makedirs(f'OUTPUT/{dir_output}')
    clip.write_videofile(f'OUTPUT/{dir_output}/animation.mp4', codec='libx264')

    for i in range(total_frame):
        frame_path = f"{DIR}{base_filename}_{i:04d}.png"
        if os.path.exists(frame_path):
            os.remove(frame_path)
            
            
def saveFrame(recording, frame, support, base_filename, time, fps):
    if recording:
        pygame.image.save(support, f"Frames/{base_filename}_{frame:04d}.png")
        if frame % fps == 0:
            # Affichage de la progression dans la console
            print(f"{frame // fps} secondes / {time} enregistrée.")
    else:
        pygame.time.wait(int(1000 / fps))