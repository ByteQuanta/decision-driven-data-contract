from pathlib import Path
import pandas as pd


class DataLoader:
    def __init__(self, input_dir: str):
        self.input_dir = Path(input_dir)

    def load_latest(self) -> pd.DataFrame:
        """
        Loads the most recent CSV file from the input directory.
        Assumes files are named with sortable timestamps.
        """
        csv_files = sorted(self.input_dir.glob("*.csv"))

        if not csv_files:
            raise FileNotFoundError("No incoming CSV files found.")

        latest_file = csv_files[-1]
        df = pd.read_csv(latest_file)

        df.attrs["source_file"] = latest_file.name
        df.attrs["row_count"] = len(df)

        return df
