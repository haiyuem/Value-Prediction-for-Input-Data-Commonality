#include <stdio.h>
#include <stdlib.h>

static const int num_frame = 10;
static const int frame_size = 200;

int func (int* array) {
    for (int i = 0; i < num_frame; i++) {
        for (int j = 0; j < frame_size; j++){
            array[i*frame_size + j] += 1;
        }
    }
    return 0;
}

int main(int argc, char ** argv) {
    int* array = malloc((num_frame * frame_size) * sizeof(int));
    for (int i = 0; i < num_frame * frame_size; i++)
        array[i] = 127;
    func(array);
    free(array);
    return 0;
}