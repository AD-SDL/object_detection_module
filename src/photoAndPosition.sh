image_file="$1"

darknet detector test /home/app/trained/trainingImages.data /home/app/trained/trainingImages.cfg /home/app/trained/trainingImages_last.weights -dont_show -ext_output "$image_file" > /home/app/.wei/temp/1
cat /home/app/.wei/temp/1 | grep left_x > /home/app/.wei/temp/output.txt