from k8s_collector import get_cluster_summary
from gemini_client import analyze_cluster

def main():
    print("[INFO] Collecting cluster data...")
    summary = get_cluster_summary()
    print(f"[INFO] Cluster Summary:\n{summary}")
    
    print("[INFO] Sending data to Gemini...")
    advice = analyze_cluster(summary)
    
    print("\n📊 Gemini's Recommendations:")
    print(advice)

if __name__ == "__main__":
    main()
