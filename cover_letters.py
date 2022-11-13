import csv
import subprocess
import os
import shutil

SEPARATE_FOLDERS = True

CSV_FILE_NAME = 'Job_Postings.csv'
TEX_FILE_NAME = 'Cover_Template.tex'
PDF_FILE_NAME = 'Cover_Template.pdf'
CSV_FILE_AUX_NAME = 'addresses_1.csv'
SIGNATURE_FILE_NAME = 'Signature_File.png'


with open(CSV_FILE_NAME, 'r') as csv_file:
	reader = csv.reader(csv_file)
	
	# Get the header and skip over it
	header = next(reader)

	for row in reader:
		# Write the csv file needed for pdf generation
		with open(CSV_FILE_AUX_NAME, 'w') as write_handler:
			aux_writer = csv.writer(write_handler)
			aux_writer.writerow(header)
			aux_writer.writerow(row[:-1])

		# Generate the pdf
		result = subprocess.run(
			['pdflatex', TEX_FILE_NAME],
		)

		# Find a good name for the pdf file
		institution = row[0].replace(' ', '_')
		position = row[1].replace(' ', '_')
		pdf_title = f'{institution}_{position}_cover.pdf'

		if SEPARATE_FOLDERS:
			folder = institution

			pdf_title = f'{folder}/{institution}_{position}_cover.pdf'

			if not os.path.exists(folder):
				os.mkdir(folder)

			shutil.copyfile(CSV_FILE_AUX_NAME, f"{folder}/{CSV_FILE_AUX_NAME}")
			shutil.copyfile(TEX_FILE_NAME, f"{folder}/{TEX_FILE_NAME}")
			shutil.copyfile(SIGNATURE_FILE_NAME, f"{folder}/{SIGNATURE_FILE_NAME}")
		else:
			idx = 2
			while os.path.exists(pdf_title):
				pdf_title = f'{institution}_{position}_cover_{idx}.pdf'
				idx += 1

		# Rename the pdf file
		os.rename(PDF_FILE_NAME, pdf_title)
