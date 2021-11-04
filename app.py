from FAST import app, db

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("--delete-database", action="store_true")

	args = parser.parse_args()
	if args.delete_database:
		for table in reversed(db.metadata.sorted_tables):
			print(f"Cleared table {table}")
			db.session.execute(table.delete())
			db.session.commit()

	app.run(debug=True)
