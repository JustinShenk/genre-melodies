#!/usr/bin/env bash

cd subsets

convert() {
  for genre in */
  do
    if [[ $genre == *examples* ]]
    then continue
    fi
    convert_dir_to_note_sequences \
    --input_dir=$genre \
    --output_file=/tmp/${genre%/}_notesequences.tfrecord \
    --recursive && echo "INFO: ${genre%/} converted to NoteSequences"
  done
}

create_database() {
  for genre in */
  do
    if [[ $genre == *examples* ]]
    then continue
    fi
    melody_rnn_create_dataset \
    --config=attention_rnn \
    --input=/tmp/${genre%/}_notesequences.tfrecord \
    --output_dir=sequence_examples/${genre} \
    --eval_ratio=0.10 && echo "INFO: ${genre%/} database created."
  done
}

train_models() {
  for genre in */
  do
    if [[ $genre == *examples* ]]
    then continue
    fi
    melody_rnn_train \
    --config=attention_rnn \
    --run_dir=/tmp/melody_rnn/logdir/run1/${genre} \
    --sequence_example_file=$(pwd)/sequence_examples/${genre%/}/training_melodies.tfrecord \
    --hparams="{'batch_size':64,'rnn_layer_sizes':[64,64]}" \
    --num_training_steps=10 && echo "INFO: ${genre%/} model trained."
  done
  echo "INFO: Training complete"
}

generate_melodies() {
  for genre in */ ;
  do
    if [[ $genre == *examples* ]];
    then continue
    fi
    melody_rnn_generate \
    --config=attention_rnn \
    --run_dir=/tmp/melody_rnn/logdir/run1/${genre} \
    --output_dir=/tmp/melody_rnn/generated/${genre} \
    --num_outputs=10 \
    --num_steps=128 \
    --hparams="{'batch_size':64,'rnn_layer_sizes':[64,64]}" \
    --primer_melody="[60]" && echo "INFO: ${genre%/} melodies generated."
  done
}

convert && echo "INFO: Files converted to NoteSequences." && \
create_database && echo "INFO: Database created." && \
train_models && echo "INFO: Melody data models trained." && \
generate_melodies && echo "INFO: Melodies generated." && \
echo "Completed."
