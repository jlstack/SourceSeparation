__author__ = 'lukestack'
import numpy as np
import nmf
from scipy.io.wavfile import read
import pickle
import stft as transform

"""
Creating training data.
"""


fs = 44100.0
nfft = 2048.0
noverlap = 1024.0
framesz = nfft/fs
hop = framesz - noverlap/fs
NUM_COMPONENTS = 20
ITERATIONS = 1000


def read_and_nmf(input_file):
    """
    :param input_file: file to be read
    :return: w (components from nmf)
    """
    (rate, data) = read(input_file)
    bee_data = (data[:, 0] + data[:, 1]) / 2.0
    if np.amin(bee_data) < -1 or np.amax(bee_data) > 1:
        bee_data /= float(max(abs(np.amax(bee_data)), abs(np.amin(bee_data))))
    T = len(bee_data) / fs
    X = transform.stft(bee_data, fs, framesz, hop)
    M = abs(X)
    w, h = nmf.factorize(M, pc=NUM_COMPONENTS, iterations=ITERATIONS)
    return w


def write_pickle(components, output_path):
    """
    :param components: w found in nmf
    :param output_path: path to write pickle to
    :return:
    """
    with open(output_path, 'wb') as output_:
            pickle.dump(components, output_)
    print components.shape


def main():
    components = read_and_nmf("/Users/lukestack/PycharmProjects/SourceSeparation/Audio/Control Files/Bees/TrainingBeesNormalized.wav")
    write_pickle(components, "/Users/lukestack/PycharmProjects/SourceSeparation/Audio/Control Files/Matrices/bees.pkl")


if __name__ == "__main__":
    main()