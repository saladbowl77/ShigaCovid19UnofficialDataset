#!/usr/bin/bash
cd /home/pi/Desktop/python/ShigaCovid19UnofficialDataset; git pull origin master; git add .; git commit -m "updateData"; git push origin HEAD:master
