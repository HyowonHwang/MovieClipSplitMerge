#!/bin/bash
count_frames () {
	ffprobe -v error -count_frames -select_streams v:0 \
		-show_entries stream=nb_read_frames \
		-of default=nokey=1:noprint_wrappers=1 "$@"
}

while getopts o: ch; do
	case $ch in
		(o) output=$OPTARG;;
	esac
done
shift $((OPTIND-1))

[ "$output" ] || {
	echo "ERROR: you must provide an output filename" >&2
	exit 2
}

workdir=$(mktemp -d fadeXXXXXX)
trap "rm -rf $workdir" EXIT

echo "processing $1"
frames=$(count_frames "$1")
ffmpeg -v error -i "$1" -vf fade=out:$((frames-15)):15 \
	-c:v libx264 -qp 0 -preset ultrafast \
	-strict -2 -y \
	$workdir/first.mp4
echo "file '$PWD/$workdir/first.mp4'" >> $workdir/concat.txt
shift

for vid in "$@"; do
	echo "processing $vid"
	vidtmp=$(mktemp $workdir/vidXXXXXX.mp4)
	frames=$(count_frames "$vid")
	ffmpeg -v error -i "$vid" \
		-vf "fade=in:0:15,fade=out:$((frames-15)):15" \
		-c:v libx264 -qp 0 -preset ultrafast \
		-strict -2 -y \
		$vidtmp
	echo "file '$PWD/$vidtmp'" >> $workdir/concat.txt
done

echo "concatenating segments"
ffmpeg -v error -f concat -safe 0 -i $workdir/concat.txt -c copy -y $workdir/final.mp4
ffmpeg -v error -c:a copy -c:v libx264 -profile:v high -level 4 -b:v 2157k -movflags +faststart -x264opts keyint=30:min-keyint=30:no-scenecut -r 30 $workdir/final_trans.mp4 -i $workdir/final.mp4
mv $workdir/final_trans.mp4 $output
