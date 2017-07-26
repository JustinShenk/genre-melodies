#!/usr/bin/env bash

cd subsets
BASE_PATH=$(pwd)

for genre in */ ; do convert_dir_to_note_sequences \
  --input_dir=$genre \
  --output_file=/tmp/${genre%/}_notesequences.tfrecord \
  --recursive;
done

for genre in */ ; do melody_rnn_create_dataset \
  --config=attention_rnn \
  --input=/tmp/${genre%/}_notesequences.tfrecord \
  --output_dir="sequence_examples/${genre}"
  --eval_ratio=0.10 && echo "INFO: ${genre%/} database created."
done

echo "INFO: Melody database creation completed."

for genre in */ ;
do
  if [[ $genre == *examples* ]]; then continue;
fi;
melody_rnn_train \
  --config="attention_rnn" \
  --run_dir=/tmp/melody_rnn/logdir/run1/${genre} \
  --sequence_example_file=$(pwd)/sequence_examples/${genre%/}_training_melodies.tfrecord \
  --num_training_steps=20000;
  echo "INFO: ${genre%/} model trained."
done

echo "INFO: Melody data models trained."

for genre in */ ;
do if [[ $genre == *examples* ]]; then continue; fi; melody_rnn_generate \
  --config=attention_rnn \
  --run_dir=/tmp/melody_rnn/logdir/run1/${genre} \
  --output_dir=/tmp/melody_rnn/generated/${genre} \
  --num_outputs=10 \
  --num_steps=128 \
  --primer_melody="[60]";
  echo "INFO: ${genre%/} melodies generated."
done
