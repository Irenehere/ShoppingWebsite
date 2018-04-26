import sys
import RecommendationSys

if __name__ == "__main__":
    customer_id = sys.argv[1]
    N = sys.argv[2]
    print(RecommendationSys.getRecommendation(customer_id,N=N))
