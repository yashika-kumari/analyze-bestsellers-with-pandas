import pandas as pd
import matplotlib.pyplot as plt


def main() -> None:
	df = pd.read_csv("bestsellers.csv")

	original_rows = len(df)
	df = df.drop_duplicates()
	deduped_rows = len(df)

	df.rename(
		columns={"Name": "Title", "Year": "Publication Year", "User Rating": "Rating"},
		inplace=True,
	)

	# Convert numeric columns and keep track of any issues for the report.
	df["Price_raw"] = df["Price"]
	df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
	df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
	invalid_price_rows = df[df["Price"].isna()]

	author_counts = df["Author"].value_counts()
	print(author_counts)

	avg_rating_by_genre = df.groupby("Genre")["Rating"].mean()
	print(avg_rating_by_genre)

	# Core summary outputs
	author_counts.head(10).to_csv("top_authors.csv")
	avg_rating_by_genre.to_csv("avg_rating_by_genre.csv")

	# Additional breakdowns and stats
	df["Genre"].value_counts().to_csv("genre_counts.csv")

	price_stats = df.groupby("Genre")["Price"].agg(["min", "median", "mean", "max"])
	price_stats.to_csv("price_stats_by_genre.csv")

	rating_stats = df.groupby("Genre")["Rating"].agg(["count", "mean", "std"])
	rating_stats.to_csv("rating_stats_by_genre.csv")

	columns_for_top = [
		col
		for col in ["Title", "Author", "Price", "Rating", "Genre", "Publication Year", "Reviews"]
		if col in df.columns
	]

	top_expensive = df.dropna(subset=["Price"]).sort_values("Price", ascending=False).head(10)
	top_expensive[columns_for_top].to_csv("top_expensive_books.csv", index=False)

	if "Reviews" in df.columns:
		top_rated = df.sort_values(
			by=["Rating", "Reviews"], ascending=[False, False]
		).head(10)
	else:
		top_rated = df.sort_values("Rating", ascending=False).head(10)
	top_rated[columns_for_top].to_csv("top_rated_books.csv", index=False)

	# Data quality report
	missing_counts = df.isna().sum()
	unique_authors = df["Author"].nunique()
	unique_titles = df["Title"].nunique()
	with open("data_quality_report.txt", "w", encoding="utf-8") as f:
		f.write("Data Quality Report\n")
		f.write("====================\n")
		f.write(f"Total rows (original): {original_rows}\n")
		f.write(f"Total rows (after dedupe): {deduped_rows}\n")
		f.write(f"Duplicates removed: {original_rows - deduped_rows}\n\n")
		f.write("Missing values per column:\n")
		for col, count in missing_counts.items():
			f.write(f"- {col}: {count}\n")
		f.write("\nUnique counts:\n")
		f.write(f"- Authors: {unique_authors}\n")
		f.write(f"- Titles: {unique_titles}\n")
		f.write("\nNon-numeric prices (if any):\n")
		if invalid_price_rows.empty:
			f.write("- None\n")
		else:
			for _, row in invalid_price_rows.iterrows():
				f.write(f"- Title: {row.get('Title', 'N/A')} | Price value: {row.get('Price_raw', 'N/A')}\n")

	# Visualization: average rating by genre
	plt.figure(figsize=(8, 5))
	avg_rating_by_genre.sort_values().plot(kind="bar", color="#4C72B0")
	plt.ylabel("Average Rating")
	plt.xlabel("Genre")
	plt.title("Average Rating by Genre")
	plt.tight_layout()
	plt.savefig("avg_rating_by_genre.png", dpi=200)
	plt.close()


if __name__ == "__main__":
	main()
