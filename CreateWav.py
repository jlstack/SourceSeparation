__author__ = 'lukestack'

from scipy.io.wavfile import read, write
import numpy as np
import os


def create_combined_wav(input_dir, file_name):
    """
    :param input_dir: directory containing wav files to be combined
    :param file_name: name of file being created
    :return: None
    """
    combined = None
    rate = 44100
    for file in os.listdir(input_dir):
        if file.endswith(".wav"):
            (rate, data) = read(input_dir + file)
            if combined is None:
                combined = data
            else:
                combined = np.vstack((combined, data))
    print type(combined), combined.shape, type(combined[0][0])
    if np.amin(combined) < -1 or np.amax(combined) > 1:
        combined = combined / float(max(abs(np.amax(combined)), abs(np.amin(combined))))
    write(file_name, rate, combined)


def create_slice(file_name, output_file_name, minute, second, num_seconds):
    """
    :param file_name: wav file that you want to take a slice from
    :param output_file_name: name of file being created
    :param minute: minute of starting position
    :param second: second of starting position
    :param num_seconds: length of slice in seconds
    :return: None
    """
    import wave
    wf = wave.open(file_name, 'rb')
    start = int(((minute * 60) + second) * wf.getframerate())
    num_frames = int(num_seconds * wf.getframerate())
    wf.setpos(start)
    frames = wf.readframes(num_frames)
    out = wave.open(output_file_name, 'wb')
    out.setframerate(wf.getframerate())
    out.setnchannels(wf.getnchannels())
    out.setsampwidth(wf.getsampwidth())
    out.writeframes(frames)
    out.close()


def main():
    #create_combined_wav("/Users/lukestack/PycharmProjects/SourceSeparation/Audio/Control Files/Bees/",
    #                    "Audio/Control Files/Bees/TrainingBeesNormalized.wav")
    create_slice("/Users/lukestack/PycharmProjects/SourceSeparation/Audio/Honey Bee Swarm Behavior Up Close and Personal (Low).wav",
                 "/Users/lukestack/PycharmProjects/SourceSeparation/Audio/Control Files/Bees/Test.wav", 18, 5, 30)

if __name__ == "__main__":
    main()