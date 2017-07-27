# Deep learning genre-specific melodies with Magenta

## Getting Started

This docker installation of a minimal jazz melody generation implementation which runs all of the scripts and begins generating:

```sh
docker run -it -p 6006:6006 -v /tmp/magenta:/genre-melodies justinshenk/melodic
```

Manual Magenta installation:
```sh
sudo apt-get update -y
sudo apt-get install libasound2-dev libasound-dev libjack-dev git -y
curl https://raw.githubusercontent.com/tensorflow/magenta/master/magenta/tools/magenta-install.sh > /tmp/magenta-install.sh &&
bash /tmp/magenta-install.sh
```
or using Conda (NOTE:  Magenta currently supports version 2 of Python):

```sh
conda create -n magenta python=2.7 jupyter
source activate magenta
```

Open a new terminal window so the environmental variable changes take effect and enter:

```sh
source activate magenta && pip install tensorflow-gpu &&
git clone https://github.com/JustinShenk/genre-melodies.git &&
cd genre-melodies &&
pip install -r requirements.txt &&
python create_dataset.py &&
sh train_model.sh
```

If using a CPU replace 'tensorflow-gpu' with 'tensorflow'.

## Preprocessing and Analysis

See the [preprocessing and visualization notebook](/create_dataset.ipynb) for sample outputs and visualization scripts.

Visualizations:

![2d visualization](/images/2d-genre-visualization.png)

![3d visualization](/images/3d-genre-visualization.png)

Tensorboard graph of trained network:

[<img src="/images/magenta_graph.png" alt="Tensorboard Graph" width="60%"/>](/images/magenta_graph.png)

## Postprocessing

Convert MIDIs to MP3 using timidity.

Install [timidity](http://macappstore.org/timidity/) with `brew install timidity` (OSX) or `sudo apt-get install timidity` (Ubuntu).

To play the sounds in a browser, convert the files to a format supported by HTML5, such as mp3. Find the generated MIDI files in `/tmp/melody_rnn/generated/[genre]`. Use a one-line shell command to convert MIDI files to mp3:

```sh
$ for file in *.mid ; do timidity "${file}" -Ow -o - | ffmpeg -i - -acodec libmp3lame -ab 64k "${file%.*}.mp3"; done
```

## Output

Check out some [samples](https://justinshenk.github.io/posts/2017/07/deep-genre/) with an explanation of Magenta's hyperparameters.
