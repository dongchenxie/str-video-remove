### Keep only

example.mp4
example.srt

in /files before start

### to start

docker build -t video_processor .
docker run -dit -v .\files:/app/files video_processor
