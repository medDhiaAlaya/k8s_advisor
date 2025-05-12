from k8s_collector import get_cluster_summary
from gemini_client import analyze_cluster

def main():
    print("[INFO] Collecting cluster data...")
    summary = get_detailed_cluster_info()
    print(f"[INFO] Data collected.")

    print("[INFO] Sending data to Gemini...")
    advice = analyze_cluster(summary)

    print("\n📊 Gemini's Recommendations:\n")
    print(advice)

    with open("recommendations.txt", "w") as f:
        f.write(advice)
    print("\n✅ Recommendations saved to recommendations.txt")


if __name__ == "__main__":
    main()
