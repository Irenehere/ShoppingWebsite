import sys
import RecommendationSys

if __name__ == "__main__":
    N = int(sys.argv[1])
    print(RecommendationSys.getPopularItem(N=N,beta=1))
