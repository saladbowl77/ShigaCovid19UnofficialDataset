#!/usr/bin/bash
cd /home/pi/Desktop/python/covid19-dataset; git pull origin main; git add .; git commit -m "updateData"; git push origin HEAD:main
