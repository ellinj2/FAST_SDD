from FAST import app, db

if __name__ == "__main__":
	# Add flag to reset database
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("--delete-database", action="store_true")

	args = parser.parse_args()
	
	# Reset databse for testing and simulations
	if args.delete_database:
		for table in reversed(db.metadata.sorted_tables):
			print(f"Cleared table {table}")
			db.session.execute(table.delete())
			db.session.commit()

	# Launch web app
	app.run(debug=False)
