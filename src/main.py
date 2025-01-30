from generator import generate


if __name__ == "__main__":
    # Define duration variables
    total_duration_seconds = 10
    clip_duration_seconds = 3

    # parameters for video gen
    clip_density = 100  # how many videos to use
    audio_density = 10  # how many audios to use
    img_density = 0  # how many img to use


    generate(total_duration_seconds,
             clip_duration_seconds,
             clip_density,
             audio_density,
             img_density)