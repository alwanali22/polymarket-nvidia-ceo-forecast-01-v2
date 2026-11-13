import json
import os
import math
import glob

def get_population_std(data):
    if len(data) < 2:
        return 0.0
    changes = [data[i] - data[i-1] for i in range(1, len(data))]
    if not changes:
        return 0.0
    mean_change = sum(changes) / len(changes)
    variance = sum((c - mean_change) ** 2 for c in changes) / len(changes)
    return math.sqrt(variance)

def get_median(data):
    if not data:
        return 0.0
    sorted_data = sorted(data)
    n = len(sorted_data)
    if n % 2 == 1:
        return sorted_data[n // 2]
    else:
        return (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2

def get_percentile(data, p):
    if not data:
        return 0.0
    sorted_data = sorted(data)
    n = len(sorted_data)
    idx = p * (n - 1)
    i = int(idx)
    frac = idx - i
    if i + 1 < n:
        return sorted_data[i] + frac * (sorted_data[i + 1] - sorted_data[i])
    return sorted_data[i]

def get_quantiles_for_horizon(median, spread, horizon):
    raw_quantiles = [
        median + spread * -1.644854,
        median + spread * -0.674490,
        median,
        median + spread * 0.674490,
        median + spread * 1.644854
    ]
    
    # Clamp and enforce non-decreasing
    quantiles = []
    last_q = -1.0
    for q in raw_quantiles:
        q = max(0.0, min(1.0, q))
        q = max(q, last_q)
        quantiles.append(round(q, 6))
        last_q = q
    return quantiles

def solve():
    input_dir = os.environ.get("MAKEFUN_INPUT_DIR", "/input/")
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output/")
    
    os.makedirs(output_dir, exist_ok=True)
    
    input_files = glob.glob(os.path.join(input_dir, "*.in"))
    
    for input_file in input_files:
        base_name = os.path.basename(input_file)
        if base_name.endswith(".in"):
            case_id = base_name[:-3]
        else:
            case_id = base_name
        output_file = os.path.join(output_dir, f"{case_id}.out")
        
        with open(input_file, 'r') as f:
            case_data = json.load(f)
            
        markets = case_data.get("markets", [])
        
        # Regime detection
        total_std = 0.0
        for m in markets:
            prices = m.get("prices", [])
            total_std += get_population_std(prices)
            
        realized_volatility = total_std / len(markets) if markets else 0.0
        tau = 360 if realized_volatility > 0.024171 else 1080
        
        forecasts = []
        for m in markets:
            prices = m.get("prices", [])
            x = prices[-1] if prices else 0.0
            
            # Median L
            L = get_median(prices[-360:])
            
            # Spread S
            diffs = [p - L for p in prices[-1440:]]
            if len(diffs) > 1:
                p75 = get_percentile(diffs, 0.75)
                p25 = get_percentile(diffs, 0.25)
                S = (p75 - p25) / 1.349
            else:
                S = 0.0005 # Fallback
                
            S = max(0.0005, min(0.05, S))
            
            q_rows = []
            for h in range(1, 241):
                median = x + (L - x) * (1 - math.exp(-h / tau))
                variance = (S**2 * (1 - math.exp(-2 * h / tau))) + (0.0002**2 * h)
                spread = math.sqrt(variance)
                
                q_rows.append(get_quantiles_for_horizon(median, spread, h))
            
            forecasts.append({
                "id": m["id"],
                "q": q_rows
            })
            
        with open(output_file, 'w') as f:
            json.dump({"forecasts": forecasts}, f)
        print(f"Processed {case_id}")

if __name__ == "__main__":
    solve()
