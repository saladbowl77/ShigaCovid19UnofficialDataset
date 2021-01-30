#!/usr/bin/bash
cd /home/pi/Desktop/python/ShigaCovid19UnofficialDataset; git pull origin main; git add .; git commit -m "updateData"; git push origin HEAD:main
