FROM tensorflow/tensorflow:1.1.0-devel

MAINTAINER Curtis Hawthorne <fjord@google.com>

# Download and build Magenta.

ENV MAGENTA_MASTER_REF v0.1.13

# Required for local development
RUN pip install scipy matplotlib intervaltree bokeh

WORKDIR /
RUN git clone https://github.com/tensorflow/magenta.git && \
    cd magenta && \
    git reset --hard $MAGENTA_MASTER_REF
WORKDIR /magenta
RUN bazel build //magenta/... && bazel test --test_output=errors //magenta/...

RUN bazel build magenta/tools/pip:build_pip_package && \
    bazel-bin/magenta/tools/pip/build_pip_package /tmp/magenta_pkg && \
    pip install --upgrade /tmp/magenta_pkg/magenta-*.whl

# Add pre-trained models (specific only)
ADD http://download.magenta.tensorflow.org/models/attention_rnn.mag /magenta-models/

# /magenta-data should be mapped to the host on startup.
RUN mkdir /magenta-data
WORKDIR /magenta-data

RUN cd ~ && \
  git clone https://github.com/JustinShenk/genre-melodies.git && \
  cd genre-melodies && \
  git checkout jazz && \
  pip install -r requirements.txt && \
  python create_dataset.py && \
  bash train_model.sh

# Start an interactive shell

CMD ["bash"]
