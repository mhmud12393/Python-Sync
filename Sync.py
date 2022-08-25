import argparse
import os
import shutil
import time

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--source_folder", required=True,
	help="Source folder path")
ap.add_argument("-r", "--replica_folder", required=True,
	help="Replica folder path")
ap.add_argument("-i", "--interval", required=True,
	help="Synchronization interval in seconds")
ap.add_argument("-l", "--log_file", required=True,
	help="Log file path")
args = vars(ap.parse_args())

# Check if the source and replica folder exist
if os.path.exists(args["source_folder"]) == False:
	print("[INFO] Source folder not found. Creating the folder")
	os.mkdir(args["source_folder"])

if os.path.exists(args["replica_folder"]) == False:
	print("[INFO] Replica folder not found. Creating the folder")
	os.mkdir(args["replica_folder"])

# Empty the replica folder
for filename in os.listdir(args["replica_folder"]):
	filePath = os.path.join(args["replica_folder"], filename)
	try:
		if os.path.isfile(filePath) or os.path.islink(filePath):
			os.unlink(filePath)
		elif os.path.isdir(filePath):
			shutil.rmtree(filePath)
	except Exception as e:
		print('Failed to delete %s. Reason: %s' % (filePath, e))

# Initialize the log file
f = open(args["log_file"], "w")
f.write("Synchronization log\n")
f.write("====================\n")
f.write("utc_time\tfile_operation\tfile_name\n")

# Perform synchronization
while True:
	for filename in os.listdir(args["source_folder"]):
		filePath = os.path.join(args["source_folder"], filename)
		replicaFilePath = os.path.join(args["replica_folder"], filename)

		# If the file is a directory then copy the directory recursively
		if os.path.isdir(filePath):
			if os.path.exists(replicaFilePath) == False:
				print("[INFO] Creating the directory {}".format(filename, encoding="utf-8"))
				os.mkdir(replicaFilePath)
				f.write("{}\tcreate\t{}\n".format(time.time(), filename, encoding="utf-8"))
				shutil.copytree(filePath, replicaFilePath)
				f.write("{}\tcopy\t{}\n".format(time.time(), filename, encoding="utf-8"))

		# If the file is a file then simply copy the file
		elif os.path.isfile(filePath):
			if os.path.exists(replicaFilePath) == False:
				print("[INFO] Copying the file {}".format(filename))
				shutil.copyfile(filePath, replicaFilePath)
				f.write("{}\tcopy\t{}\n".format(time.time(), filename, encoding="utf-8"))

	# Remove files from the replica folder which are not present in the source folder
	for filename in os.listdir(args["replica_folder"]):
		filePath = os.path.join(args["replica_folder"], filename, encoding="utf-8")
		sourceFilePath = os.path.join(args["source_folder"], filename, encoding="utf-8")

		# If the file is a directory then remove the directory recursively
		if os.path.isdir(filePath):
			if os.path.exists(sourceFilePath) == False:
				print("[INFO] Deleting the directory {}".format(filename), encoding="utf-8")
				shutil.rmtree(filePath)
				f.write("{}\tdelete\t{}\n".format(time.time(), filename, encoding="utf-8"))

		# If the file is a file then simply delete the file
		elif os.path.isfile(filePath):
			if os.path.exists(sourceFilePath) == False:
				print("[INFO] Deleting the file {}".format(filename), encoding="utf-8")
				os.unlink(filePath)
				f.write("{}\tdelete\t{}\n".format(time.time(), filename, encoding="utf-8"))

	# Sleep for interval seconds
	time.sleep(int(args["interval"]))
