import json
import sys
from typing import Any, Dict, Union

import numpy as np


def load_payload() -> Dict[str, Any]:
    if len(sys.argv) > 1:
        try:
            return json.loads(sys.argv[1])
        except json.JSONDecodeError:
            pass
    return {}


def calculate_stats(text: str) -> Dict[str, Union[int, float]]:
    words = [token for token in text.split() if token]
    word_lengths = np.array([len(word) for word in words], dtype=float)

    stats = {
        "chars": len(text),
        "words": len(words),
        "unique_words": len(set(words)),
    }

    if word_lengths.size:
        stats.update(
            {
                "avg_word_length": float(np.mean(word_lengths)),
                "median_word_length": float(np.median(word_lengths)),
                "std_word_length": float(np.std(word_lengths)),
            }
        )
    else:
        stats.update(
            {
                "avg_word_length": 0.0,
                "median_word_length": 0.0,
                "std_word_length": 0.0,
            }
        )

    return stats


def main() -> None:
    payload = load_payload()
    text = str(payload.get("text", ""))

    result = dict(payload)
    result["stats"] = calculate_stats(text)

    print(json.dumps(result))


if __name__ == "__main__":
    main()
