import argparse
import yaml
import pandas as pd
import numpy as np
import logging
import time
import json
import sys


def write_error_metrics(output_file, message):
    metrics = {
        "version": "v1",
        "status": "error",
        "error_message": message
    }

    with open(output_file, "w") as f:
        json.dump(metrics, f, indent=4)

    print(json.dumps(metrics, indent=4))


def main():
    start_time = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--log-file", required=True)

    args = parser.parse_args()

    logging.basicConfig(
        filename=args.log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    logging.info("Job started")

    try:
        # Load config
        with open(args.config, "r") as f:
            config = yaml.safe_load(f)

        required = ["seed", "window", "version"]

        for key in required:
            if key not in config:
                raise ValueError(f"Missing config key: {key}")

        seed = config["seed"]
        window = config["window"]
        version = config["version"]

        np.random.seed(seed)

        logging.info(
            f"Config loaded | seed={seed}, window={window}, version={version}"
        )

        # Load CSV
        df = pd.read_csv(args.input)

        if df.empty:
            raise ValueError("CSV file is empty")

        if "close" not in df.columns:
            raise ValueError("Missing required column: close")

        logging.info(f"Rows loaded: {len(df)}")

        # Rolling mean
        logging.info("Computing rolling mean")

        df["rolling_mean"] = df["close"].rolling(window=window).mean()

        # Signal
        logging.info("Generating signals")

        df["signal"] = (
            df["close"] > df["rolling_mean"]
        ).astype(int)

        rows_processed = len(df)

        signal_rate = float(df["signal"].mean())

        latency_ms = int((time.time() - start_time) * 1000)

        metrics = {
            "version": version,
            "rows_processed": rows_processed,
            "metric": "signal_rate",
            "value": round(signal_rate, 4),
            "latency_ms": latency_ms,
            "seed": seed,
            "status": "success"
        }

        with open(args.output, "w") as f:
            json.dump(metrics, f, indent=4)

        logging.info(f"Metrics: {metrics}")
        logging.info("Job completed successfully")

        print(json.dumps(metrics, indent=4))

    except Exception as e:
        logging.exception("Job failed")

        write_error_metrics(args.output, str(e))

        sys.exit(1)


if __name__ == "__main__":
    main()